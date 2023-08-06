#ifndef TPTALIRO_CORE_PARAM_H
#define TPTALIRO_CORE_PARAM_H

#include "banned.h"
#include "core/ltl2tree.h"  // Node, Number

#define max(a, b) (((a) > (b)) ? (a) : (b))

int enqueue(struct queue *q, Node *phi);
Node *popfront(struct queue *q);
int dequeue(struct queue *q);
void init_queue(struct queue *q);
int queue_empty_p(const struct queue *q);
/* mxArray *DP(Node *phi, PMap *predMap, const double *XTrace, */
/*             const double *TStamps, const double *LTrace, */
/*             DistCompData *p_distData, FWTaliroParam *param, */
/*             Miscellaneous *miscell); */

HyDis hmax(HyDis inp1, HyDis inp2);
HyDis hmin(HyDis inp1, HyDis inp2);

void moveNode2to1(Node **pt_node1, Node *node2);
void moveNodeFromLeft(Node **node);
void moveNodeFromRight(Node **node);
Node *SimplifyNodeValue(Node *node);
Node *SimplifyBoolConn(int BCon, Node *node, void (*MoveNodeL)(Node **),
                       void (*MoveNodeR)(Node **),
                       HyDis (*Comparison)(HyDis, HyDis));

Interval NumberPlusInter(Number num, Interval inter);
int e_le(Number num1, Number num2, FWTaliroParam *p_par);
int e_eq(Number num1, Number num2, FWTaliroParam *p_par);
int e_leq(Number num1, Number num2, FWTaliroParam *p_par);
int e_ge(Number num1, Number num2, FWTaliroParam *p_par);
int e_geq(Number num1, Number num2, FWTaliroParam *p_par);

#endif
