#include "pch.h"
#include "Graph.h"
#include "GraphApplicationDlg.h"
#include <set>



// =============================================================================
// CONVEX HULL =================================================================
// =============================================================================

// left ========================================================================
// Recta de p1 a p2. i posició del punt p respecte la recta
// resultat>0: p a la esquerra.
// resultat==0: p sobre la recta.
// resultat<0: p a la dreta

double PosicioRespeteRecta(CGPoint& a, CGPoint& b, CGPoint &c)
{
	return (a.m_Y - b.m_Y) * (c.m_X - b.m_X) - (a.m_X - b.m_X) * (c.m_Y - b.m_Y);
}

// AreaTriangle ================================================================

double AreaTriangle(CGPoint& a, CGPoint& b, CGPoint c)
{
	return abs((a.m_Y - b.m_Y) * (c.m_X - b.m_X) - (a.m_X - b.m_X) * (c.m_Y - b.m_Y)) / 2.0;
}

// QuickHullRec =================================================================

list<CVertex*> QuickHullRec(CVertex* pV1,CVertex* pV2,list<CVertex*> &vertices)
{
	if (vertices.empty()) return {pV1, pV2};
	CVertex* pVMaxArea=NULL;
	double maxArea = -1;
	for (CVertex* pV : vertices) {
		double area = AreaTriangle(pV1->m_Point, pV2->m_Point, pV->m_Point);
		if (area > maxArea) {
			maxArea = area;
			pVMaxArea = pV;
		}
	}
	//return { pMin, pVMaxArea, pMax };
	if (maxArea<=0) return { pV1, pV2 };
	list<CVertex*> left;
	list<CVertex*> right;
	for (CVertex* pV : vertices) {
		if (PosicioRespeteRecta(pV1->m_Point, pVMaxArea->m_Point, pV->m_Point) > 0) {
			left.push_back(pV);
		}
		else if (PosicioRespeteRecta(pVMaxArea->m_Point,pV2->m_Point, pV->m_Point) > 0) {
			right.push_back(pV);
		}
	}
	list<CVertex*> qhLeft = QuickHullRec(pV1, pVMaxArea, left);
	list<CVertex*> qhRight = QuickHullRec(pVMaxArea,pV2, right);
	qhRight.pop_front();
	for (CVertex* pV : qhRight) 	qhLeft.push_back(pV);
	return qhLeft;
}


// QuickHull ===================================================================

CConvexHull QuickHull(CGraph& g)
{
	CConvexHull ch(&g);
	if (g.m_Vertices.empty()) return ch;
	CVertex* pMin = &g.m_Vertices.front();
	CVertex* pMax= pMin;
	for (CVertex& v : g.m_Vertices) {
		if (v.m_Point.m_X < pMin->m_Point.m_X || v.m_Point.m_X == pMin->m_Point.m_X && v.m_Point.m_Y < pMin->m_Point.m_Y) pMin = &v;
		else if (v.m_Point.m_X > pMax->m_Point.m_X || v.m_Point.m_X == pMax->m_Point.m_X && v.m_Point.m_Y > pMax->m_Point.m_Y) pMax = &v;
	}
	if (pMin->m_Point == pMax->m_Point) {
		ch.m_Vertices.push_back(pMin);
	}
	else {
		list<CVertex*> up;
		list<CVertex*> down;
		for (CVertex& v : g.m_Vertices) {
			double pos = PosicioRespeteRecta(pMin->m_Point, pMax->m_Point, v.m_Point);
			if (pos > 0) down.push_back(&v);
			else if (pos < 0) up.push_back(&v);
		}
		list<CVertex*> qhLeft = QuickHullRec(pMin, pMax, down);
		list<CVertex*> qhRight = QuickHullRec(pMax, pMin, up);
		qhRight.pop_front();
		qhRight.pop_back();
		for (CVertex* pV : qhRight) qhLeft.push_back(pV);
		ch.m_Vertices = qhLeft;
	}
	return ch;
}