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

def reconstruir_camino(origen, destino):
    camino = []
    actual = destino
    while actual != origen:
        if actual.previousEdge is None:
            return []  # No existe camino
        camino.append(actual.previousEdge)
        actual = actual.previousNode
    camino.reverse()
    return camino

def SalesmanTrackBacktrackingGreedy(g, visits):
    num_visitas = len(visits.Vertices)

    # Caso simple (solo origen y destino)
    if num_visitas == 2:
        dijkstra.DijkstraQueue(g, visits.Vertices[0])
        camino_simple = reconstruir_camino(visits.Vertices[0], visits.Vertices[1])
        track_resultado = graph.Track(g)
        for arista in camino_simple:
            track_resultado.AddLast(arista)
        return track_resultado

    mejor_distancia = math.inf
    mejor_camino = []

    distancias = [[math.inf]*num_visitas for _ in range(num_visitas)]
    caminos = [[[] for _ in range(num_visitas)] for _ in range(num_visitas)]

    # Precalcular caminos óptimos con Dijkstra y verificar existencia
    for i, origen in enumerate(visits.Vertices):
        dijkstra.DijkstraQueue(g, origen)
        for j, destino in enumerate(visits.Vertices):
            if i != j:
                camino = reconstruir_camino(origen, destino)
                if camino:
                    distancias[i][j] = destino.DijkstraDistance
                    caminos[i][j] = camino
                else:
                    distancias[i][j] = math.inf

    visitado = [False]*num_visitas
    visitado[0] = True

    camino_actual = []
    distancia_actual = 0

    def backtrack(visita_actual, nivel):
        nonlocal mejor_distancia, mejor_camino, distancia_actual

        if nivel == num_visitas - 1:
            if distancias[visita_actual][num_visitas - 1] == math.inf:
                return  # no existe camino final
            distancia_total = distancia_actual + distancias[visita_actual][num_visitas - 1]
            if distancia_total < mejor_distancia:
                mejor_distancia = distancia_total
                mejor_camino = camino_actual + caminos[visita_actual][num_visitas - 1]
            return

        for siguiente_visita in range(1, num_visitas - 1):
            if not visitado[siguiente_visita] and distancias[visita_actual][siguiente_visita] != math.inf:
                nueva_distancia = distancia_actual + distancias[visita_actual][siguiente_visita]
                if nueva_distancia >= mejor_distancia:
                    continue

                visitado[siguiente_visita] = True
                camino_actual.extend(caminos[visita_actual][siguiente_visita])
                distancia_actual = nueva_distancia

                backtrack(siguiente_visita, nivel + 1)

                for _ in caminos[visita_actual][siguiente_visita]:
                    camino_actual.pop()
                distancia_actual -= distancias[visita_actual][siguiente_visita]
                visitado[siguiente_visita] = False

    backtrack(0, 1)

    track_resultado = graph.Track(g)
    for arista in mejor_camino:
        track_resultado.AddLast(arista)

    return track_resultado

