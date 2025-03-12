import graph
import math
import sys
import queue
import heapq

# Dijkstra =====================================================================

def Dijkstra(g, start):
    # Inicializar las distancias a infinito, excepto para el vértice de inicio
    for v in g.Vertices:
        v.DijkstraDistance = float('inf')
    g.GetVertex(start).DijkstraDistance = 0

    # Marcar todos los vértices como no visitados
    no_visitados = set(g.Vertices)

    while no_visitados:
        # Encontrar el vértice con la menor distancia que no ha sido visitado
        vActual = min(no_visitados, key=lambda v: v.DijkstraDistance)

        # Visitar todos los vértices adyacentes
        for e in vActual.Edges:
            vecino = e.Destination
            if vecino in no_visitados:
                # Calcular la posible distancia más corta
                nueva_distancia = vActual.DijkstraDistance + e.Length
                if nueva_distancia < vecino.DijkstraDistance:
                    vecino.DijkstraDistance = nueva_distancia

        # Marcar el vértice actual como visitado
        no_visitados.remove(vActual)

        # Si todos los vértices han sido visitados, salir del bucle
        if not no_visitados:
            break

    # Opcional: devolver las distancias si es necesario
    return {v.Name: v.DijkstraDistance for v in g.Vertices}


# DijkstraQueue ================================================================

# Queue needed
def DijkstraQueue(g, start):
    # Inicializar las distancias a infinito, excepto para el vértice de inicio
    for v in g.Vertices:
        v.DijkstraDistance = float('inf')
    start_vertex = g.GetVertex(start)
    start_vertex.DijkstraDistance = 0

    # Priority queue
    pq = queue.PriorityQueue()
    pq.put((0, start_vertex))

    visited = set()

    while not pq.empty():
        current_distance, vActual = pq.get()

        if vActual in visited:
            continue

        visited.add(vActual)

        for e in vActual.Edges:
            vecino = e.Destination
            new_distance = current_distance + e.Length

            if new_distance < vecino.DijkstraDistance:
                vecino.DijkstraDistance = new_distance
                pq.put((new_distance, vecino))

    return {v.Name: v.DijkstraDistance for v in g.Vertices}
"""
# Heapq needed

def DijkstraQueue(g, start):
    # Inicializar las distancias a infinito, excepto para el vértice de inicio
    for v in g.Vertices:
        v.DijkstraDistance = float('inf')
    start_vertex = g.GetVertex(start)
    start_vertex.DijkstraDistance = 0

    # Marcar todos los vértices como no visitados
    DijkstraVisit = {v: False for v in g.Vertices}

    # Crear la cola de prioridad y agregar el vértice inicial
    priority_queue = []
    heapq.heappush(priority_queue, (0, start_vertex))

    while priority_queue:
        # Extraer el vértice con la distancia más corta no visitado
        current_distance, vActual = heapq.heappop(priority_queue)

        if DijkstraVisit[vActual]:
            continue
        
        # Marcar el vértice como visitado
        DijkstraVisit[vActual] = True

        # Actualizar las distancias para cada vértice adyacente
        for e in vActual.Edges:
            vecino = e.Destination
            distancia = current_distance + e.Length

            if distancia < vecino.DijkstraDistance:
                vecino.DijkstraDistance = distancia
                heapq.heappush(priority_queue, (distancia, vecino))

    # Opcional: devolver las distancias si es necesario
    return {v.Name: v.DijkstraDistance for v in g.Vertices}
"""

