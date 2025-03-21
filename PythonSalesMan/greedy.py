
import graph
import math
import sys
import queue
import dijkstra


# SalesmanTrackGreedy ==========================================================
def get_arestas(v1, v):
    arestas = [v1.previousEdge]
    pred = v1.previousNode
    while pred != v:
        arestas.append(pred.previousEdge)
        pred = pred.previousNode
    arestas.reverse()
    return arestas

def SalesmanTrackGreedy(g, visits):
    objetivo = visits.Vertices[-1]
    vertice = visits.Vertices[0]
    candidatos = visits.Vertices[1:-1]
    camino = graph.Track(g)
    arestas = []

    while candidatos:
        dijkstra.Dijkstra(g, vertice)
        distancia_minima = math.inf
        nuevo_vertice = min((vertex for vertex in candidatos if vertex.DijkstraDistance < distancia_minima),
                            key=lambda vertex: vertex.DijkstraDistance)
        candidatos.remove(nuevo_vertice)
        arestas.extend(get_arestas(nuevo_vertice, vertice))
        vertice = nuevo_vertice
    dijkstra.Dijkstra(g, vertice)
    arestas.extend(get_arestas(objetivo, vertice))

    for edge in arestas:
        camino.AddLast(edge)

    return camino