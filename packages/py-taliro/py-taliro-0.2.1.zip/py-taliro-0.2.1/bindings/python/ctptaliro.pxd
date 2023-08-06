cdef extern from "core/ltl2tree.h":
    cdef int LTL_ERROR

cdef extern from "core/evaluate.h":
    ctypedef struct Predicate:
        char *name

        size_t a_dims
        size_t a_nrows
        size_t a_ncols
        double *a

        size_t b_dims
        size_t b_nrows
        size_t b_ncols
        double *b

        size_t l_dims
        size_t l_nrows
        size_t l_ncols
        double *l

    ctypedef struct Guard:
        size_t a_dims
        size_t a_nrows
        size_t a_ncols
        double *a

        size_t b_dims
        size_t b_nrows
        size_t b_ncols
        double *b

    ctypedef struct Evaluation:
        double dl;
        double ds;

    Evaluation evaluate(
        char *spec,
        size_t npreds, Predicate *preds,
        size_t st_dims, size_t st_nrows, size_t st_ncols, double *st,
        size_t ts_dims, size_t ts_nrows, double *ts,
        size_t lt_nrows, double *lt,
        size_t am_dims, size_t am_nrows, size_t am_ncols, double *am,
        size_t gm_dims, size_t gm_nrows, size_t gm_ncols, Guard *gm
    )
