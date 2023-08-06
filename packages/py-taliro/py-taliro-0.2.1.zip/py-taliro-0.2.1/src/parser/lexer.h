#ifndef TPTALIRO_PARSER_LEXER_H
#define TPTALIRO_PARSER_LEXER_H

#include <ctype.h>

#include "banned.h"
#include "core/ltl2tree.h"

#define Token(y)                                  \
  miscell->tl_yylval = tl_nn(y, ZN, ZN, miscell); \
  return y
#define MetricToken(y)                            \
  miscell->tl_yylval = tl_nn(y, ZN, ZN, miscell); \
  miscell->tl_yylval->time = miscell->TimeCon;    \
  return y

static int follow(int, int, int, int *, size_t, char *, int *, Miscellaneous *);
static void getword(int, int (*tst)(int), int *, size_t, char *,
                    Miscellaneous *);
static void mtl_con(int *, size_t, char *, Miscellaneous *, int *);
static int mtl_follow(int, int, int, int *, size_t, char *, Miscellaneous *,
                      int *);
static int tl_lex(int *, size_t, char *, Miscellaneous *, int *);

Interval getbounds(int *, size_t, char *, Miscellaneous *, int *);
Number getnumber(char, int *, size_t, char *, int *, Miscellaneous *);
Symbol *getsym(Symbol *);
int hash(char *);
void tl_clearlookup(char *, Miscellaneous *);
Symbol *tl_lookup(char *, Miscellaneous *);
int tl_yylex(int *, size_t, char *, Miscellaneous *, int *);

/* inline function(s) */
int isalnum_(int c) { return (isalnum(c) || c == '_'); }

#endif
