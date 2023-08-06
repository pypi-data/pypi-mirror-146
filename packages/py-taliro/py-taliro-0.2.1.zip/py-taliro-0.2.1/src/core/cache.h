#ifndef TPTALIRO_CORE_CACHE_H
#define TPTALIRO_CORE_CACHE_H

#include "banned.h"
#include "core/ltl2tree.h"

Node *cached(Node *, Miscellaneous *, int *, char *, int *);
Node *in_cache(Node *, int *, char *, int *, Miscellaneous *);

Node *dupnode(Node *);
Node *getnode(Node *);
Node *tl_nn(int, Node *, Node *, Miscellaneous *);
void releasenode(int, Node *);

int all_lfts(int, Node *, Node *, int *, char *, int *, Miscellaneous *);
int one_lft(int, Node *, Node *, int *, char *, int *, Miscellaneous *);

int isequal(Node *, Node *, int *, char *, int *, Miscellaneous *);
int sameform(Node *, Node *, int *, char *, int *, Miscellaneous *);
int sametrees(int, Node *, Node *, int *, char *, int *, Miscellaneous *);

int any_and(Node *, Node *, int *, char *, int *, Miscellaneous *);
int any_lor(Node *, Node *, int *, char *, int *, Miscellaneous *);
int any_term(Node *, Node *, int *, char *, int *, Miscellaneous *);
int anywhere(int, Node *, Node *, int *, char *, int *, Miscellaneous *);

#endif
