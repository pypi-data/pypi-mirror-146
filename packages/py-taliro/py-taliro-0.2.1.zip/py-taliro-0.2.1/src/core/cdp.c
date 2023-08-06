#include "core/cdp.h"

#include <stdlib.h>

#include "banned.h"
#include "core/cdistances.h"  // csigned_dist
#include "core/dp.h"          // init_queue(), setupIndeces()
#include "core/distances.h"   // DistCompData, HyDis
#include "core/ltl2tree.h"  // FWTaliroParam, tl_lookup(), Miscellaneous, Node, PMap, queue, Symbol

/**
 * Calculate the system distances using a dynamic programming
 * approach.
 *
 * @param root Parsed root node of specification
 * @param pmap List of predicates
 * @param st State traces
 * @param ts Timestamps
 * @param lt Location traces
 * @param dists Hybrid distance data
 * @param params Set of parameters/settings
 * @param miscell Additional miscellaneous settings
 *
 * @return The robustness computation of the system
 */
HyDis cdp(Node *root, PMap *pmap, const double *st, const double *ts,
          const double *lt, DistCompData *dists, FWTaliroParam *params,
          Miscellaneous *miscell) {
  // PARSE TREE BREADTH-FIRST SEARCH
  queue q;
  init_queue(&q);

  int qi = 1;
  int root_size = BFS(&q, root, &qi);

  // FORMULA SETUP
  Node **subformulas = malloc(sizeof(Node *) * (root_size + 1));
  setupIndeces(subformulas, root);

  // TODO:
  //   - Check the index matches the subformula->index

  // MONITOR TABLE SETUP
  HyDis **table = malloc(sizeof(HyDis *) * (root_size + 1));
  int max_time = 0;

  for (int i = 1; i <= root_size; ++i) {
    table[i] = (HyDis *)malloc(sizeof(HyDis) * (params->nSamp));

    if (subformulas[i]->group > max_time) {
      max_time = subformulas[i]->group;
    }
  }

  // PREDICATE SETUP
  Symbol *sym;

  for (size_t i = 0; i < (params->nPred); ++i) {
    if (pmap[i].true_pred) {
      sym = tl_lookup(pmap[i].str, miscell);
      sym->set = &(pmap[i].set);
      sym->Normalized = pmap[i].Normalized;
      sym->NormBounds = pmap[i].NormBounds;
    }
  }

  // STATE TRACE SETUP
  double *traces;

  if (params->nInp > 4 && params->nCLG == 1) {
    traces = malloc(sizeof(double) * (params->SysDim + 1));
  } else {
    traces = malloc(sizeof(double) * (params->SysDim));
  }

  // TIMESTAMP SETUP
  double *timestamps = malloc(sizeof(double) * (params->nSamp));

  // COMPUTE ROBUSTNESS
  for (size_t i = 0; i < (params->nSamp); ++i) {
    timestamps[i] = ts[i];

    for (size_t ii = 0; ii < (params->SysDim); ++ii) {
      traces[ii] = st[i + ii * (params->nSamp)];
    }

    // copy location trace data if exists
    if (params->nInp > 4 && params->nCLG == 1) {
      traces[params->SysDim] = lt[i];
    }

    for (int ii = 1; ii <= root_size; ++ii) {
      switch (subformulas[ii]->ntyp) {
        case TRUE:
          table[ii][i] = SetToInf(+1, i);
          break;
        case FALSE:
          table[ii][i] = SetToInf(-1, i);
          break;
        case PREDICATE:
          // TODO:
          //   - Error Check(s)
          //       - Check if the set of the predicate has been defined

          if ((params->nInp >= 6) && (subformulas[ii]->sym->set->nloc > 0)) {
            // control location graph present
            if ((params->nInp == 7) && (dists->GuardMap)) {
              // guard map present
              table[ii][i] =
                  csigned_hdistg(traces, subformulas[ii]->sym->set,
                                 params->SysDim, dists, params->tnLoc);
              table[ii][i].iteration = i;
              table[ii][i].preindex = subformulas[ii]->sym->index;
            } else {
              // no guard map present
              table[ii][i] =
                  csigned_distzero(traces, subformulas[ii]->sym->set,
                                   params->SysDim, dists->LDist, params->tnLoc);
              table[ii][i].iteration = i;
              table[ii][i].preindex = subformulas[ii]->sym->index;
            }
          } else {
            // no control location graph
            table[ii][i].ds =
                csigned_dist(traces, subformulas[ii]->sym->set, params->SysDim);
            table[ii][i].dl = 0;
            table[ii][i].iteration = i;
            table[ii][i].preindex = subformulas[ii]->sym->index;
          }
          break;
        default:
          break;
      }
    }
  }

  // POST-PROCESSING COMPUTATION
  if ((params->LTL) == 1) {
    for (int i = ((int)(params->nSamp)) - 1; i >= 0; --i) {
      DP_LTL(subformulas, table, params, root_size, i, 0);
    }
  } else if ((params->TPTL) == 1) {
    double freezetime;

    for (int i = max_time; i >= 1; --i) {
      for (int ii = 0; ii < ((int)(params->nSamp)); ++ii) {
        freezetime = timestamps[ii];

        for (int iii = ((int)(params->nSamp)) - 1; iii >= ii; --iii) {
          Resolve_Constraint(subformulas, table, timestamps, root_size, iii, i,
                             freezetime);
        }

        for (int iii = ((int)(params->nSamp)) - 1; iii >= ii; --iii) {
          DP_LTL(subformulas, table, params, root_size, iii, i);
        }
      }
    }

    for (int i = ((int)(params->nSamp)) - 1; i >= 0; --i) {
      DP_LTL(subformulas, table, params, root_size, i, 0);
    }
  }

  root->rob = table[1][0];

  // MEMORY DEALLOCATION
  free(timestamps);
  free(traces);

  for (int i = 1; i <= root_size; ++i) {
    free(table[i]);
  }

  free(table);
  free(subformulas);

  return root->rob;
}
