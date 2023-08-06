#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "banned.h"
#include "core/distances.h"
#include "core/evaluate.h"
#include "core/ltl2tree.h"
#include "core/param.h"

#define BUFF_LEN 4096

int LTL_ERROR = 0;

void *emalloc(size_t n) {
  void *tmp;

  if (!(tmp = (void *)calloc(n, 1))) {
    fprintf(stderr, "mx_tp_taliro: not enough memory!");
  }

  return tmp;
}

int tl_Getchar(int *cnt, size_t hasuform, const char *uform) {
  if (*cnt < (int)hasuform) return uform[(*cnt)++];
  (*cnt)++;
  return -1;
}

void tl_UnGetchar(int *cnt) {
  if (*cnt > 0) (*cnt)--;
}

#define Binop(a)                 \
  fprintf(miscell->tl_out, "("); \
  dump(n->lft, miscell);         \
  fprintf(miscell->tl_out, a);   \
  dump(n->rgt, miscell);         \
  fprintf(miscell->tl_out, ")")

static void sdump(Node *n, char *dumpbuf) {
  switch (n->ntyp) {
    case PREDICATE:
      snprintf(dumpbuf + strlen(dumpbuf), strlen(n->sym->name) + 1, "%s",
               n->sym->name);
      break;
    case U_OPER:
      snprintf(dumpbuf + strlen(dumpbuf), strlen("U") + 1, "%s", "U");
      goto common2;
    case V_OPER:
      snprintf(dumpbuf + strlen(dumpbuf), strlen("V") + 1, "%s", "V");
      goto common2;
    case OR:
      snprintf(dumpbuf + strlen(dumpbuf), strlen("|") + 1, "%s", "|");
      goto common2;
    case AND:
      snprintf(dumpbuf + strlen(dumpbuf), strlen("&") + 1, "%s", "&");
    common2:
      sdump(n->rgt, dumpbuf);
    common1:
      sdump(n->lft, dumpbuf);
      break;
    case NEXT:
      snprintf(dumpbuf + strlen(dumpbuf), strlen("X") + 1, "%s", "X");
      goto common1;
    case NOT:
      snprintf(dumpbuf + strlen(dumpbuf), strlen("!") + 1, "%s", "!");
      goto common1;
    case TRUE:
      snprintf(dumpbuf + strlen(dumpbuf), strlen("T") + 1, "%s", "T");
      break;
    case FALSE:
      snprintf(dumpbuf + strlen(dumpbuf), strlen("F") + 1, "%s", "F");
      break;
    default:
      snprintf(dumpbuf + strlen(dumpbuf), strlen("?") + 1, "%s", "?");
      break;
  }
}

Symbol *DoDump(Node *n, char *dumpbuf, Miscellaneous *miscell) {
  if (!n) return ZS;

  if (n->ntyp == PREDICATE) return n->sym;

  dumpbuf[0] = '\0';
  sdump(n, dumpbuf);
  return tl_lookup(dumpbuf, miscell);
}

void dump(Node *n, Miscellaneous *miscell) {
  if (!n) return;

  switch (n->ntyp) {
    case OR:
      Binop(" || ");
      break;
    case AND:
      Binop(" && ");
      break;
    case U_OPER:
      Binop(" U ");
      break;
    case V_OPER:
      Binop(" V ");
      break;
    case NEXT:
      fprintf(miscell->tl_out, "X");
      fprintf(miscell->tl_out, " (");
      dump(n->lft, miscell);
      fprintf(miscell->tl_out, ")");
      break;
    case NOT:
      fprintf(miscell->tl_out, "!");
      fprintf(miscell->tl_out, " (");
      dump(n->lft, miscell);
      fprintf(miscell->tl_out, ")");
      break;
    case FALSE:
      fprintf(miscell->tl_out, "false");
      break;
    case TRUE:
      fprintf(miscell->tl_out, "true");
      break;
    case PREDICATE:
      fprintf(miscell->tl_out, "(%s)", n->sym->name);
      break;
    case -1:
      fprintf(miscell->tl_out, " D ");
      break;
    default:
      printf("Unknown token: ");
      tl_explain(n->ntyp);
      break;
  }
}

void tl_explain(int n) {
  switch (n) {
    case ALWAYS:
      printf("[]");
      break;
    case EVENTUALLY:
      printf("<>");
      break;
    case IMPLIES:
      printf("->");
      break;
    case EQUIV:
      printf("<->");
      break;
    case PREDICATE:
      printf("predicate");
      break;
    case OR:
      printf("||");
      break;
    case AND:
      printf("&&");
      break;
    case NOT:
      printf("!");
      break;
    case U_OPER:
      printf("U");
      break;
    case V_OPER:
      printf("V");
      break;
    case NEXT:
      printf("X");
      break;
    case TRUE:
      printf("true");
      break;
    case FALSE:
      printf("false");
      break;
    case ';':
      printf("end of formula");
      break;
    default:
      printf("%c", n);
      break;
  }
}

static void non_fatal(char *s1, char *s2, const int *cnt, char *uform,
                      int *tl_yychar, Miscellaneous *miscell) {
  int i;

  printf("TaLiRo: ");
  if (s2)
    printf(s1, s2);
  else
    printf(s1);
  if ((*tl_yychar) != -1 && (*tl_yychar) != 0) {
    printf(", saw '");
    tl_explain((*tl_yychar));
    printf("'");
  }
  printf("\nTaLiRo: %s\n---------", uform);
  for (i = 0; i < (*cnt); i++) printf("-");
  printf("^\n");
  fflush(stdout);
  (miscell->tl_errs)++;
}

void tl_yyerror(char *s1, int *cnt, char *uform, int *tl_yychar,
                Miscellaneous *miscell) {
  LTL_ERROR = 1;
  Fatal(s1, (char *)0, cnt, uform, tl_yychar, miscell);
}

void Fatal(char *s1, char *s2, int *cnt, char *uform, int *tl_yychar,
           Miscellaneous *miscell) {
  non_fatal(s1, s2, cnt, uform, tl_yychar, miscell);
  tl_exit(0);
}

void fatal(char *s1, char *s2, int *cnt, char *uform, int *tl_yychar,
           Miscellaneous *miscell) {
  non_fatal(s1, s2, cnt, uform, tl_yychar, miscell);
  tl_exit(0);
}

void put_uform(char *uform, Miscellaneous *miscell) {
  fprintf(miscell->tl_out, "%s", uform);
}

void tl_exit(int i) {
  fprintf(stderr, "mx_tp_taliro(%d): unexpected error, tl_exit executed.", i);
}

/* used for visualizing TPTL formula tree */
void print2file(int *c, Node *n, FILE *f) {
  int i;
  if (!n) return;
  (*c)++;
  i = (*c);
  switch (n->ntyp) {
    case TRUE:
      fprintf(f, "  \"TRUE(%d)\"\n", i);
      break;
    case FALSE:
      fprintf(f, "  \"FALSE(%d)\"\n", i);
      break;
    case PREDICATE:
      fprintf(f, "  \"%s(%d)\"\n", n->sym->name, i);
      break;
    case NOT:
      fprintf(f, "  \"NOT(%d)\"\n", i);
      fprintf(f, "  \"NOT(%d)\" ->", i);
      print2file(c, n->lft, f);
      break;
    case AND:
      fprintf(f, "  \"AND(%d)\"\n", i);
      fprintf(f, "  \"AND(%d)\" ->", i);
      print2file(c, n->lft, f);
      fprintf(f, "  \"AND(%d)\" ->", i);
      print2file(c, n->rgt, f);
      break;
    case OR:
      fprintf(f, "  \"OR(%d)\"\n", i);
      fprintf(f, "  \"OR(%d)\" ->", i);
      print2file(c, n->lft, f);
      fprintf(f, "  \"OR(%d)\" ->", i);
      print2file(c, n->rgt, f);
      break;
    case IMPLIES:
      fprintf(f, "  \"IMPLIES(%d)\"\n", i);
      fprintf(f, "  \"IMPLIES(%d)\" ->", i);
      print2file(c, n->lft, f);
      fprintf(f, "  \"IMPLIES(%d)\" ->", i);
      print2file(c, n->rgt, f);
      break;
    case NEXT:
      fprintf(f, "  \"NEXT(%d)\"\n", i);
      fprintf(f, "  \"NEXT(%d)\" ->", i);
      print2file(c, n->lft, f);
      break;
    case WEAKNEXT:
      fprintf(f, "  \"WEAKNEXT(%d)\"\n", i);
      fprintf(f, "  \"WEAKNEXT(%d)\" ->", i);
      print2file(c, n->lft, f);
      break;
    case U_OPER:
      fprintf(f, "  \"U(%d)\"\n", i);
      fprintf(f, "  \"U(%d)\" ->", i);
      print2file(c, n->lft, f);
      fprintf(f, "  \"U(%d)\" ->", i);
      print2file(c, n->rgt, f);
      break;
    case V_OPER:
      fprintf(f, "  \"R(%d)\"\n", i);
      fprintf(f, "  \"R(%d)\" ->", i);
      print2file(c, n->lft, f);
      fprintf(f, "  \"R(%d)\" ->", i);
      print2file(c, n->rgt, f);
      break;
    case EVENTUALLY:
      fprintf(f, "  \"<>(%d)\"\n", i);
      fprintf(f, "  \"<>(%d)\" ->", i);
      print2file(c, n->rgt, f);
      break;
    case ALWAYS:
      fprintf(f, "  \"[](%d)\"\n", i);
      fprintf(f, "  \"[](%d)\" ->", i);
      print2file(c, n->rgt, f);
      break;
    case FREEZE_AT:
      fprintf(f, "  \"@ %s(%d)\"\n", n->sym->name, i);
      fprintf(f, "  \"@ %s(%d)\" ->", n->sym->name, i);
      print2file(c, n->lft, f);
      break;
    case CONSTR_LE:
      fprintf(f, "  \"%s <= %f (index=%d)\"\n", n->sym->name,
              n->value.numf.f_num, i);
      break;
    case CONSTR_LS:
      fprintf(f, "  \"%s < %f (index=%d)\"\n", n->sym->name,
              n->value.numf.f_num, i);
      break;
    case CONSTR_EQ:
      fprintf(f, "  \"%s == %f (index=%d)\"\n", n->sym->name,
              n->value.numf.f_num, i);
      break;
    case CONSTR_GE:
      fprintf(f, "  \"%s >= %f (index=%d)\"\n", n->sym->name,
              n->value.numf.f_num, i);
      break;
    case CONSTR_GR:
      fprintf(f, "  \"%s > %f (index=%d)\"\n", n->sym->name,
              n->value.numf.f_num, i);
      break;
    default:
      break;
  }
}

void countVar(int *c, Node *n, char *varName, int g) {
  if (!n) return;
  n->group = g;
  /*if(n->ntyp==FREEZE_AT)
      (*c)++;
      var=n->sym->name;
  else{ if(n->ntyp==FREEZE_AT)

  }*/

  switch (n->ntyp) {
    case FREEZE_AT:
      varName = n->sym->name;
      (*c)++;
      n->group = (*c);
      countVar(c, n->lft, varName, n->group);
      break;
    case CONSTR_LE:
      if (strcmp(varName, n->sym->name) != 0) {
        fprintf(stderr, "Time variable is not independent");
      }
      break;
    case CONSTR_LS:
      if (strcmp(varName, n->sym->name) != 0) {
        fprintf(stderr, "Time variable is not independent");
      }
      break;
    case CONSTR_EQ:
      if (strcmp(varName, n->sym->name) != 0) {
        fprintf(stderr, "Time variable is not independent");
      }
      break;
    case CONSTR_GE:
      if (strcmp(varName, n->sym->name) != 0) {
        fprintf(stderr, "Time variable is not independent");
      }
      break;
    case CONSTR_GR:
      if (strcmp(varName, n->sym->name) != 0) {
        fprintf(stderr, "Time variable is not independent");
      }
      break;
    case NOT:
      countVar(c, n->lft, varName, g);
      break;
    case AND:
      countVar(c, n->lft, varName, g);
      countVar(c, n->rgt, varName, g);
      break;
    case OR:
      countVar(c, n->lft, varName, g);
      countVar(c, n->rgt, varName, g);
      break;
    case IMPLIES:
      countVar(c, n->lft, varName, g);
      countVar(c, n->rgt, varName, g);
      break;
    case NEXT:
      countVar(c, n->lft, varName, g);
      break;
    case WEAKNEXT:
      countVar(c, n->lft, varName, g);
      break;
    case U_OPER:
      countVar(c, n->lft, varName, g);
      countVar(c, n->rgt, varName, g);
      break;
    case V_OPER:
      countVar(c, n->lft, varName, g);
      countVar(c, n->rgt, varName, g);
      break;
    case EVENTUALLY:
      countVar(c, n->rgt, varName, g);
      break;
    case ALWAYS:
      countVar(c, n->rgt, varName, g);
      break;
    default:
      break;
  }
}

/* void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[])
 * { */
/*   char buffer[4096]; */
/*   Predicate pmap[mxGetNumberOfElements(prhs[1])]; */

/*   // copy specification */
/*   mxGetString(prhs[0], buffer, mxGetDimensions(prhs[0])[1] + 1); */

/*   // setup predicate(s) */
/*   for (size_t i = 0; i < mxGetNumberOfElements(prhs[1]); ++i) { */
/*     // name */
/*     char tmp[4096]; */
/*     mxGetString(mxGetField(prhs[1], i, "str"), tmp,
 * mxGetDimensions(mxGetField(prhs[1], i, "str"))[1] + 1); */

/*     pmap[i].name = (char *)malloc(sizeof(char) * strlen(tmp) + 1); */

/*     if (strlen(tmp) > 4095) { */
/*       mexErrMsgTxt("error(mexFunction): requirement too long (MAX: 4096
 * characters)\n"); */
/*       exit(1); */
/*     } */

/*     strcpy(pmap[i].name, tmp); */

/*     // a matrix */
/*     pmap[i].a_dims = mxGetNumberOfDimensions(mxGetField(prhs[1], i, "A")); */
/*     pmap[i].a_nrows = mxGetDimensions(mxGetField(prhs[1], i, "A"))[0]; */
/*     pmap[i].a_ncols = mxGetDimensions(mxGetField(prhs[1], i, "A"))[1]; */
/*     pmap[i].a = mxGetPr(mxGetField(prhs[1], i, "A")); */

/*     // b matrix */
/*     pmap[i].b_dims = mxGetNumberOfDimensions(mxGetField(prhs[1], i, "b")); */
/*     pmap[i].b_nrows = mxGetDimensions(mxGetField(prhs[1], i, "b"))[0]; */
/*     pmap[i].b_ncols = mxGetDimensions(mxGetField(prhs[1], i, "b"))[1]; */
/*     pmap[i].b = mxGetPr(mxGetField(prhs[1], i, "b")); */
/*   } */

/*   evaluate(buffer, */
/*            mxGetNumberOfElements(prhs[1]), &pmap[0], */
/*            mxGetNumberOfDimensions(prhs[2]), */
/*            mxGetDimensions(prhs[2])[0], */
/*            mxGetDimensions(prhs[2])[1], */
/*            mxGetPr(prhs[2]), */
/*            mxGetNumberOfDimensions(prhs[3]), */
/*            mxGetDimensions(prhs[3])[0], */
/*            mxGetPr(prhs[3])); */

/*   /\* Variables needed to process the input *\/ */
/*   mwSize buflen; */
/*   size_t NElems; */
/*   mwSize ndimA, ndimb, ndimG, ndim, ndimP; */
/*   const mwSize *dimsA, *dimsb, *dims, *dimsP; */
/*   mwIndex jstruct, iii, jjj, i1, j1, idx_j; */
/*   mxArray *tmp, *tmp_cell; */
/*   /\* Variables needed for monitor *\/ */
/*   Node *node; */
/*   double *XTrace, *TStamps, *LTrace; */
/*   DistCompData distData; */
/*   PMap *predMap; */
/*   int kk, ll, tempI; */
/*   bool par_on; */
/*   bool is_Multi_HA; */
/*   int npred, npar; */

/*   static char uform[BUFF_LEN]; */
/*   static size_t hasuform = 0; */
/*   static int *cnt; */
/*   int temp = 0; */

/*   Miscellaneous *miscell = (Miscellaneous *)emalloc(sizeof(Miscellaneous));
 */
/*   int *tl_yychar = (int *)emalloc(sizeof(int)); */
/*   miscell->dp_taliro_param.LTL = 1; */
/*   miscell->dp_taliro_param.ConOnSamples = 0; */
/*   miscell->dp_taliro_param.SysDim = 0; */
/*   miscell->dp_taliro_param.nSamp = 0; */
/*   miscell->dp_taliro_param.nPred = 0; */
/*   miscell->dp_taliro_param.true_nPred = 0; */
/*   miscell->dp_taliro_param.tnLoc = 0; */
/*   miscell->dp_taliro_param.nInp = 0; */
/*   miscell->dp_taliro_param.nCLG = 1; */
/*   miscell->tl_errs = 0; */
/*   miscell->type_temp = 0; */

/*   /\* Reset cnt to 0: */
/*           cnt is the counter that points to the next symbol in the formula */
/*           to be processed. This is a static variable and it retains its */
/*           value between Matlab calls to mx_tp_taliro. *\/ */
/*   cnt = &temp; */

/*   /\* Other initializations *\/ */
/*   miscell->dp_taliro_param.nInp = nrhs; */
/*   par_on = false; */
/*   npred = 0; */
/*   npar = 0; */

/*   /\* Make sure the I/O are in the right form *\/ */
/*   if (nrhs < 3) */
/*     mexErrMsgTxt("mx_tp_taliro: At least 3 inputs are required."); */
/*   else if (nlhs > 1) */
/*     mexErrMsgTxt("mx_tp_taliro: Too many output arguments."); */
/*   else if (nrhs > 8) */
/*     mexErrMsgTxt("mx_tp_taliro: Too many input arguments."); */
/*   else if (!mxIsChar(prhs[0])) */
/*     mexErrMsgTxt("mx_tp_taliro: 1st input must be a string with TL
 * formula."); */
/*   else if (!mxIsStruct(prhs[1])) */
/*     mexErrMsgTxt( */
/*         "mx_tp_taliro: 2nd input must be a structure (predicate map)."); */
/*   else if (!mxIsDouble(prhs[2])) */
/*     mexErrMsgTxt( */
/*         "mx_tp_taliro: 3rd input must be a numerical array (State trace).");
 */
/*   else if (nrhs > 3 && !mxIsDouble(prhs[3])) */
/*     mexErrMsgTxt( */
/*         "mx_tp_taliro: 4th input must be a numerical array (Time stamps).");
 */
/*   else if (nrhs > 5 && !mxIsDouble(prhs[4])) */
/*     mexErrMsgTxt( */
/*         "mx_tp_taliro: 5th input must be a numerical array (Location
 * trace)."); */
/*   else if (nrhs > 5 && !(mxIsDouble(prhs[5]) || mxIsCell(prhs[5]))) */
/*     mexErrMsgTxt( */
/*         "mx_tp_taliro: 6th input must be a numerical array \n (Minimum path "
 */
/*         "distance to each control location for each predicate)."); */
/*   else if (nrhs > 7 && !(mxIsCell(prhs[6]))) */
/*     mexErrMsgTxt( */
/*         "mx_tp_taliro: 7th input must be a cell array (Adjacency list)."); */
/*   else if (nrhs > 7 && !(mxIsStruct(prhs[7]) || mxIsCell(prhs[7]))) */
/*     mexErrMsgTxt("mx_tp_taliro: 8th input must be a structure (guard map).");
 */

/*   if (nlhs > 1) mexErrMsgTxt("Too many output arguments."); */
/*   plhs[0] = mxCreateDoubleMatrix(1, 1, mxREAL); */

/*   /\* Process inputs *\/ */
/*   /\* Get the formula *\/ */
/*   dims = mxGetDimensions(prhs[0]); */
/*   buflen = dims[1] * sizeof(mxChar) + 1; */

/*   // 1. Check length of formula */
/*   if (buflen >= BUFF_LEN) { */
/*     mexPrintf("%s%d%s\n", "The formula must be less than ", BUFF_LEN, */
/*               " characters."); */
/*     mexErrMsgTxt("mx_tp_taliro: Formula too long."); */
/*   } */

/*   if (mxGetString(prhs[0], uform, buflen)) { */
/*     mexPrintf("%s%d\n", "mxArray: ", prhs[0]); */
/*     mexErrMsgTxt("mx_tp_taliro: unable to copy mxArray into str\n"); */
/*     tl_exit(2); */
/*   } */

/*   hasuform = strlen(uform); */

/*   for (iii = 0; iii < hasuform; iii++) { */
/*     if (uform[iii] == '\t' || uform[iii] == '\"' || uform[iii] == '\n') */
/*       uform[iii] = ' '; */
/*   } */

/*   /\* Get state trace *\/ */
/*   ndim = mxGetNumberOfDimensions(prhs[2]); */

/*   // 2. Check trace dimensions */
/*   if (ndim > 2) */
/*     mexErrMsgTxt("mx_tp_taliro: The state trace is not in proper form!"); */
/*   dims = mxGetDimensions(prhs[2]); */
/*   miscell->dp_taliro_param.nSamp = dims[0]; */
/*   miscell->dp_taliro_param.SysDim = dims[1]; */
/*   XTrace = mxGetPr(prhs[2]); */

/*   /\* Get time stamps *\/ */
/*   if (nrhs > 3) { */
/*     ndim = mxGetNumberOfDimensions(prhs[3]); */
/*     if (ndim > 2) */
/*       mexErrMsgTxt( */
/*           "mx_tp_taliro: The time stamp sequence is not in proper form!"); */
/*     dims = mxGetDimensions(prhs[3]); */
/*     if (miscell->dp_taliro_param.nSamp != dims[0]) */
/*       mexErrMsgTxt( */
/*           "mx_tp_taliro: The lengths of the time stamp sequence and the state
 * " */
/*           "trace do not match!"); */
/*     TStamps = mxGetPr(prhs[3]); */
/*   } */

/*   /\* Get location trace and location graph *\/ */
/*   if (nrhs > 4) { */
/*     ndim = mxGetNumberOfDimensions(prhs[4]); */
/*     if (ndim > 2) */
/*       mexErrMsgTxt("mx_tp_taliro: The location trace is not in proper
 * form!"); */
/*     dims = mxGetDimensions(prhs[4]); */
/*     if (miscell->dp_taliro_param.nSamp != dims[0]) */
/*       mexErrMsgTxt( */
/*           "mx_tp_taliro: The lengths of the location trace and the state
 * trace " */
/*           "do not match!"); */
/*     LTrace = mxGetPr(prhs[4]); */

/*     /\* For Multiple H.A.s is added  *\/ */
/*     miscell->dp_taliro_param.nCLG = dims[1]; */
/*     if (nrhs > 5 && (mxIsCell(prhs[5]))) { */
/*       is_Multi_HA = 1; */
/*       mexErrMsgTxt( */
/*           "mx_tp_taliro: Multiple Hybrid Automata is not suppoterd in " */
/*           "TP_TaLiRo!"); */
/*     } else if (nrhs > 5) { */
/*       is_Multi_HA = 0; */
/*       ndim = mxGetNumberOfDimensions(prhs[5]); */
/*       if (ndim > 2) */
/*         mexErrMsgTxt( */
/*             "mx_tp_taliro: The minimum distance array is not in proper
 * form!"); */
/*       dims = mxGetDimensions(prhs[5]); */
/*       miscell->dp_taliro_param.tnLoc = dims[0]; */
/*       distData.LDist = mxGetPr(prhs[5]); */
/*     } */
/*     /\*  For Multiple H.A.s *\/ */
/*   } */

/*   /\* Get guards *\/ */
/*   if (nrhs > 7 && is_Multi_HA == 0) { */
/*     /\*  ONE Hybrid Automata  *\/ */
/*     const mwSize *dimsG; */

/*     NElems = mxGetNumberOfElements(prhs[6]); */
/*     if (NElems == 0) { */
/*       mexErrMsgTxt("mx_tp_taliro: the adjacency list is empty!"); */
/*     } */
/*     distData.AdjL = (double **)emalloc(NElems * sizeof(double *)); */
/*     distData.AdjLNell = (size_t *)emalloc(NElems * sizeof(size_t)); */
/*     for (int ii = 0; ii < NElems; ii++) { */
/*       distData.AdjL[ii] = mxGetPr(mxGetCell(prhs[6], ii)); */
/*       ndim = mxGetNumberOfDimensions(mxGetCell(prhs[6], ii)); */
/*       dims = mxGetDimensions(mxGetCell(prhs[6], ii)); */
/*       if (ndim > 2 || dims[0] > 1) { */
/*         mexErrMsgTxt( */
/*             "mx_tp_taliro: The adjacency list is not in correct format!"); */
/*       } */
/*       distData.AdjLNell[ii] = dims[1]; */
/*     } */

/*     ndimG = mxGetNumberOfDimensions(prhs[7]); */
/*     if (ndimG > 2) { */
/*       mexErrMsgTxt("mx_tp_taliro: The guard sets are not in proper form!");
 */
/*     } */
/*     dimsG = mxGetDimensions(prhs[7]); */
/*     if ((dimsG[0] != dimsG[1]) || */
/*         (dimsG[0] != miscell->dp_taliro_param.tnLoc)) { */
/*       mexErrMsgTxt( */
/*           "mx_tp_taliro: The guard array must be a square array structure or
 * " */
/*           "\n the dimensions of the guard array do not match the adjacency "
 */
/*           "matrix!"); */
/*     } */
/*     distData.GuardMap = (GuardSet **)emalloc(dimsG[0] * sizeof(GuardSet *));
 */
/*     for (int ii = 0; ii < dimsG[0]; ii++) { */
/*       if (distData.AdjLNell[ii] > 0) { */
/*         distData.GuardMap[ii] = */
/*             (GuardSet *)emalloc(distData.AdjLNell[ii] * sizeof(GuardSet)); */
/*         for (int jj = 0; jj < distData.AdjLNell[ii]; jj++) { */
/*           /\* Get set for guard (ii,jj) *\/ */
/*           idx_j = ((mwIndex)distData.AdjL[ii][jj]) - 1; */
/*           /\* for projection is added *\/ */
/*           tmp_cell = mxGetField(prhs[7], ii + idx_j * dimsG[0], "proj"); */
/*           if (tmp_cell == NULL) { */
/*             distData.GuardMap[ii][jj].nproj = 0; */
/*           } else { */
/*             ndimP = mxGetNumberOfDimensions(tmp_cell); */
/*             if (ndimP > 2) { */
/*               mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 */
/*                         ")"); */
/*               mexErrMsgTxt( */
/*                   "mx_tp_taliro: Above guard: The projection map is not in "
 */
/*                   "proper form!"); */
/*             } */
/*             dimsP = mxGetDimensions(tmp_cell); */
/*             if (dimsP[0] != 1) { */
/*               mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 */
/*                         ")"); */
/*               mexErrMsgTxt( */
/*                   "mx_tp_taliro: Above guard: The projection map must be a
 * row " */
/*                   "vector !"); */
/*             } */
/*             if (dimsP[1] > miscell->dp_taliro_param.SysDim) { */
/*               mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 */
/*                         ")"); */
/*               mexErrMsgTxt( */
/*                   "mx_tp_taliro: Above guard: The projection map must have "
 */
/*                   "size less than or equal to the system dimentions !"); */
/*             } */
/*             distData.GuardMap[ii][jj].nproj = dimsP[1]; */
/*             distData.GuardMap[ii][jj].proj = */
/*                 (int *)emalloc(distData.GuardMap[ii][jj].nproj *
 * sizeof(int)); */
/*             tempI = 0; */
/*             for (iii = 0; iii < distData.GuardMap[ii][jj].nproj; iii++) { */
/*               distData.GuardMap[ii][jj].proj[iii] = */
/*                   (int)(mxGetPr(tmp_cell))[iii]; */
/*               if (distData.GuardMap[ii][jj].proj[iii] > */
/*                   miscell->dp_taliro_param.SysDim) { */
/*                 mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 */
/*                           ")"); */
/*                 mexErrMsgTxt( */
/*                     "mx_tp_taliro: Above guard: The projection index must be
 * " */
/*                     "less than or equal to the system dimentions !"); */
/*               } */
/*               if (distData.GuardMap[ii][jj].proj[iii] <= tempI) { */
/*                 mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 */
/*                           ")"); */
/*                 mexErrMsgTxt( */
/*                     "mx_tp_taliro: Above guard: The projection index must be
 * " */
/*                     "incremental !"); */
/*               } else { */
/*                 tempI = distData.GuardMap[ii][jj].proj[iii]; */
/*               } */
/*             } */
/*           } */
/*           /\* for projection *\/ */
/*           idx_j = ((mwIndex)distData.AdjL[ii][jj]) - 1; */
/*           tmp_cell = mxGetField(prhs[7], ii + idx_j * dimsG[0], "A"); */
/*           if (tmp_cell == NULL) { */
/*             mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 * ")"); */
/*             mexErrMsgTxt("mx_tp_taliro: Above guard: Field 'A' is
 * undefined!"); */
/*           } */
/*           /\* If it is a cell, then the guard set is a union of polytopes *\/
 */
/*           if (mxIsCell(tmp_cell)) { */
/*             ndim = mxGetNumberOfDimensions(tmp_cell); */
/*             if (ndim > 2) { */
/*               mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 */
/*                         ")"); */
/*               mexErrMsgTxt( */
/*                   "mx_tp_taliro: Above guard: if A is a cell, it must be a "
 */
/*                   "column vector cell!"); */
/*             } */
/*             dims = mxGetDimensions(tmp_cell); */
/*             if (dims[0] != 1) { */
/*               mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 */
/*                         ")"); */
/*               mexErrMsgTxt( */
/*                   "mx_tp_taliro: Above guard: if A is a cell, it must be a "
 */
/*                   "column vector cell!"); */
/*             } */
/*             distData.GuardMap[ii][jj].nset = dims[1]; /\* the number of sets
 * *\/ */
/*           } else { */
/*             /\* For backward combatibility, non-cell inputs should be also */
/*              * accepted *\/ */
/*             distData.GuardMap[ii][jj].nset = 1; /\* the number of sets *\/ */
/*           } */

/*           distData.GuardMap[ii][jj].ncon = */
/*               (int *)emalloc(distData.GuardMap[ii][jj].nset * sizeof(int));
 */
/*           distData.GuardMap[ii][jj].nproj = 0; */
/*           distData.GuardMap[ii][jj].A = (double ***)emalloc( */
/*               distData.GuardMap[ii][jj].nset * sizeof(double **)); */
/*           for (kk = 0; kk < distData.GuardMap[ii][jj].nset; kk++) { */
/*             if (mxIsCell(tmp_cell)) { */
/*               tmp = mxGetCell(tmp_cell, kk); */
/*             } else { */
/*               tmp = tmp_cell; */
/*             } */
/*             ndimA = mxGetNumberOfDimensions(tmp); */
/*             if (ndimA > 2) { */
/*               mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 */
/*                         ")"); */
/*               mexErrMsgTxt( */
/*                   "mx_tp_taliro: Above guard: A is not in proper form!"); */
/*             } */
/*             dimsA = mxGetDimensions(tmp); */
/*             if (miscell->dp_taliro_param.SysDim != dimsA[1]) { */
/*               mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 */
/*                         ")"); */
/*               mexErrMsgTxt( */
/*                   "mx_tp_taliro: Above guard: The dimensions of the set " */
/*                   "constraints and the state trace do not match!"); */
/*             } */
/*             distData.GuardMap[ii][jj].ncon[kk] = */
/*                 dimsA[0]; /\* the number of constraints *\/ */
/*             if (distData.GuardMap[ii][jj].ncon[kk] > 2 && */
/*                 miscell->dp_taliro_param.SysDim == 1) { */
/*               mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 */
/*                         ")"); */
/*               mexErrMsgTxt( */
/*                   "mx_tp_taliro: Above guard: For 1D signals only up to two "
 */
/*                   "constraints per predicate are allowed!\n More than two are
 * " */
/*                   "redundant!"); */
/*             } */
/*             distData.GuardMap[ii][jj].A[kk] = (double **)emalloc( */
/*                 distData.GuardMap[ii][jj].ncon[kk] * sizeof(double *)); */
/*             for (i1 = 0; i1 < distData.GuardMap[ii][jj].ncon[kk]; i1++) { */
/*               distData.GuardMap[ii][jj].A[kk][i1] = (double *)emalloc( */
/*                   miscell->dp_taliro_param.SysDim * sizeof(double)); */
/*               for (j1 = 0; j1 < miscell->dp_taliro_param.SysDim; j1++) { */
/*                 distData.GuardMap[ii][jj].A[kk][i1][j1] = (mxGetPr( */
/*                     tmp))[i1 + j1 * distData.GuardMap[ii][jj].ncon[kk]]; */
/*               } */
/*             } */
/*           } */
/*           /\* get b *\/ */
/*           tmp_cell = mxGetField(prhs[7], ii + idx_j * dimsG[0], "b"); */
/*           if (tmp_cell == NULL) { */
/*             mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 * ")"); */
/*             mexErrMsgTxt("mx_tp_taliro: Above guard: Field 'b' is
 * undefined!"); */
/*           } */
/*           /\* If it is a cell, then the guard set is a union of polytopes *\/
 */
/*           if (mxIsCell(tmp_cell)) { */
/*             ndim = mxGetNumberOfDimensions(tmp_cell); */
/*             if (ndim > 2) { */
/*               mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 */
/*                         ")"); */
/*               mexErrMsgTxt( */
/*                   "mx_tp_taliro: Above guard: if b is a cell, it must be a "
 */
/*                   "column vector cell!"); */
/*             } */
/*             dims = mxGetDimensions(tmp_cell); */
/*             if (dims[0] != 1) { */
/*               mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 */
/*                         ")"); */
/*               mexErrMsgTxt( */
/*                   "mx_tp_taliro: Above guard: if b is a cell, it must be a "
 */
/*                   "column vector cell!"); */
/*             } */
/*             if (distData.GuardMap[ii][jj].nset != dims[1]) { */
/*               mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 */
/*                         ")"); */
/*               mexErrMsgTxt( */
/*                   "mx_tp_taliro: Above guard: the dimensions of 'A' and 'b' "
 */
/*                   "must match!"); */
/*             } */
/*           } */
/*           distData.GuardMap[ii][jj].b = (double **)emalloc( */
/*               distData.GuardMap[ii][jj].nset * sizeof(double *)); */
/*           for (kk = 0; kk < distData.GuardMap[ii][jj].nset; kk++) { */
/*             if (mxIsCell(tmp_cell)) { */
/*               tmp = mxGetCell(tmp_cell, kk); */
/*             } else { */
/*               tmp = tmp_cell; */
/*             } */
/*             ndimb = mxGetNumberOfDimensions(tmp); */
/*             if (ndimb > 2) { */
/*               mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 */
/*                         ")"); */
/*               mexErrMsgTxt( */
/*                   "mx_tp_taliro: Above guard: The set constraints are not in
 * " */
/*                   "proper form!"); */
/*             } */
/*             dimsb = mxGetDimensions(tmp); */
/*             if (distData.GuardMap[ii][jj].ncon[kk] != dimsb[0]) { */
/*               mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 */
/*                         ")"); */
/*               mexErrMsgTxt( */
/*                   "mx_tp_taliro: Above guard: The number of constraints " */
/*                   "between A and b do not match!"); */
/*             } */
/*             distData.GuardMap[ii][jj].b[kk] = mxGetPr(tmp); */
/*             if (distData.GuardMap[ii][jj].ncon[kk] == 2 && */
/*                 miscell->dp_taliro_param.SysDim == 1) { */
/*               if ((distData.GuardMap[ii][jj].A[kk][0][0] > 0 && */
/*                    distData.GuardMap[ii][jj].A[kk][1][0] > 0) || */
/*                   (distData.GuardMap[ii][jj].A[kk][0][0] < 0 && */
/*                    distData.GuardMap[ii][jj].A[kk][1][0] < 0)) { */
/*                 mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 */
/*                           ")"); */
/*                 mexErrMsgTxt( */
/*                     "mx_tp_taliro: Above guard: The set has redundant " */
/*                     "constraints! Please remove redundant constraints."); */
/*               } */
/*               if (!((distData.GuardMap[ii][jj].A[kk][0][0] < 0 && */
/*                      (distData.GuardMap[ii][jj].b[kk][0] / */
/*                           distData.GuardMap[ii][jj].A[kk][0][0] <= */
/*                       distData.GuardMap[ii][jj].b[kk][1] / */
/*                           distData.GuardMap[ii][jj].A[kk][1][0])) || */
/*                     (distData.GuardMap[ii][jj].A[kk][1][0] < 0 && */
/*                      (distData.GuardMap[ii][jj].b[kk][1] / */
/*                           distData.GuardMap[ii][jj].A[kk][1][0] <= */
/*                       distData.GuardMap[ii][jj].b[kk][0] / */
/*                           distData.GuardMap[ii][jj].A[kk][0][0])))) { */
/*                 mexPrintf("%s%d%s%d%s \n", "Guard (", ii + 1, ",", idx_j + 1,
 */
/*                           ")"); */
/*                 mexErrMsgTxt( */
/*                     "mx_tp_taliro: Above guard: The set is empty! Please " */
/*                     "modify the constraints."); */
/*               } */
/*             } */
/*           } */
/*         } */
/*       } */
/*     } */
/*     /\*  ONE Hybrid Automata  *\/ */
/*   } */

/*   /\* Get predicate map*\/ */
/*   NElems = mxGetNumberOfElements(prhs[1]); */
/*   miscell->dp_taliro_param.nPred = NElems; */
/*   miscell->dp_taliro_param.true_nPred = NElems; */
/*   if (NElems == 0) mexErrMsgTxt("mx_tp_taliro: the predicate map is empty!");
 */
/*   predMap = (PMap *)emalloc(NElems * sizeof(PMap)); */
/*   miscell->parMap = (ParMap *)emalloc(NElems * sizeof(ParMap)); */
/*   miscell->predMap = (PMap *)emalloc(NElems * sizeof(PMap)); */

/*   miscell->pList.pindex = (int *)emalloc(NElems * sizeof(int)); */

/*   /\* initial predicate list*\/ */
/*   for (ll = 0; ll < NElems; ll++) { */
/*     miscell->pList.pindex[ll] = -1; */
/*   } */

/*   for (jstruct = 0; jstruct < NElems; jstruct++) { */
/*     /\* Get predicate name *\/ */
/*     tmp = mxGetField(prhs[1], jstruct, "str"); */
/*     if (tmp == NULL) { */
/*       tmp = mxGetField(prhs[1], jstruct, "par"); */
/*       if (tmp == NULL) { */
/*         mexPrintf("%s%d\n", "Predicate no ", jstruct + 1); */
/*         mexErrMsgTxt( */
/*             "mx_tp_taliro: The above parameter must has either the 'str'
 * field " */
/*             "or 'par' field!"); */
/*       } else { */
/*         par_on = true; */
/*         npar++; */
/*       } */
/*     } else { */
/*       par_on = false; */
/*       npred++; */
/*     } */

/*     /\* If this is a parameter *\/ */
/*     if (par_on) { */
/*       mexErrMsgTxt( */
/*           "mx_tp_taliro: parameter estimation is not supported by TP-TaLiRo
 * !"); */
/*     } else { */
/*       /\* Get name of the predicate *\/ */
/*       dims = mxGetDimensions(tmp); */
/*       buflen = dims[1] * sizeof(mxChar) + 1; */
/*       predMap[jstruct].str = (char *)emalloc(buflen); */
/*       miscell->predMap[jstruct].str = (char *)emalloc(buflen); */
/*       predMap[jstruct].set.idx = (int)jstruct; */
/*       predMap[jstruct].true_pred = true; */

/*       if (mxGetString(tmp, predMap[jstruct].str, buflen)) { */
/*         mexPrintf("%s%d\n", "Predicate no ", jstruct + 1); */
/*         mexErrMsgTxt("mx_tp_taliro: unable to copy mxArray into str\n"); */
/*         tl_exit(2); */
/*       } */

/*       if (mxGetString(tmp, miscell->predMap[jstruct].str, buflen)) { */
/*         mexPrintf("%s%d\n", "Predicate no ", jstruct + 1); */
/*         mexErrMsgTxt("mx_tp_taliro: unable to copy mxArray into str\n"); */
/*         tl_exit(2); */
/*       } */

/*       /\* Get range*\/ */
/*       tmp = mxGetField(prhs[1], jstruct, "range"); */
/*       if (tmp != NULL) { */
/*         predMap[jstruct].Range = mxGetPr(tmp); */
/*         miscell->predMap[jstruct].Range = mxGetPr(tmp); */
/*       } */

/*       tmp = mxGetField(prhs[1], jstruct, "Normalized"); */
/*       if (tmp != NULL) { */
/*         miscell->predMap[jstruct].Normalized = mxGetScalar(tmp) > 0.5; */
/*         predMap[jstruct].Normalized = miscell->predMap[jstruct].Normalized;
 */
/*         if (miscell->predMap[jstruct].Normalized) { */
/*           tmp = mxGetField(prhs[1], jstruct, "NormBounds"); */
/*           if (tmp == NULL) { */
/*             mexPrintf("%s%s \n", "Predicate: ",
 * miscell->predMap[jstruct].str); */
/*             mexErrMsgTxt( */
/*                 "mx_tp_taliro: Above predicate: 'NormBounds' is " */
/*                 "empty/undefined when 'Normalized' is set to true!"); */
/*           } */
/*           ndim = mxGetNumberOfDimensions(tmp); */
/*           dims = mxGetDimensions(tmp); */
/*           if (!(ndim == 2 && ((dims[0] == 1 && dims[1] == 1) || */
/*                               (dims[0] == 1 && dims[1] == 2) || */
/*                               (dims[0] == 2 && dims[1] == 1)))) { */
/*             mexPrintf("%s%s \n", "Predicate: ",
 * miscell->predMap[jstruct].str); */
/*             mexErrMsgTxt( */
/*                 "mx_tp_taliro: Above predicate: 'NormBounds' should be a 1D
 * or " */
/*                 "2D vector!"); */
/*           } */
/*           if (nrhs > 4 && !((dims[0] == 1 && dims[1] == 2) || */
/*                             (dims[0] == 2 && dims[1] == 1))) { */
/*             mexPrintf("%s%s \n", "Predicate: ",
 * miscell->predMap[jstruct].str); */
/*             mexErrMsgTxt( */
/*                 "mx_tp_taliro: Above predicate: 'NormBounds' should be a 2D "
 */
/*                 "vector!"); */
/*           } */
/*           predMap[jstruct].NormBounds = mxGetPr(tmp); */
/*           miscell->predMap[jstruct].NormBounds = mxGetPr(tmp); */
/*         } else { */
/*           miscell->predMap[jstruct].Normalized = false; */
/*           predMap[jstruct].Normalized = false; */
/*           miscell->predMap[jstruct].NormBounds = NULL; */
/*           predMap[jstruct].NormBounds = NULL; */
/*         } */
/*       } */
/*       /\* Get projection *\/ */
/*       tmp = mxGetField(prhs[1], jstruct, "proj"); */
/*       if (tmp == NULL) { */
/*         predMap[jstruct].set.nproj = 0; */
/*       } else { */
/*         ndimP = mxGetNumberOfDimensions(tmp); */
/*         if (ndimP > 2) { */
/*           mexPrintf("%s%s \n", "Predicate: ", predMap[jstruct].str); */
/*           mexErrMsgTxt( */
/*               "mx_tp_taliro: Above predicate: The projection map is not in "
 */
/*               "proper form!"); */
/*         } */
/*         dimsP = mxGetDimensions(tmp); */
/*         if (dimsP[0] != 1) { */
/*           mexPrintf("%s%s \n", "Predicate: ", predMap[jstruct].str); */
/*           mexErrMsgTxt( */
/*               "mx_tp_taliro: Above predicate: The projection map must be a
 * row " */
/*               "vector !"); */
/*         } */
/*         if (dimsP[1] > miscell->dp_taliro_param.SysDim) { */
/*           mexPrintf("%s%s \n", "Predicate: ", predMap[jstruct].str); */
/*           mexErrMsgTxt( */
/*               "mx_tp_taliro: Above predicate: The projection map must have "
 */
/*               "size less than or equal to the system dimentions !"); */
/*         } */
/*         predMap[jstruct].set.nproj = dimsP[1]; */
/*         predMap[jstruct].set.proj = */
/*             (int *)emalloc(predMap[jstruct].set.nproj * sizeof(int)); */
/*         tempI = 0; */
/*         for (iii = 0; iii < predMap[jstruct].set.nproj; iii++) { */
/*           predMap[jstruct].set.proj[iii] = (int)(mxGetPr(tmp))[iii]; */
/*           if (predMap[jstruct].set.proj[iii] > */
/*               miscell->dp_taliro_param.SysDim) { */
/*             mexPrintf("%s%s \n", "Predicate: ", predMap[jstruct].str); */
/*             mexErrMsgTxt( */
/*                 "mx_tp_taliro: Above predicate: The projection index must be
 * " */
/*                 "less than or equal to the system dimentions !"); */
/*           } */
/*           if (predMap[jstruct].set.proj[iii] <= tempI) { */
/*             mexPrintf("%s%s \n", "Predicate: ", predMap[jstruct].str); */
/*             mexErrMsgTxt( */
/*                 "mx_tp_taliro: Above predicate: The projection index must be
 * " */
/*                 "incremental !"); */
/*           } else { */
/*             tempI = predMap[jstruct].set.proj[iii]; */
/*           } */
/*         } */
/*       } */

/*       /\* Get set *\/ */
/*       tmp = mxGetField(prhs[1], jstruct, "A"); */
/*       /\* If A is empty, then we should have an interval *\/ */
/*       if (tmp == NULL) { */
/*         tmp = mxGetField(prhs[1], jstruct, "Int"); */
/*         if (tmp == NULL) { */
/*           mexPrintf("%s%s \n", "Predicate: ", predMap[jstruct].str); */
/*           mexErrMsgTxt( */
/*               "mx_tp_taliro: Above predicate: Both fields 'A' and 'Int' do
 * not " */
/*               "exist!"); */
/*         } */
/*       } else if (mxIsEmpty(tmp)) { */
/*         predMap[jstruct].set.isSetRn = true; */
/*         predMap[jstruct].set.ncon = 0; */
/*       } else { */
/*         predMap[jstruct].set.isSetRn = false; */
/*         /\* get A *\/ */
/*         ndimA = mxGetNumberOfDimensions(tmp); */
/*         if (ndimA > 2) { */
/*           mexPrintf("%s%s \n", "Predicate: ", predMap[jstruct].str); */
/*           mexErrMsgTxt( */
/*               "mx_tp_taliro: Above predicate: The set constraints are not in
 * " */
/*               "proper form!"); */
/*         } */
/*         dimsA = mxGetDimensions(tmp); */
/*         /\* for projection is updated *\/ */
/*         if ((miscell->dp_taliro_param.SysDim != dimsA[1] && */
/*              predMap[jstruct].set.nproj == 0) || */
/*             (predMap[jstruct].set.nproj != dimsA[1] && */
/*              predMap[jstruct].set.nproj > 0)) { */
/*           mexPrintf("%s%s \n", "Predicate: ", predMap[jstruct].str); */
/*           mexErrMsgTxt( */
/*               "mx_tp_taliro: Above predicate: The dimensions of the set " */
/*               "constraints and the state trace do not match!"); */
/*         } */
/*         predMap[jstruct].set.ncon = dimsA[0]; /\* the number of constraints
 * *\/ */
/*         if (predMap[jstruct].set.ncon > 2 && */
/*             miscell->dp_taliro_param.SysDim == 1) { */
/*           mexPrintf("%s%s \n", "Predicate: ", predMap[jstruct].str); */
/*           mexErrMsgTxt( */
/*               "mx_tp_taliro: Above predicate: For 1D signals only up to two "
 */
/*               "constraints per predicate are allowed!\n More than two are "
 */
/*               "redundant!"); */
/*         } */
/*         /\* for projection is added *\/ */
/*         predMap[jstruct].set.A = */
/*             (double **)emalloc(predMap[jstruct].set.ncon * sizeof(double *));
 */
/*         if (predMap[jstruct].set.nproj == 0) { */
/*           for (iii = 0; iii < predMap[jstruct].set.ncon; iii++) { */
/*             predMap[jstruct].set.A[iii] = (double *)emalloc( */
/*                 miscell->dp_taliro_param.SysDim * sizeof(double)); */
/*             for (jjj = 0; jjj < miscell->dp_taliro_param.SysDim; jjj++) */
/*               predMap[jstruct].set.A[iii][jjj] = */
/*                   (mxGetPr(tmp))[iii + jjj * predMap[jstruct].set.ncon]; */
/*           } */
/*         } else { */
/*           for (iii = 0; iii < predMap[jstruct].set.ncon; iii++) { */
/*             predMap[jstruct].set.A[iii] = */
/*                 (double *)emalloc(predMap[jstruct].set.nproj *
 * sizeof(double)); */
/*             for (jjj = 0; jjj < predMap[jstruct].set.nproj; jjj++) */
/*               predMap[jstruct].set.A[iii][jjj] = */
/*                   (mxGetPr(tmp))[iii + jjj * predMap[jstruct].set.ncon]; */
/*           } */
/*         } */
/*         /\* for projection *\/ */

/*         /\* get b *\/ */
/*         tmp = mxGetField(prhs[1], jstruct, "b"); */
/*         if (tmp == NULL) { */
/*           mexPrintf("%s%s\n", "Predicate: ", predMap[jstruct].str); */
/*           mexErrMsgTxt("mx_tp_taliro: Above predicate: Field 'b' is empty!");
 */
/*         } */
/*         ndimb = mxGetNumberOfDimensions(tmp); */
/*         if (ndimb > 2) { */
/*           mexPrintf("%s%s\n", "Predicate: ", predMap[jstruct].str); */
/*           mexErrMsgTxt( */
/*               "mx_tp_taliro: Above predicate: The set constraints are not in
 * " */
/*               "proper form!"); */
/*         } */
/*         dimsb = mxGetDimensions(tmp); */
/*         if (predMap[jstruct].set.ncon != dimsb[0]) { */
/*           mexPrintf("%s%s\n", "Predicate: ", predMap[jstruct].str); */
/*           mexErrMsgTxt( */
/*               "mx_tp_taliro: Above predicate: The number of constraints " */
/*               "between A and b do not match!"); */
/*         } */
/*         predMap[jstruct].set.b = mxGetPr(tmp); */
/*         if (predMap[jstruct].set.ncon == 2 && */
/*             (miscell->dp_taliro_param.SysDim == 1 || */
/*              predMap[jstruct].set.nproj == 1)) { */
/*           if ((predMap[jstruct].set.A[0][0] > 0 && */
/*                predMap[jstruct].set.A[1][0] > 0) || */
/*               (predMap[jstruct].set.A[0][0] < 0 && */
/*                predMap[jstruct].set.A[1][0] < 0)) { */
/*             mexPrintf("%s%s\n", "Predicate: ", predMap[jstruct].str); */
/*             mexErrMsgTxt( */
/*                 "mx_tp_taliro: Above predicate: The set has redundant " */
/*                 "constraints! Please remove redundant constraints."); */
/*           } */
/*           if (!((predMap[jstruct].set.A[0][0] < 0 && */
/*                  (predMap[jstruct].set.b[0] / predMap[jstruct].set.A[0][0] <=
 */
/*                   predMap[jstruct].set.b[1] / predMap[jstruct].set.A[1][0]))
 * || */
/*                 (predMap[jstruct].set.A[1][0] < 0 && */
/*                  (predMap[jstruct].set.b[1] / predMap[jstruct].set.A[1][0] <=
 */
/*                   predMap[jstruct].set.b[0] /
 * predMap[jstruct].set.A[0][0])))) { */
/*             mexPrintf("%s%s\n", "Predicate: ", predMap[jstruct].str); */
/*             mexErrMsgTxt( */
/*                 "mx_tp_taliro: Above predicate: The set is empty! Please " */
/*                 "modify the constraints."); */
/*           } */
/*         } */
/*       } */
/*       /\* get control locations *\/ */
/*       if (nrhs > 4) { */
/*         tmp = mxGetField(prhs[1], jstruct, "loc"); */
/*         if (is_Multi_HA == 0) { */
/*           size_t NCells; */

/*           NCells = mxGetNumberOfElements(tmp); */
/*           if (tmp == NULL) { */
/*             mexPrintf("%s%s\n", "Predicate: ", predMap[jstruct].str); */
/*             mexErrMsgTxt( */
/*                 "mx_tp_taliro: Above predicate: Field 'loc' is empty!"); */
/*           } */
/*           ndim = mxGetNumberOfDimensions(tmp); */
/*           if (ndim > 2) { */
/*             mexPrintf("%s%s\n", "Predicate: ", predMap[jstruct].str); */
/*             mexErrMsgTxt( */
/*                 "mx_tp_taliro: Above predicate: The control location vector
 * is " */
/*                 "not in proper form!"); */
/*           } */
/*           dims = mxGetDimensions(tmp); */
/*           if (dims[0] > 1) { */
/*             mexPrintf("%s%s\n", "Predicate: ", predMap[jstruct].str); */
/*             mexErrMsgTxt( */
/*                 "mx_tp_taliro: Above predicate: The control location vector "
 */
/*                 "must be row vector!"); */
/*           } */
/*           predMap[jstruct].set.nloc = dims[1]; */
/*           predMap[jstruct].set.loc = mxGetPr(tmp); */
/*         } */
/*       } */
/*     } */
/*   } */

/*   miscell->tl_out = stdout; */

/*   /\* set up some variables wrt to timing constraints *\/ */
/*   miscell->zero2inf.l_closed = 1; */
/*   miscell->zero2inf.u_closed = 0; */
/*   miscell->emptyInter.l_closed = 0; */
/*   miscell->emptyInter.u_closed = 0; */
/*   if (miscell->dp_taliro_param.ConOnSamples) { */
/*     miscell->zero.numi.inf = 0; */
/*     miscell->zero.numi.i_num = 0; */
/*     miscell->inf.numi.inf = 1; */
/*     miscell->inf.numi.i_num = 0; */
/*     miscell->zero2inf.lbd = miscell->zero; */
/*     miscell->zero2inf.ubd = miscell->inf; */
/*     miscell->emptyInter.lbd = miscell->zero; */
/*     miscell->emptyInter.ubd = miscell->zero; */
/*   } else { */
/*     miscell->zero.numf.inf = 0; */
/*     miscell->zero.numf.f_num = 0.0; */
/*     miscell->inf.numf.inf = 1; */
/*     miscell->inf.numf.f_num = 0.0; */
/*     miscell->zero2inf.lbd = miscell->zero; */
/*     miscell->zero2inf.ubd = miscell->inf; */
/*     miscell->emptyInter.lbd = miscell->zero; */
/*     miscell->emptyInter.ubd = miscell->zero; */
/*   } */

/*   node = tl_parse(cnt, hasuform, uform, miscell, tl_yychar); */
/*   temp = 0; */
/*   cnt = &temp; */
/*   countVar(cnt, node, NULL, 0); */
/*   /\*mexPrintf("\nNumber of freeze time variables is %d\n",(*cnt));*\/ */

/*   if ((*cnt) > 0) { */
/*     miscell->dp_taliro_param.TPTL = 1; */
/*     miscell->dp_taliro_param.LTL = 0; */
/*     /\*mexPrintf("\nTPTL\n");*\/ */
/*   } else { */
/*     miscell->dp_taliro_param.TPTL = 0; */
/*     miscell->dp_taliro_param.LTL = 1; */
/*     /\*mexPrintf("\nLTL\n");*\/ */
/*   } */

/*   if (miscell->dp_taliro_param.LTL == 0 && nrhs < 4) */
/*     mexErrMsgTxt( */
/*         "mx_tp_taliro: The formula is in MTL, but there are no timestamps!");
 */

/*   plhs[0] = DP(node, predMap, XTrace, TStamps, LTrace, &distData, */
/*                &(miscell->dp_taliro_param), miscell); */

/*   for (iii = 0; iii < miscell->dp_taliro_param.true_nPred; iii++) { */
/*     tl_clearlookup(predMap[iii].str, miscell); */
/*     for (jjj = 0; jjj < predMap[iii].set.ncon; jjj++) */
/*       mxFree(predMap[iii].set.A[jjj]); */
/*     mxFree(predMap[iii].str); */
/*     mxFree(predMap[iii].set.A); */
/*   } */
/*   for (iii = 0; iii < miscell->dp_taliro_param.true_nPred; iii++) { */
/*     mxFree(miscell->predMap[iii].str); */
/*     mxFree(miscell->parMap[iii].str); */
/*   } */
/*   mxFree(miscell->pList.pindex); */
/*   mxFree(miscell->predMap); */
/*   mxFree(miscell->parMap); */
/*   mxFree(predMap); */
/*   /\* for projection and multiple H.A.s is updated *\/ */
/*   if (nrhs > 7) { */
/*     if (is_Multi_HA == 0) { */
/*       for (iii = 0; iii < miscell->dp_taliro_param.tnLoc; iii++) { */
/*         for (jjj = 0; jjj < distData.AdjLNell[iii]; jjj++) { */
/*           for (kk = 0; kk < distData.GuardMap[iii][jjj].nset; kk++) { */
/*             for (i1 = 0; i1 < distData.GuardMap[iii][jjj].ncon[kk]; i1++) {
 */
/*               mxFree(distData.GuardMap[iii][jjj].A[kk][i1]); */
/*             } */
/*             mxFree(distData.GuardMap[iii][jjj].A[kk]); */
/*           } */
/*           mxFree(distData.GuardMap[iii][jjj].A); */
/*           mxFree(distData.GuardMap[iii][jjj].b); */
/*           mxFree(distData.GuardMap[iii][jjj].ncon); */
/*         } */
/*         mxFree(distData.GuardMap[iii]); */
/*       } */
/*       mxFree(distData.GuardMap); */
/*       mxFree(distData.AdjLNell); */
/*       mxFree(distData.AdjL); */
/*     } */
/*   } */
/*   mxFree(miscell); */
/*   mxFree(tl_yychar); */
/*   ; */
/* } */
