from typing import Dict, List

import numpy as np
cimport numpy as np
from libc.stdlib cimport malloc, free

from ctptaliro cimport Predicate as cPredicate, Guard as cGuard, evaluate, LTL_ERROR

class ParserError(Exception):
    pass

def tptaliro(spec: str, preds, st, ts, lt=None, adj_list=None, guards=None):
    """Compute robustness using TP-TaLiRo.
    """

    # SPECIFICATION SETUP
    cy_spec = spec.encode("utf-8")


    # PREDICATE SETUP
    npreds = len(preds)
    cdef cPredicate *pmap = <cPredicate *>malloc(<size_t>npreds * sizeof(cPredicate))

    pnames = [] # ref list of predicate names
    for i in range(npreds):
        # name
        pnames.append(preds[i]["name"].encode("utf-8"))
        pmap[i].name = pnames[i]

        # A matrix
        pmap[i].a_dims = <size_t>(preds[i]["a"]).ndim
        pmap[i].a_nrows = <size_t>((preds[i]["a"]).shape)[0]
        pmap[i].a_ncols = <size_t>((preds[i]["a"]).shape)[1]

        pmap[i].a = <double *>malloc(<size_t>(preds[i]["a"]).size * sizeof(double))
        a_cont = np.ascontiguousarray(preds[i]["a"], dtype=np.double)

        for ii in range((preds[i]["a"].shape)[0]):
            for iii in range((preds[i]["a"].shape)[1]):
                (pmap[i].a)[ii + iii * pmap[i].a_nrows] = a_cont[ii][iii]

        # b matrix
        pmap[i].b_dims = <size_t>(preds[i]["b"]).ndim
        pmap[i].b_nrows = <size_t>((preds[i]["b"]).shape)[0]
        pmap[i].b_ncols = <size_t>((preds[i]["b"]).shape)[1]

        pmap[i].b = <double *>malloc(<size_t>(preds[i]["b"]).size * sizeof(double))
        b_cont = np.ascontiguousarray(preds[i]["b"], dtype=np.double)

        for ii in range((preds[i]["b"].shape)[0]):
            for iii in range((preds[i]["b"].shape)[1]):
                (pmap[i].b)[ii + iii * pmap[i].b_nrows] = b_cont[ii][iii]

        # location(s)
        if "l" in preds[i]:
            # location(s) exist
            pmap[i].l_dims = <size_t>(preds[i]["l"]).ndim
            pmap[i].l_nrows = <size_t>((preds[i]["l"]).shape)[0]
            pmap[i].l_ncols = <size_t>((preds[i]["l"]).shape)[1]

            pmap[i].l = <double *>malloc(<size_t>(preds[i]["l"]).size * sizeof(double))
            l_cont = np.ascontiguousarray(preds[i]["l"], dtype=np.double)

            for ii in range((preds[i]["l"].shape)[0]):
                for iii in range((preds[i]["l"].shape)[1]):
                    (pmap[i].l)[ii + iii * pmap[i].l_nrows] = l_cont[ii][iii]
        else:
            # no location(s) exist
            pmap[i].l_dims = 0
            pmap[i].l_nrows = 0
            pmap[i].l_ncols = 0

            pmap[i].l = NULL


    # STATE TRACE SETUP
    cy_st = <double *>malloc(<size_t>(st.size) * sizeof(double))
    st_cont = np.ascontiguousarray(st, dtype=np.double)

    for i in range((st.shape)[0]):
        for ii in range((st.shape)[1]):
            cy_st[i + ii * (st.shape)[0]] = st_cont[i][ii]


    # TIMESTAMP SETUP
    cy_ts = <double *>malloc(<size_t>(ts.size) * sizeof(double))
    ts_cont = np.ascontiguousarray(ts, dtype=np.double)

    for i in range((ts.shape)[0]):
        for ii in range((ts.shape)[1]):
            cy_ts[i + ii * (ts.shape)[0]] = ts_cont[i][ii]


    # LOCATION TRACE SETUP
    cdef double *cy_lt = NULL

    if lt is not None:
        cy_lt = <double *>malloc(<size_t>(lt.size) * sizeof(double))
        lt_cont = np.ascontiguousarray(lt, dtype=np.double)

        for i in range((lt.shape)[0]):
            for ii in range((lt.shape)[1]):
                cy_lt[i + ii * (lt.shape)[0]] = lt_cont[i][ii]
    else:
        lt = np.empty((0, 0))


    # ADJACENCY MATRIX SETUP
    cdef double *cy_adj_matrix = NULL

    if adj_list is not None:
        adj_matrix = to_matrix(adj_list)
        cy_adj_matrix = <double *>malloc(<size_t>(adj_matrix.size) * sizeof(double))
        adj_matrix_cont = np.ascontiguousarray(adj_matrix, dtype=np.double)

        for i in range((adj_matrix.shape)[0]):
            for ii in range((adj_matrix.shape)[1]):
                cy_adj_matrix[i + ii * (adj_matrix.shape)[0]] = adj_matrix_cont[i][ii]
    else:
        adj_matrix = np.empty((0, 0))


    # GUARD MAP SETUP
    cdef cGuard *cy_gm = NULL
    gm_prop = None

    if guards is not None:
        gm_prop = np.empty((len(adj_list.keys()), len(adj_list.keys())))
        cy_gm = <cGuard *>malloc(<size_t>(gm_prop.size) * sizeof(cGuard));

        # initialize guard map
        for i in range(gm_prop.size):
            cy_gm[i].a_dims = 2
            cy_gm[i].a_nrows = 0
            cy_gm[i].a_ncols = 0
            cy_gm[i].a = NULL

            cy_gm[i].b_dims = 2
            cy_gm[i].b_nrows = 0
            cy_gm[i].b_ncols = 0
            cy_gm[i].b = NULL

        for guard, constraint in guards.items():
            index = map_guard(guard, adj_list)

            # A matrix
            cy_gm[index].a_dims = <size_t>constraint["a"].ndim
            cy_gm[index].a_nrows = <size_t>constraint["a"].shape[0]
            cy_gm[index].a_ncols = <size_t>constraint["a"].shape[1]

            cy_gm[index].a = <double *>malloc(<size_t>(constraint["a"]).size * sizeof(double))
            a_cont = np.ascontiguousarray(constraint["a"], dtype=np.double)

            for ii in range((constraint["a"].shape)[0]):
                for iii in range((constraint["a"].shape)[1]):
                    (cy_gm[index].a)[ii + iii * cy_gm[index].a_nrows] = a_cont[ii][iii]

            # b matrix
            cy_gm[index].b_dims = <size_t>constraint["b"].ndim
            cy_gm[index].b_nrows = <size_t>constraint["b"].shape[0]
            cy_gm[index].b_ncols = <size_t>constraint["b"].shape[1]

            cy_gm[index].b = <double *>malloc(<size_t>(constraint["b"]).size * sizeof(double))
            b_cont = np.ascontiguousarray(constraint["b"], dtype=np.double)

            for ii in range((constraint["b"].shape)[0]):
                for iii in range((constraint["b"].shape)[1]):
                    (cy_gm[index].b)[ii + iii * cy_gm[index].b_nrows] = b_cont[ii][iii]
    else:
        gm_prop = np.empty((0, 0))

    # COMPUTE ROBUSTNESS
    eval =  evaluate(
        cy_spec,
        npreds, pmap,
        st.ndim, st.shape[1], st.shape[0], cy_st,
        ts.ndim, ts.shape[1], cy_ts,
        lt.ndim, cy_lt,
        adj_matrix.ndim, adj_matrix.shape[1], adj_matrix.shape[0], cy_adj_matrix,
        gm_prop.ndim, gm_prop.shape[1], gm_prop.shape[0], cy_gm
    )

    # MEMORY DEALLOCATION
    free(cy_ts)
    free(cy_st)

    for i in range(npreds):
        free(pmap[i].b)
        free(pmap[i].a)

        if pmap[i].l != NULL:
            free(pmap[i].l)

    free(pmap)

    if LTL_ERROR:
        raise ParserError("Could not parse formula")

    return eval


def map_guard(guard, adj_list):
    """Return the index of the guard position.
    """

    locations = list(adj_list.keys())
    return locations.index(guard[1]) + locations.index(guard[0]) * len(locations)


def to_matrix(adj_list: Dict[str, List[str]]):
    """Convert an adjacency list into an equivalent matrix.
    """

    locations = list(adj_list.keys())

    # verify set of neighbors match set of locations
    all_neighbors = [location for neighbors in adj_list.values() for location in neighbors]

    if not set(all_neighbors).issubset(set(locations)):
        raise RuntimeError("set of neighbors does not match set of locations")

    # initialize adjacency matrix to INF
    matrix = np.full(
        shape=(len(locations), len(locations)),
        fill_value=np.inf
    )

    # convert to matrix
    for location, neighbors in adj_list.items():
        row = locations.index(location)

        for neighbor in neighbors:
            col = locations.index(neighbor)

            matrix[row, col] = 1

    # distance to self is zero, always
    for i in range(len(locations)):
        matrix[i, i] = 0

    return matrix

