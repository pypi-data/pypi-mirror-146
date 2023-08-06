#ifndef TPTALIRO_CORE_DP_H
#define TPTALIRO_CORE_DP_H

#include <stddef.h>

#include "banned.h"
#include "core/distances.h"
#include "core/ltl2tree.h"

#define intMax32bit 2147483647

HyDis SetToInf(int, int);

double Normalize(double, double);
HyDis NormalizeHybrid(HyDis, double, double);

int enqueue(struct queue *, Node *);
int dequeue(struct queue *);

int BFS(struct queue *, Node *, int *);

void print2file2(Node *, FILE *);
void setupIndeces(Node **, Node *);

void printTable(HyDis **, FWTaliroParam *, int);

void DP_LTL(Node **, HyDis **, FWTaliroParam *, int, size_t, int);
void Resolve_Constraint(Node **, HyDis **, const double *, int, int, int,
                        double);

/* mxArray *DP(Node *, PMap *, const double *, const double *, const double *,
 */
/*             DistCompData *, FWTaliroParam *, Miscellaneous *); */

void moveNode2to1(Node **, Node *);
void moveNodeFromRight(Node **);
void moveNodeFromLeft(Node **);

Node *SimplifyNodeValue(Node *);
Node *SimplifyBoolConn(int, Node *, void (*MoveNodeL)(Node **),
                       void (*MoveNodeR)(Node **),
                       HyDis (*Comparison)(HyDis, HyDis));

HyDis hmax(HyDis, HyDis);
HyDis hmin(HyDis, HyDis);

Interval NumberPlusInter(Number, Interval);

int e_le(Number, Number, FWTaliroParam *);
int e_eq(Number, Number, FWTaliroParam *);
int e_leq(Number, Number, FWTaliroParam *);
int e_ge(Number, Number, FWTaliroParam *);
int e_geq(Number, Number, FWTaliroParam *);

/* inline definition(s) */
void init_queue(struct queue *q);
int queue_empty_p(const struct queue *q);

int imax(int a, int b);
int imin(int a, int b);

#endif
