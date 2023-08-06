#ifndef TPTALIRO_CORE_CDP_H
#define TPTALIRO_CORE_CDP_H

#include "banned.h"
#include "core/distances.h"  // DistCompData, HyDis
#include "core/ltl2tree.h"   // FWTaliroParam, Miscellaneous, Node, PMap

/* forward declaration(s) */
HyDis cdp(Node *, PMap *, const double *, const double *, const double *,
          DistCompData *, FWTaliroParam *, Miscellaneous *);

#endif
