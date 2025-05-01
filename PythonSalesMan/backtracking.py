import graph
import math
import sys
import queue
import dijkstra

def SalesmanTrackBacktracking(g, visits):
    mejor_camino = None
    mejor_distancia = math.inf
    
    origen = visits.Vertices[0]
    destino = visits.Vertices[-1]
    visitas_intermedias = set(visits.Vertices[1:-1])

    camino_actual = []
    
    def backtrack(v_actual, dist_actual, pendientes, visitados_tramo):
        nonlocal mejor_camino, mejor_distancia

        # Llegar a una visita pendiente
        nueva_visita = False
        if v_actual in pendientes:
            pendientes = pendientes - {v_actual}
            visitados_tramo = set()  # Reset visitas del tramo
            nueva_visita = True

        # Comprobar fin del camino
        if v_actual == destino and not pendientes:
            if dist_actual < mejor_distancia:
                mejor_camino = camino_actual[:]
                mejor_distancia = dist_actual
            return
        
        # Explorar vecinos
        for arista in v_actual.Edges:
            vecino = arista.Destination
            if vecino not in visitados_tramo:
                camino_actual.append(arista)
                visitados_tramo.add(vecino)

                nueva_distancia = dist_actual + arista.Length
                if nueva_distancia < mejor_distancia:
                    backtrack(vecino, nueva_distancia, pendientes, visitados_tramo)

                camino_actual.pop()
                visitados_tramo.remove(vecino)

    visitados_tramo = set([origen])
    backtrack(origen, 0, visitas_intermedias, visitados_tramo)

    track_resultado = graph.Track(g)
    if mejor_camino:
        for arista in mejor_camino:
            track_resultado.AddLast(arista)

    return track_resultado

# ==============================================================================

def SalesmanTrackBacktrackingGreedy(g, visits):
    return graph.Track(g)

