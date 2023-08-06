#ifndef TPTALIRO_CORE_LTL2TREE_H
#define TPTALIRO_CORE_LTL2TREE_H

#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#include "banned.h"
#include "core/distances.h"

#define NullSymbol (Symbol *)0
#define YYSTYPE Nodeptr
#define Nhash 255

#define ZN (Node *)0
#define ZS (Symbol *)0

#define True tl_nn(TRUE, ZN, ZN, miscell)
#define False tl_nn(FALSE, ZN, ZN, miscell)
#define Not(a) \
  push_negation(tl_nn(NOT, a, ZN, miscell), miscell, cnt, uform, tl_yychar)
#define rewrite(n) canonical(right_linked(n), miscell, cnt, uform, tl_yychar)

#define Debug(x)      \
  {                   \
    if (0) printf(x); \
  }
#define Debug2(x, y)              \
  {                               \
    if (tl_verbose) printf(x, y); \
  }
#define Dump(x)              \
  {                          \
    if (0) dump(x, miscell); \
  }
#define Explain(x)                 \
  {                                \
    if (tl_verbose) tl_explain(x); \
  }
#define Assert(x, y)                                                  \
  {                                                                   \
    if (!(x)) {                                                       \
      tl_explain(y);                                                  \
      Fatal(": assertion failed\n", (char *)0, cnt, uform, tl_yychar, \
            miscell);                                                 \
    }                                                                 \
  }

#define min(a, b) (((a) < (b)) ? (a) : (b))

typedef struct Symbol {
  char *name;
  ConvSet *set;
  struct Symbol *next; /* linked list, symbol table */
  int index;
  bool Normalized; /* GF: If set to true, then the valuation of the predicate is
                      normalized to range [-1,1] */
  double *NormBounds; /* GF: min and max interval for normalization */
} Symbol;

typedef struct {
  int LTL;           /* Is this an LTL formula */
  int ConOnSamples;  /* Are the constraints on the actual time or the # of
                        samples? */
  size_t SysDim;     /* System dimension */
  size_t nSamp;      /* Number of Samples */
  size_t nPred;      /* Number of Predicates */
  size_t true_nPred; /* Number of Predicates */
  size_t tnLoc;      /* total number of control locations */
  int nInp;          /* Number of inputs to mx_dp_taliro */
  int ParON;         /* Indicator if parameter is used */

  int nCLG;          /* Number HAs in multiple H.A.s*/
  size_t *tnLocNCLG; /* total number of control locations for each HA in
                        multiple H.A.s*/

  int TPTL; /* Is this an TPTL formula */
} FWTaliroParam;

typedef struct queue {
  int i;
  struct Node *first;
  struct Node *last;
} queue;

typedef union {
  struct {
    int inf;
  } num;
  struct {
    int inf;
    double f_num;
  } numf;
  struct {
    int inf;
    int i_num;
  } numi;
} Number;

typedef struct {
  Number lbd;
  int l_closed;
  Number ubd;
  int u_closed;
} Interval;

typedef struct Node {
  short ntyp; /* node type */
  int visited;
  int index;
  int LBound;
  int UBound;
  int LBound_nxt;
  int BoundCheck;
  int UBindicator;
  int LBindicator;
  int LBindicator_nxt;
  int loop_end;
  HyDis rob;     /* robustness */
  HyDis rob_sec; /* robustness_last */
  Interval time; /* lower and upper real time bounds */
  struct Symbol *sym;
  struct Node *lft; /* tree */
  struct Node *rgt; /* tree */
  struct Node *nxt; /* if linked list */
  Number value;
  /* for TPTL monitor */
  int Lindex;
  int Rindex;
  int group;
} Node;

enum {
  ALWAYS = 257,
  AND,        /* 258 */
  EQUIV,      /* 259 */
  EVENTUALLY, /* 260 */
  FALSE,      /* 261 */
  IMPLIES,    /* 262 */
  NOT,        /* 263 */
  OR,         /* 264 */
  PREDICATE,  /* 265 */
  TRUE,       /* 266 */
  U_OPER,     /* 267 */
  V_OPER,     /* 268 */
  NEXT,       /* 269 */
  VALUE,      /* 270 */
  WEAKNEXT,   /* 271 */
  U_MOD,      /* 272 */
  V_MOD,      /* 273 */
  FREEZE_AT,  /* 274 */
  CONSTR_LE,  /* 275 */
  CONSTR_LS,  /* 276 */
  CONSTR_EQ,  /* 277 */
  CONSTR_GE,  /* 278 */
  CONSTR_GR,  /* 279 */
  CONSTRAINT, /* 280 */
  POSITIVE_POLAR = 1,
  NEGATIVE_POLAR = -1,
  MIXED_POLAR = 0,
  UNDEFINED_POLAR = 2,
  PRED = 1,
  PAR = 2,
  PREDPAR = 3
};

typedef Node *Nodeptr;

typedef struct Cache {
  Node *before;
  Node *after;
  int same;
  struct Cache *nxt;
} Cache;

typedef struct PMap {
  char *str;
  ConvSet set;
  bool true_pred;
  double *Range;
  /* GF: If set to true, then the valuation of the predicate is normalized to
   * range [-1,1] */
  bool Normalized;
  /* GF: max value for normalization, e.g., if NormBounds = 2.5, then it is
   * expected that the robustness */
  /* should be in the interval [-2.5,2.5]. Thus, the robustness value will be
   * mapped to the interval [-1,1]. */
  /* For hybrid distances the 2nd element is the maximum path distance on the
   * graph  */
  double *NormBounds;
} PMap;

typedef struct ParMap {
  char *str;
  double *value;
  int index;
  double *Range;
  bool lbd;
  int type;
  bool with_value;
  /* GF: If set to true, then the valuation of the predicate is normalized to
   * range [-1,1] */
  bool Normalized;
  /* GF: max value for normalization, e.g., if NormBounds = 2.5, then it is
   * expected that the robustness */
  /* should be in the interval [-2.5,2.5]. Thus, the robustness value will be
   * mapped to the interval [-1,1]. */
  /* For hybrid distances the 3rd element is the maximum path distance on the
   * graph  */
  double *NormBounds;
} ParMap;

typedef struct {
  /* Peer reviewed on 2013.07.22 by Dokhanchi, Adel */
  int *pindex;
  size_t total;
  int used;
} PredList;

typedef struct {
  int polar;
} Polarity;

typedef struct {
  Number zero;
  Number inf;
  Interval zero2inf;
  Interval emptyInter;
  Interval TimeCon;
  YYSTYPE tl_yylval;
  FWTaliroParam dp_taliro_param;
  int tl_errs;
  FILE *tl_out;
  char yytext[2048];
  Symbol *symtab[Nhash + 1];
  ParMap *parMap;
  PMap *predMap;
  PredList pList;
  bool lbd;
  int type_temp;
} Miscellaneous;

Node *Canonical(Node *, Miscellaneous *, int *, char *, int *);
Node *canonical(Node *, Miscellaneous *, int *, char *, int *);
Node *getnode(Node *);
Node *push_negation(Node *, Miscellaneous *, int *, char *, int *);
Node *switchNotTempOper(Node *n, int ntyp, Miscellaneous *, int *cnt,
                        char *uform, int *tl_yychar);
Node *right_linked(Node *);
Node *tl_nn(int, Node *, Node *, Miscellaneous *);

Symbol *tl_lookup(char *, Miscellaneous *miscell);
void tl_clearlookup(char *, Miscellaneous *miscell);
Symbol *getsym(Symbol *);
Symbol *DoDump(Node *, char *, Miscellaneous *miscell);

void *emalloc(size_t);

int anywhere(int, Node *, Node *, int *, char *, int *, Miscellaneous *);
int dump_cond(Node *, Node *, int);
int isequal(Node *, Node *, int *, char *, int *, Miscellaneous *);
int tl_Getchar(int *cnt, size_t hasuform, const char *uform);

void dump(Node *, Miscellaneous *);
void Fatal(char *, char *, int *, char *, int *, Miscellaneous *);
void fatal(char *, char *, int *, char *, int *, Miscellaneous *);
void fsm_print(void);
void releasenode(int, Node *);
void tl_explain(int);
void tl_UnGetchar(int *cnt);
Node *tl_parse(int *cnt, size_t hasuform, char *uform, Miscellaneous *miscell,
               int *);
void tl_yyerror(char *s1, int *cnt, char *uform, int *, Miscellaneous *);
void trans(Node *);

int tl_yylex(int *cnt, size_t hasuform, char *uform, Miscellaneous *miscell,
             int *tl_yychar);
void fatal(char *, char *, int *, char *, int *, Miscellaneous *);
void put_uform(char *uform, Miscellaneous *);
void tl_exit(int i);

extern int LTL_ERROR;

#endif
