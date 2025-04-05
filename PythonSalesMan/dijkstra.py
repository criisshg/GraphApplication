import graph
import math
import sys
import heapq


# Dijkstra =====================================================================
def Dijkstra(g,start):
	# Inicializar las distancias a infinito
	for vertice in g.Vertices:
		vertice.DijkstraDistance = sys.float_info.max
	start.DijkstraDistance = 0.0

	#Inicializamos el diccionario de vertices visitados con las distancias
	DijkstraVisit = {vertice: math.inf for vertice in g.Vertices}

	vActual = start
	DijkstraVisit[vActual] = 0.0

	#Recorremos el diccionario hasta que no queden nodos por visitar
	if start is not None:  # Si el nodo inicial no es None, comenzamos el recorrido
		while DijkstraVisit:  
			for aresta in vActual.Edges:
				distancia = aresta.Length + DijkstraVisit[vActual]  
				vecino = aresta.Destination  
				if (vecino in DijkstraVisit) and (distancia < DijkstraVisit[vecino]):
					vecino.previousNode = vActual  
					vecino.previousEdge = aresta
					DijkstraVisit[vecino] = distancia

			#Actualizamos la distancia del vertice actual eliminandolo del diccionario que recorremos
			vActual.DijkstraDistance = DijkstraVisit.pop(vActual)

			#Buscamos el proximo vertice que sera el vecino con la menor distancia
			next_vecino = None
			dist_min = math.inf
			for vecino, dist in DijkstraVisit.items():
				if dist < dist_min:
					dist_min = dist
					next_vecino = vecino
			vActual = next_vecino
			if vActual == None:  # Si no hay más vecinos, salimos del bucle
				break



# DijkstraQueue ================================================================

def DijkstraQueue(g, start):
    # Inicializar distancias
    for vertice in g.Vertices:
        vertice.DijkstraDistance = sys.float_info.max
    
    start.DijkstraDistance = 0.0
    
    # Usar una cola de prioridad (heap)
    heap = []
    heapq.heappush(heap, (0.0, start))
    
    while heap:  # Mientras haya nodos por procesar
        current_dist, vActual = heapq.heappop(heap)
        
        # Si ya encontramos un camino mejor, ignorar este
        if current_dist > vActual.DijkstraDistance:
            continue
        # Si la distancia actual es mayor que la mejor conocida, ignorar
        for aresta in vActual.Edges:
            vecino = aresta.Destination
            distance = current_dist + aresta.Length
            
            # Actualizamos la distancia si encontramos un camino mejor
            if distance < vecino.DijkstraDistance:
                vecino.DijkstraDistance = distance
                vecino.previousNode = vActual
                vecino.previousEdge = aresta
                heapq.heappush(heap, (distance, vecino))