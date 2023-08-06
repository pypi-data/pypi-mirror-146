#include "core/evaluate.h"

#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "banned.h"
#include "core/cdp.h"        // cdp
#include "core/distances.h"  // DistCompData
#include "core/ltl2tree.h"  // FWTaliroParam, Miscellaneous, #Nhash, Node, ParMap, PMap

/* temporary forward declaration(s) */
void countVar(int *, Node *, char *, int);

/**
 * Compute the resulting robustness of the
 * based on the provided constraints and trace data.
 *
 * @param spec TPTL formula
 * @param npreds Number of predicates
 * @param preds List of predicates
 * @param st_dims Dimensions of the state trace (must be two)
 * @param st_nrows Number of rows in the state trace
 * @param st_ncols Number of columns in the state trace
 * @param ts_dims Dimensions of the timestamp (must be two)
 * @param ts_nrows Number of rows in the timestamp
 * @param ts_ncols Number of columns in the timestamp
 *
 * @return The robustness calculation of the system
 */
Evaluation evaluate(char *spec, size_t npreds, Predicate *preds, size_t st_dims,
                    size_t st_nrows, size_t st_ncols, double *st,
                    size_t ts_dims, size_t ts_nrows, double *ts,
                    size_t lt_nrows, double *lt, size_t am_dims,
                    size_t am_nrows, size_t am_ncols, double *am,
                    size_t gm_dims, size_t gm_nrows, size_t gm_ncols,
                    Guard *gm) {
  // non-referenced parameter(s)
  UNUSED(st_dims);
  UNUSED(ts_dims);
  UNUSED(ts_nrows);
  UNUSED(lt_nrows);
  UNUSED(lt);
  UNUSED(am_dims);
  UNUSED(am_nrows);
  UNUSED(am_ncols);
  UNUSED(am);
  UNUSED(gm_dims);
  UNUSED(gm_nrows);
  UNUSED(gm_ncols);
  UNUSED(gm);

  /* double *dist = shortest_paths(am_nrows, am); */
  /* printMatrix(am_nrows, am_ncols, dist); */

  // print input(s)
  /* printEvaluateInputs(spec, npreds, preds, */
  /*                     st_dims, st_nrows, st_ncols, st, */
  /*                     ts_dims, ts_nrows, ts); */

  Miscellaneous miscell;
  miscell.dp_taliro_param.LTL = 1;
  miscell.dp_taliro_param.ConOnSamples = 0;
  miscell.dp_taliro_param.SysDim = 0;
  miscell.dp_taliro_param.nSamp = 0;
  miscell.dp_taliro_param.nPred = 0;
  miscell.dp_taliro_param.true_nPred = 0;
  miscell.dp_taliro_param.tnLoc = 0;
  miscell.dp_taliro_param.nInp = 0;
  miscell.dp_taliro_param.nCLG = 1;
  miscell.dp_taliro_param.nInp = 4;  // static-set
  miscell.tl_errs = 0;
  miscell.type_temp = 0;

  // SPECIFICATION SETUP
  // TODO:
  //   - Error Check(s):
  //      1. Formula size must be less than MAX_BUFFERSIZE
  //      2. Ensure it is null-terminated
  //      3. Ensure `snprintf` returned correctly

  char formula[MAX_BUFFERSIZE];
  size_t formula_size = 0;
  int nfreeze = 0;

  snprintf(formula, MAX_BUFFERSIZE, "%s", spec);
  formula_size = strlen(formula);

  // replace tabs, double-quotes, and newlines
  for (size_t i = 0; i < formula_size; ++i) {
    if (formula[i] == '\t' || formula[i] == '\"' || formula[i] == '\n') {
      formula[i] = ' ';
    }
  }

  // STATE TRACE SETUP
  // TODO:
  //   - Error Check(s):
  //      1. Ensure the dimensions == 2
  //      2. Ensure the number of rows >= 1
  //      3. Ensure the number of columns >= 1
  //      4. Ensure that `st` is not NULL

  miscell.dp_taliro_param.nSamp = st_nrows;
  miscell.dp_taliro_param.SysDim = st_ncols;

  // TIMESTAMP SETUP
  // TODO:
  //   - Error Check(s):
  //      1. Ensure the dimensions == 2
  //      2. Ensure the number of rows match the `nSamp`
  //      3. Ensure that `ts` is not NULL

  // LOCATION TRACE SETUP
  // TODO:
  //   - Error Check(s):
  //      1. Check the dimensions of `lt_ndims`
  //      2. Ensure `lt_nrows` == `miscell.dp_taliro_param.nSamp` (`st_nrows`)
  size_t nha = 0;

  DistCompData dists;
  dists.GuardMap = NULL;

  if (lt) {
    miscell.dp_taliro_param.nInp = 5;
    // CONTROL LOCATION GRAPH SETUP
    // TODO:
    //  - Error Check(s):
    //     1. Ensure `am` is not NULL
    //  - Implement multiple HA support

    if (am) {
      miscell.dp_taliro_param.nInp = 6;

      // compute shortest path(s) (floyd-warshall)
      double *sp = shortest_paths(am_nrows, am);

      double *ldist = pred_paths(npreds, preds, am_nrows, sp);
      free(sp);

      // single hybrid automata
      nha = 1;  // temporary (default)

      miscell.dp_taliro_param.tnLoc = am_nrows;
      dists.LDist = ldist;
    }
  }

  // GUARD MAP SETUP
  if (gm) {
    miscell.dp_taliro_param.nInp = 7;
    // ADJACENCY LIST SETUP
    // TODO:
    //   - Support multple adjacency lists
    //   - Ensure the adjacency list is NOT empty

    dists.AdjL = malloc(am_nrows * sizeof(double *));  // default 1 (tmp)
    dists.AdjLNell = malloc(am_nrows * sizeof(size_t));

    for (size_t i = 0; i < am_nrows; ++i) {
      size_t num_neighbors = get_num_neighbors(i, am_nrows, am);
      dists.AdjL[i] = get_neighbors(i, num_neighbors, am_nrows, am);

      dists.AdjLNell[i] = num_neighbors;
    }

    // GUARD SETUP
    // TODO:
    //   - Verify the guard is NxN (i.e., a square)

    dists.GuardMap = malloc(gm_nrows * sizeof(GuardSet *));

    for (size_t i = 0; i < gm_nrows; ++i) {
      if (dists.AdjLNell[i] > 0) {
        // a guard from i to j exists
        dists.GuardMap[i] = malloc(dists.AdjLNell[i] * sizeof(GuardSet));

        for (size_t j = 0; j < dists.AdjLNell[i]; ++j) {
          // TODO:
          //   - Implement projection checking

          size_t index = dists.AdjL[i][j] - 1;

          dists.GuardMap[i][j].nproj = 0;  // temporary (default)
          dists.GuardMap[i][j].nset = 1;   // temporary (default)
          dists.GuardMap[i][j].ncon =
              malloc(dists.GuardMap[i][j].nset * sizeof(int));

          // A matrix
          // TODO:
          //   - Check that A is not NULL
          //   - Implement union of polytopes

          dists.GuardMap[i][j].A =
              malloc(dists.GuardMap[i][j].nset * sizeof(double **));

          for (int k = 0; k < dists.GuardMap[i][j].nset; ++k) {
            // TODO:
            //   - Implement union of polytopes
            //   - Check dimensions of A
            //   - Verify the number of A columns == SysDim

            dists.GuardMap[i][j].ncon[k] = gm[index + i * gm_ncols].a_nrows;
            dists.GuardMap[i][j].A[k] =
                malloc(dists.GuardMap[i][j].ncon[k] * sizeof(double *));

            for (int ii = 0; ii < dists.GuardMap[i][j].ncon[k]; ++ii) {
              dists.GuardMap[i][j].A[k][ii] =
                  malloc(miscell.dp_taliro_param.SysDim * sizeof(double));

              for (size_t jj = 0; jj < miscell.dp_taliro_param.SysDim; ++jj) {
                dists.GuardMap[i][j].A[k][ii][jj] =
                    gm[index + i * gm_ncols]
                        .a[ii + jj * dists.GuardMap[i][j].ncon[k]];
              }
            }
          }

          // b matrix
          // TODO:
          //   - Check that b is not NULL
          //   - Implement union of polytopes

          dists.GuardMap[i][j].b =
              malloc(dists.GuardMap[i][j].nset * sizeof(double *));

          for (int k = 0; k < dists.GuardMap[i][j].nset; ++k) {
            // TODO:
            //   - Implement union of polytopes
            //   - Check dimensions of b
            //   - Verify the number of b rows == ncon[ik]

            dists.GuardMap[i][j].b[k] = gm[index + i * gm_ncols].b;
          }
        }
      }
    }
  }

  // PREDICATES SETUP
  // TODO:
  //   - Error Check(s):
  //      1. Ensure `npreds` is not zero
  //      2. Ensure that `preds` is not NULL

  PMap *pmap = malloc(sizeof(PMap) * npreds);

  miscell.dp_taliro_param.nPred = npreds;
  miscell.dp_taliro_param.true_nPred = npreds;

  miscell.parMap = (ParMap *)malloc(npreds * sizeof(ParMap));  // parameters
  miscell.predMap = (PMap *)malloc(npreds * sizeof(PMap));     // predicates
  miscell.pList.pindex = (int *)malloc(npreds * sizeof(int));

  // init predicate index list
  for (size_t i = 0; i < npreds; ++i) {
    miscell.pList.pindex[i] = -1;
  }

  // copy `preds` to `pmap`
  for (size_t i = 0; i < npreds; ++i) {
    // name
    // TODO:
    //   - Error Check(s):
    //      1. Ensure `pmap[i].str` is allocated properly
    //      2. Ensure resulting `pmap[i].str` copy is successful
    //      3. Ensure `miscell.predMap[i].str` is allocated properly
    //      4. Ensure resulting `miscell.predMap[i].str` copy is successful

    size_t name_size = strlen(preds[i].name) + 1;

    pmap[i].str = (char *)malloc(name_size * sizeof(char));
    snprintf(pmap[i].str, name_size, "%s", preds[i].name);

    miscell.predMap[i].str = (char *)malloc(name_size * sizeof(char));
    snprintf(miscell.predMap[i].str, name_size, "%s", preds[i].name);

    pmap[i].set.idx = (int)i;
    pmap[i].true_pred = true;

    // range
    // TODO:
    //   - Add range attribute to Predicate
    //   - Implement range setup/checks

    // normalization(s)
    // TODO:
    //   - Implement normalization setup/checks

    // projection(s)
    // TODO:
    //   - Add projection attribute to Predicate
    //   - Implement projection setup/checks

    pmap[i].set.nproj = 0;  // (temporarily default)

    // A matrix
    // TODO:
    //   - Check if A is NULL (if so, check for interval: do nothing?)

    if (preds[i].a_nrows == 0 || preds[i].a_ncols == 0) {
      // A is empty
      pmap[i].set.isSetRn = true;
      pmap[i].set.ncon = 0;
    } else {
      // A is not empty
      // TODO:
      //   - Ensure the dimensions == 2
      //   - Ensure the number of constraints match state trace
      //   - Ensure the system dimensions match the state trace
      //   - Ensure a max of two constraints is present for 1D state traces

      pmap[i].set.isSetRn = false;
      pmap[i].set.ncon = preds[i].a_nrows;

      // TODO:
      //   - Implement projection setup/checks (i.e. when `nproj` > 0)

      pmap[i].set.A = (double **)malloc(pmap[i].set.ncon * sizeof(double *));

      if (pmap[i].set.nproj == 0) {
        // always true (for now)
        for (int ii = 0; ii < pmap[i].set.ncon; ++ii) {
          size_t size = miscell.dp_taliro_param.SysDim;
          pmap[i].set.A[ii] = (double *)malloc(size * sizeof(double));

          for (size_t iii = 0; iii < size; ++iii) {
            pmap[i].set.A[ii][iii] = preds[i].a[ii + iii * pmap[i].set.ncon];
          }
        }
      }
    }

    // b matrix
    // TODO:
    //   - Check if b matrix is NULL
    //   - Ensure the dimensions of b == 2
    //   - Ensure the `b_nrows` == the number of constraints
    //   - Ensure the number of columns == 1

    pmap[i].set.b = preds[i].b;

    // TODO:
    //   - Check for redundant constraints

    // control location(s)
    // TODO:
    //   - Error Check(s):
    //       - Check that a location field is added to the predicate
    //       - Ensure the dimensions of loc == 2
    //       - Ensure the number of rows is NOT > 1
    //       - Ensure `loc` is not NULL
    //   - Determine better method for optional argument resolution(s)
    //   - Implement multiple hybrid automata predicate setup

    if (lt) {
      if (nha == 1) {
        pmap[i].set.nloc = preds[i].l_ncols;
        pmap[i].set.loc = preds[i].l;
      }
    }
  }

  // PARSING
  miscell.tl_out = stdout;

  miscell.zero2inf.l_closed = 1;
  miscell.zero2inf.u_closed = 0;
  miscell.emptyInter.l_closed = 0;
  miscell.emptyInter.u_closed = 0;

  if (miscell.dp_taliro_param.ConOnSamples) {
    miscell.zero.numi.inf = 0;
    miscell.zero.numi.i_num = 0;
    miscell.inf.numi.inf = 1;
    miscell.inf.numi.i_num = 0;
    miscell.zero2inf.lbd = miscell.zero;
    miscell.zero2inf.ubd = miscell.inf;
    miscell.emptyInter.lbd = miscell.zero;
    miscell.emptyInter.ubd = miscell.zero;
  } else {
    miscell.zero.numf.inf = 0;
    miscell.zero.numf.f_num = 0.0;
    miscell.inf.numf.inf = 1;
    miscell.inf.numf.f_num = 0.0;
    miscell.zero2inf.lbd = miscell.zero;
    miscell.zero2inf.ubd = miscell.inf;
    miscell.emptyInter.lbd = miscell.zero;
    miscell.emptyInter.ubd = miscell.zero;
  }

  // initialize symbol table
  for (size_t i = 0; i < (Nhash + 1); ++i) {
    miscell.symtab[i] = NULL;
  }

  // parse formula
  int tl_yychar;
  Node *root;

  LTL_ERROR = 0;
  root = tl_parse(&nfreeze, formula_size, formula, &miscell, &tl_yychar);

  // count freezetime variable(s)
  nfreeze = 0;
  countVar(&nfreeze, root, NULL, 0);

  // set temporal logic used (TPTL or LTL)
  if (nfreeze > 0) {
    miscell.dp_taliro_param.TPTL = 1;
    miscell.dp_taliro_param.LTL = 0;
  } else {
    miscell.dp_taliro_param.TPTL = 1;
    miscell.dp_taliro_param.LTL = 1;
  }

  // TODO:
  //   - Check if the formula is MTL with no timestamps

  // ROBUSTNESS COMPUTATION
  HyDis hdist =
      cdp(root, pmap, st, ts, lt, &dists, &(miscell.dp_taliro_param), &miscell);

  // MEMORY DEALLOCATION

  // predicate map
  for (size_t i = 0; i < npreds; ++i) {
    // name
    free(miscell.predMap[i].str);
    free(pmap[i].str);

    // A matrix
    for (int ii = 0; ii < pmap[i].set.ncon; ++ii) {
      free(pmap[i].set.A[ii]);
    }

    free(pmap[i].set.A);
  }

  // miscellaneous
  free(miscell.pList.pindex);
  free(miscell.predMap);
  free(miscell.parMap);

  // predicate map
  free(pmap);

  Evaluation eval;
  eval.dl = hdist.dl;
  eval.ds = hdist.ds;

  return eval;
}

/**
 * Given an adjacency matrix, compute the shortest
 * path between every vertex on the graph (i.e., floyd warshall algorithm).
 *
 * @param nv Number of vertices in the graph
 * @param am Directed graph represented as an adjacency matrix
 *
 * @return The resulting distance matrix between each (i, j) vertex
 */
double *shortest_paths(size_t nv, const double *am) {
  size_t nvnv = nv * nv;
  double *dist = malloc(sizeof(double) * nvnv);

  // initialize distances (A0 matrix)
  for (size_t i = 0; i < nvnv; ++i) {
    dist[i] = am[i];
  }

  // solve shortest distances (A1 -> AK matrix)
  for (size_t k = 0; k < nv; ++k) {
    for (size_t i = 0; i < nv; ++i) {
      for (size_t j = 0; j < nv; ++j) {
        if (dist[i + k * nv] + dist[k + j * nv] < dist[i + j * nv]) {
          dist[i + j * nv] = dist[i + k * nv] + dist[k + j * nv];
        }
      }
    }
  }

  return dist;
}

double *pred_paths(size_t npreds, Predicate *preds, size_t nv, double *sp) {
  size_t ndists = npreds * nv;
  double *ldist = malloc(ndists * sizeof(double));

  for (size_t i = 0; i < ndists; ++i) {
    ldist[i] = nv;
  }

  for (size_t i = 0; i < npreds; ++i) {
    for (size_t j = 0; j < preds[i].l_ncols; ++j) {
      int location = (int)preds[i].l[j];

      for (size_t k = 0; k < nv; ++k) {
        ldist[k + i * nv] = min(ldist[k + i * nv], sp[(location - 1) * nv + k]);
      }
    }
  }

  return ldist;
}

/*
 * Given an adjacency matrix and a location,
 * calculate the number of neighbors the provided
 * location has a transition to.
 *
 * @param location Location (row-wise) to find the number of neighbors of
 * @param nv Number of vertices in the control location graph
 * @param am Adjacency matrix as contiguous array
 *
 * @return The total number of neighbors of a location
 */
size_t get_num_neighbors(size_t location, size_t nv, const double *am) {
  size_t num_neighbors = 0;

  for (size_t i = 0; i < nv; ++i) {
    if (am[location + i * nv] == 1) {
      ++num_neighbors;
    }
  }

  return num_neighbors;
}

/*
 * Given an adjacency matrix and a location,
 * return a list of all locations the provided location
 * has a transition to.
 *
 * @param location Location (row-wise) to find neighbors of
 * @param num_neighbors The number of neighbors the location has
 * @param nv Number of vertices in the control location graph
 * @param am Adjacency matrix as contiguous array
 *
 * @return An array of neighboring locations
 */
double *get_neighbors(size_t location, size_t num_neighbors, size_t nv,
                      const double *am) {
  double *neighbors = malloc(num_neighbors * sizeof(double));
  size_t index = 0;

  for (size_t i = 0; i < nv; ++i) {
    if (am[location + i * nv] == 1) {
      neighbors[index] = (i + 1);  // start index is 1
      ++index;
    }
  }

  return neighbors;
}

void printEvaluatePredicate(Predicate pred, size_t index) {
  printf("\tPredicate #%zu\n", index);

  // name
  printf("\t\tName: %s\n", pred.name);

  // A matrix
  printf("\t\tA Matrix:\n");
  printf("\t\t\tDimensions: %zu\n", pred.a_dims);
  printf("\t\t\tNum Rows: %zu\n", pred.a_nrows);
  printf("\t\t\tNum Columns: %zu\n", pred.a_ncols);

  printf("\t\t\tRaw Value(s): ");
  for (size_t i = 0; i < pred.a_nrows * pred.a_ncols; ++i) {
    printf("%f ", pred.a[i]);
  }
  printf("\n");

  // b matrix
  printf("\t\tb Matrix:\n");
  printf("\t\t\tDimensions: %zu\n", pred.b_dims);
  printf("\t\t\tNum Rows: %zu\n", pred.b_nrows);
  printf("\t\t\tNum Columns: %zu\n", pred.b_ncols);

  printf("\t\t\tRaw Value(s): ");
  for (size_t i = 0; i < pred.b_nrows * pred.b_ncols; ++i) {
    printf("%f ", pred.b[i]);
  }
  printf("\n");

  return;
}

void printEvaluateInputs(char *spec, size_t npreds, Predicate *preds,
                         size_t st_dims, size_t st_nrows, size_t st_ncols,
                         double *st, size_t ts_dims, size_t ts_nrows,
                         double *ts) {
  // specification
  printf("SPECIFICATION:\n");
  printf("\t\"%s\"\n", spec);

  // predicate(s)
  printf("PREDICATES:\n");
  for (size_t i = 0; i < npreds; ++i) {
    printEvaluatePredicate(preds[i], i);
  }

  // state trace(s)
  printf("STATE TRACES:\n");
  printf("\tDimensions: %zu\n", st_dims);
  printf("\tNum Rows: %zu\n", st_nrows);
  printf("\tNum Columns: %zu\n", st_ncols);

  printf("\t\t\tRaw Value(s): ");
  for (size_t i = 0; i < st_nrows * st_ncols; ++i) {
    printf("%f ", st[i]);
  }
  printf("\n");

  // timestamp(s)
  printf("TIMESTAMPS:\n");
  printf("\tDimensions: %zu\n", ts_dims);
  printf("\tNum Rows: %zu\n", ts_nrows);

  printf("\t\t\tRaw Value(s): ");
  for (size_t i = 0; i < ts_nrows; ++i) {
    printf("%f ", ts[i]);
  }
  printf("\n");

  return;
}

void printMatrix(size_t nrows, size_t ncols, double *m) {
  for (size_t i = 0; i < nrows; ++i) {
    for (size_t j = 0; j < ncols; ++j) {
      printf(" %f", m[j + i * ncols]);
    }

    printf("\n");
  }
}
