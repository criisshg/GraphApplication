import graph
import math
import sys
import queue
import heapq

# Dijkstra =====================================================================

def Dijkstra(g, start):
    # Inicializar las distancias a infinito, excepto para el vértice de inicio
    for v in g.Vertices:
        v.DijkstraDistance = math.inf
    g.GetVertex(start).DijkstraDistance = 0

    # Marcar todos los vértices como no visitados
    DijkstraVisit = set(g.Vertices)

    while DijkstraVisit:
        # Encontrar el vértice con la menor distancia que no ha sido visitado
        vActual = min(DijkstraVisit, key=lambda v: v.DijkstraDistance)

        # Visitar todos los vértices adyacentes
        for v in vActual.Edges:
            vecino = v.Destination
            if vecino in DijkstraVisit:
                # Calcular la posible distancia más corta
                nueva_distancia = vActual.DijkstraDistance + v.Length
                if nueva_distancia < vecino.DijkstraDistance:
                    vecino.DijkstraDistance = nueva_distancia

        # Marcar el vértice actual como visitado
        DijkstraVisit.remove(vActual)
    

# DijkstraQueue ================================================================

# Queue needed
def DijkstraQueue(g, start):
    # Inicializar las distancias a infinito, excepto para el vértice de inicio
    for v in g.Vertices:
        v.DijkstraDistance = math.inf
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

        for v in vActual.Edges:
            vecino = v.Destination
            new_distance = current_distance + v.Length

            if new_distance < vecino.DijkstraDistance:
                vecino.DijkstraDistance = new_distance
                pq.put((new_distance, vecino))

        visited.add(vActual)

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
        for v in vActual.Edges:
            vecino = v.Destination
            distancia = current_distance + v.Length

            if distancia < vecino.DijkstraDistance:
                vecino.DijkstraDistance = distancia
                heapq.heappush(priority_queue, (distancia, vecino))

    # Opcional: devolver las distancias si es necesario
    return {v.Name: v.DijkstraDistance for v in g.Vertices}
"""

