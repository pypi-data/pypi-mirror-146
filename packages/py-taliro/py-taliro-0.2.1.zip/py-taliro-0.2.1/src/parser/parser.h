#ifndef TPTALIRO_PARSER_PARSER_H
#define TPTALIRO_PARSER_PARSER_H

#include <stddef.h>

#include "banned.h"
#include "core/ltl2tree.h"

static int implies(Node *, Node *, int *, char *, int *, Miscellaneous *);
static Node *bin_simpler(Node *, Miscellaneous *, int *, char *, int *);
static Node *bin_minimal(Node *, Miscellaneous *, int *, char *, int *);
static Node *tl_factor(int *, size_t, char *, Miscellaneous *, int *);
static Node *tl_level(int, int *, size_t, char *, Miscellaneous *, int *);
static Node *tl_formula(int *, size_t, char *, Miscellaneous *, int *);

Node *tl_parse(int *, size_t, char *, Miscellaneous *, int *);

#endif
