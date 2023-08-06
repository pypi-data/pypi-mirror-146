#ifndef TPTALIRO_CORE_REWRT_H
#define TPTALIRO_CORE_REWRT_H

#include "banned.h"
#include "core/ltl2tree.h"

#define BUFF_LEN 4096

static void addcan(int, Node *, Miscellaneous *);
static void marknode(int, Node *);

Node *right_linked(Node *n);
Node *canonical(Node *, Miscellaneous *, int *, char *, int *);
Node *push_negation(Node *, Miscellaneous *, int *, char *, int *);
Node *switchNotTempOper(Node *, int, Miscellaneous *, int *, char *, int *);

Node *Canonical(Node *, Miscellaneous *, int *, char *, int *);

#endif
