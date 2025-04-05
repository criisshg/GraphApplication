# -*- coding: utf-8 -*-
import dijkstra
import graph
import math
import sys
import heapq

# SalesmanTrackGreedy ==========================================================
def get_arestas(v1, v):
    """Reconstruye el camino desde v1 hasta v usando los nodos anteriores"""
    arestas = []
    current = v1
    while current != v:
        # Añadir la arista al camino
        arestas.append(current.previousEdge)
        current = current.previousNode
    arestas.reverse()
    return arestas

def SalesmanTrackGreedy(g, visits):
    if len(visits.Vertices) < 2:  # Si no hay suficientes vértices, no hay camino para recorrer
        return graph.Track(g)
    
    # inicializar el camino y los vértices
    objetivo = visits.Vertices[-1]
    vertice_actual = visits.Vertices[0]
    candidatos = visits.Vertices[1:-1]
    camino = graph.Track(g)
    
    # Precomputar todas las distancias desde el vértice actual
    dijkstra.DijkstraQueue(g, vertice_actual)
    
    while candidatos:
        # Encontrar el candidato más cercano usando la distancia ya calculada
        candidato_mas_cercano = min(candidatos, key=lambda v: v.DijkstraDistance)
        
        # Reconstruir camino y actualizar
        arestas_camino = get_arestas(candidato_mas_cercano, vertice_actual)
        for edge in arestas_camino:
            camino.AddLast(edge)
        
        # Actualizar para la siguiente iteración
        vertice_actual = candidato_mas_cercano
        candidatos.remove(candidato_mas_cercano)
        
        # Recalcular distancias desde el nuevo vértice
        dijkstra.DijkstraQueue(g, vertice_actual)
    
    # Añadir camino al objetivo final
    arestas_finales = get_arestas(objetivo, vertice_actual)
    for edge in arestas_finales:
        camino.AddLast(edge)
    return camino