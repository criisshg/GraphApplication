import graph
import math
import sys
import queue


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
	if start is not None:
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
			if vActual == None:
				break



# DijkstraQueue ================================================================

def DijkstraQueue(g, start):
    # Inicializar las distancias a infinito
    for vertice in g.Vertices:
        vertice.DijkstraDistance = sys.float_info.max

    # Inicializamos el diccionario de vertices visitados con las distancias
    DijkstraVisit = {vertice: False for vertice in g.Vertices}
    DijkstraVisit[start] = False
    start.DijkstraDistance = 0.0

    # Inicializamos la cola con el vertice inicial
    cola = [start]

    while cola:
        vActual = cola.pop(0)

        # Si el vertice no ha sido visitado
        # Para cada vecino del vertice desencolado
        for aresta in vActual.Edges:
            vecino = aresta.Destination
            distance = aresta.Length + vActual.DijkstraDistance

            # Si la distancia al vecino a través del vertice desencolado es menor que su distancia actual
            if distance < vecino.DijkstraDistance:
                # Actualizamos la distancia del vecino
                vecino.DijkstraDistance = distance

                # Encolamos el vecino
                cola.append(vecino)

        # Marcamos el vertice como visitado
        DijkstraVisit[vActual] = True