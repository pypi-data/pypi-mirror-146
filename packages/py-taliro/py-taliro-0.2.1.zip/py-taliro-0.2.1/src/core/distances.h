#ifndef TPTALIRO_CORE_DISTANCES_H
#define TPTALIRO_CORE_DISTANCES_H

#include <stdbool.h>
#include <stddef.h>

#include "banned.h"

#define dmin(a, b) (((a) < (b)) ? (a) : (b))
#define MIN_DIM 100
#define NullSet (ConvSet *)0

/**
 * Convex Set representation.
 *
 * The convex set represents a convex area that...
 *
 * @member Dim Set type of set (0: 1D, else: 1+D).
 * @member idx Predicate map index.
 * @member proj Project dimensions in a higher-dimension space.
 * @member nproj The number of project components.
 * @member loc Locations in the Hybrid Automata (HA).
 * @member nloc Number of locations in HA (0: any location).
 * @member isSetRn If true, $R^{n}$ (indicated by an empty A as input).
 * @member ncon Total number of constraints.
 * @member A The A constraint matrix part in Ax <= b.
 * @member b The b constraint matrix part in Ax <= b.
 * @member lb Lower bound of interval: "{", "[", or "(".
 * @member ub Upper bound of interval: "}", "]", or ")".
 * @member lbcl Inclusivity of lower bound (0: exclusive, else: inclusive).
 * @member upcl Inclusivity of upper bound (0: exclusive, else: inclusive). */
typedef struct {
  int Dim;
  int idx;
  int *proj;
  int nproj;
  double *loc;
  int nloc;

  bool isSetRn;
  int ncon;
  double **A;
  double *b;

  double lb;
  double ub;
  int lbcl;
  int ubcl;
} ConvSet;

/**
 * Convex Set for guard sets.
 *
 * The convex set for guard sets captures...
 *
 * @member nset The number of sets.
 * @member ncon The number of constraints.
 * @member A The A constraint matrix part in Ax <= b.
 * @member b The b constraint matrix part in Ax <= b.
 * @member proj The set of projected dimensions in a higher-dim space.
 * @member nproj The number of projected components. */
typedef struct {
  int nset;
  int *ncon;
  double ***A;
  double **b;

  int *proj;
  int nproj;
} GuardSet;

/**
 * The Distance Computation Data representation.
 *
 * The distance computation data serves to capture...
 *
 * @member LDist The distance between the control location and the predicate
 * locations on the hybrid automaton graph.
 * @member GuardMap The maps for the guard sets.
 * @member AdjL The adjacency list for control locations.
 * @member AdjLNell The number of neighbors of each control location. */
typedef struct {
  double *LDist;
  GuardSet **GuardMap;
  double **AdjL;
  size_t *AdjLNell;
} DistCompData;

/**
 * Hybrid Distance representation.
 *
 * The hybrid distance serves to represent the robustness
 * of the Hybrid Automaton.
 *
 * @member dl
 * @member ds
 * @member iteration The most related iteration.
 * @member preindex The most related predicate index. */
typedef struct {
  double dl;
  double ds;
  int iteration;
  int preindex;
} HyDis;

HyDis SignedHDist0(double *, ConvSet *, int, double *, size_t);
HyDis SignedHDistG(double *, ConvSet *, int, DistCompData *, size_t);
double SignedDist(double *, ConvSet *, int);

int isPointInConvSet(double *, ConvSet *, int);

double inner_prod(const double *, const double *, int);
double norm(const double *, int);

void vec_add(double *, const double *, const double *, int);
void vec_scl(double *, double, const double *, int);

#endif
