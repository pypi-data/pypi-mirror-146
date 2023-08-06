#include "core/cdistances.h"

#include <math.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

#include "banned.h"
#include "core/distances.h"  // ConvSet, HyDis, inner_prod(), isPointInConvSet(), #MIN_DIM, norm(), vec_scl
#include "core/param.h"  // max

/**
 * Compute the resulting distance from the convex
 * set and trace data.
 *
 * @param trace State traces
 * @param ConvSet Convex set representing a constraint
 * @param dims System dimensions (i.e. number of columns in `trace`)
 *
 * @return Distance computation of convex set
 */
double csigned_dist(double *trace, ConvSet *cs, int dims) {
  // DISTANCE COMPUTATION
  if (cs->isSetRn) {
    return INFINITY;
  } else {
    double dist;

    if (dims == 1) {
      dist = fabs(cs->b[0] / cs->A[0][0] - trace[0]);

      if (cs->ncon == 2) {
        dist = dmin(dist, fabs(cs->b[1] / cs->A[1][0] - trace[0]));
      }

      if (isPointInConvSet(trace, cs, dims)) {
        return dist;
      } else {
        return -dist;
      }
    } else {
      if (cs->ncon == 1) {
        // single constraint, multi-dimensional trace
        double a, b;

        if (dims < MIN_DIM) {
          double x0[MIN_DIM];

          if (cs->nproj == 0) {
            a = norm(cs->A[0], dims);
            a = a * a;

            b = ((cs->b[0]) - inner_prod(cs->A[0], trace, dims)) / a;
            vec_scl(x0, b, cs->A[0], dims);

            dist = norm(x0, dims);

            if (isPointInConvSet(trace, cs, dims)) {
              return dist;
            } else {
              return -dist;
            }
          } else {
            // projection setup
            double *trace_prj = malloc(sizeof(double) * cs->nproj);

            // copy content(s)
            for (int i = 0; i < cs->nproj; ++i) {
              trace_prj[i] = trace[cs->proj[i] - 1];
            }

            a = norm(cs->A[0], cs->nproj);
            a = a * a;

            b = ((cs->b[0]) - inner_prod(cs->A[0], trace_prj, cs->nproj)) / a;
            vec_scl(x0, b, cs->A[0], cs->nproj);

            dist = norm(x0, cs->nproj);

            if (!isPointInConvSet(trace_prj, cs, cs->nproj)) {
              dist = -dist;
            }

            free(trace_prj);
            return dist;
          }
        } else {
          double *x0 = malloc(sizeof(double) * dims);

          a = norm(cs->A[0], dims);
          a = a * a;

          b = ((cs->b[0]) - inner_prod(cs->A[0], trace, dims)) / a;
          vec_scl(x0, b, cs->A[0], dims);

          dist = norm(x0, dims);

          if (!isPointInConvSet(trace, cs, dims)) {
            dist = -dist;
          }

          free(x0);
          return dist;
        }
      } else {
        // TODO:
        //   - Implement multiple constraints with multi-dimensional traces

        fprintf(stderr,
                "error(cdistances): unable to compute robustness for "
                "multi-constraint, multi-trace system (-INF)\n");

        return -INFINITY;
      }
    }
  }
}

HyDis csigned_distzero(double *trace, ConvSet *cs, int dims, double *ldist,
                       size_t nloc) {
  bool in_loc = false;

  for (int i = 0; i < cs->nloc; ++i) {
    if (((int)trace[dims]) == ((int)cs->loc[i])) {
      in_loc = true;
      break;
    }
  }

  // COMPUTE HYBRID DISTANCE
  HyDis hdist;

  if (in_loc) {
    hdist.dl = 0;
    hdist.ds = csigned_dist(trace, cs, dims);
  } else {
    hdist.dl = -(int)ldist[((int)trace[dims] - 1) + (int)cs->idx * nloc];
    hdist.ds = -INFINITY;
  }

  return hdist;
}

HyDis csigned_hdistg(double *trace, ConvSet *cs, int dims, DistCompData *dists,
                     size_t nloc) {
  // TODO:
  //   - Ensure all locations are positive integers

  int location = (int)trace[dims];
  bool in_location = false;

  for (int i = 0; i < cs->nloc; ++i) {
    if (location == (int)cs->loc[i]) {
      in_location = true;
      break;
    }
  }

  // COMPUTE HYBRID DISTANCE CONSIDERING GUARDS
  HyDis hdist;

  if (in_location) {
    hdist.dl = 0;
    hdist.ds = csigned_dist(trace, cs, dims);
  } else {
    int pdist = (int)dists->LDist[(location - 1) + (int)cs->idx * nloc];

    hdist.dl = -pdist;
    hdist.ds = -INFINITY;

    if (dists->AdjLNell[location - 1] > 0) {
      for (size_t i = 0; i < dists->AdjLNell[location - 1]; ++i) {
        // TODO:
        //   - Implement projection

        size_t index = dists->AdjL[location - 1][i] - 1;

        if ((int)dists->LDist[index + (int)cs->idx * nloc] < pdist) {
          double dist = -INFINITY;
          ConvSet gs;

          for (int j = 0; j < dists->GuardMap[location - 1][i].nset; ++j) {
            gs.ncon = dists->GuardMap[location - 1][i].ncon[j];
            gs.isSetRn = false;

            // A and b matrix
            gs.A = dists->GuardMap[location - 1][i].A[j];
            gs.b = dists->GuardMap[location - 1][i].b[j];

            // projections
            gs.nproj = dists->GuardMap[location - 1][i].nproj;

            // TODO:
            //   - Implement multiple constraints computation

            dist = csigned_dist(trace, &gs, dims);  // temporary (default)

            if (dist > 0) {
              dist = 0.0;
            }

            dist = max(-INFINITY, dist);
          }

          if (dist > hdist.ds) {
            hdist.ds = dist;
          }
        }
      }
    }
  }

  return hdist;
}
