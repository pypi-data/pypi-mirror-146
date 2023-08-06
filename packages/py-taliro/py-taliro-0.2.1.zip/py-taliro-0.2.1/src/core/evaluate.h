#ifndef TPTALIRO_CORE_EVALUATE_H
#define TPTALIRO_CORE_EVALUATE_H

#include <stddef.h>

#include "banned.h"

#define MAX_BUFFERSIZE 4096
#define UNUSED(x) (void)(x)

/* interfacing datastructure(s) */

/**
 * Represent a predicate constraint.
 *
 * @member name Predicate name as referenced within the spec
 * @member a_dims Dimensions of A matrix (must be two)
 * @member a_nrows Number of A matrix rows (constraints)
 * @member a_ncols Number of A matrix columns (system dimensions)
 * @member a Pointer to first location within A matrix
 * @member b_dims Dimensions of b matrix (must be two)
 * @member b_nrows Number of b matrix rows (constraints)
 * @member b_ncols Number of b matrix columns (system dimensions)
 * @member b Pointer to first location within b matrix
 */
typedef struct {
  char *name;

  size_t a_dims;
  size_t a_nrows;
  size_t a_ncols;
  double *a;

  size_t b_dims;
  size_t b_nrows;
  size_t b_ncols;
  double *b;

  size_t l_dims;
  size_t l_nrows;
  size_t l_ncols;
  double *l;
} Predicate;

typedef struct {
  size_t a_dims;
  size_t a_nrows;
  size_t a_ncols;
  double *a;

  size_t b_dims;
  size_t b_nrows;
  size_t b_ncols;
  double *b;
} Guard;

typedef struct {
  double dl;
  double ds;
} Evaluation;

/* forward declaration(s) */
Evaluation evaluate(char *, size_t, Predicate *, size_t, size_t, size_t,
                    double *, size_t, size_t, double *, size_t, double *,
                    size_t, size_t, size_t, double *, size_t, size_t, size_t,
                    Guard *);

double *shortest_paths(size_t, const double *);
double *pred_paths(size_t, Predicate *, size_t, double *);

size_t get_num_neighbors(size_t, size_t, const double *);
double *get_neighbors(size_t, size_t, size_t, const double *);

void printEvaluatePredicate(Predicate, size_t);
void printEvaluateInputs(char *, size_t, Predicate *, size_t, size_t, size_t,
                         double *, size_t, size_t, double *);
void printMatrix(size_t, size_t, double *);

#endif
