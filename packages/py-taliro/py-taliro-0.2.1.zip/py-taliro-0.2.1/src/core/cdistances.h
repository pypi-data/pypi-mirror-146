#ifndef TPTALIRO_CORE_CDISTANCES_H
#define TPTALIRO_CORE_CDISTANCES_H

#include "banned.h"
#include "core/distances.h"  // ConvSet

/* forward declaration(s) */
double csigned_dist(double *, ConvSet *, int);

HyDis csigned_distzero(double *, ConvSet *, int, double *, size_t);
HyDis csigned_hdistg(double *, ConvSet *, int, DistCompData *, size_t);

#endif
