import graph
import math
import sys
import queue
import dijkstra

def SalesmanTrackBacktracking(g, visits):
    """
    Algoritmo de backtracking para resolver el problema del vendedor viajero.
    Encuentra el camino más corto que visita todos los vértices de 'visits' en el grafo 'g'.
    """
    # Listas mutables de 1 elemento para mutar en la función recursiva
    mejor_camino    = [None]
    mejor_distancia = [math.inf]
    
    origen = visits.Vertices[0]
    destino = visits.Vertices[-1]
    visitas_intermedias = set(visits.Vertices[1:-1]) # Vertices visitados intermedios

    camino_actual = []
    
    def backtrack(v_actual, dist_actual, pendientes, visitados_tramo):
        """
        FUnción recursiva para explorar caminos posibles.
        """
        # Llegar a una visita pendiente
        if v_actual in pendientes:
            pendientes = pendientes - {v_actual}
            visitados_tramo = set()  # Reset visitas del tramo

        # Comprobación de Caso Base (Fin del Camino)
        if v_actual == destino and not pendientes:
            if dist_actual < mejor_distancia[0]:
                mejor_camino[0] = camino_actual[:]
                mejor_distancia[0] = dist_actual
            return
        
        # Explorar vecinos
        for arista in v_actual.Edges:
            # verifica si el destino del arco no ha sido visitado en este tramo
            vecino = arista.Destination
            if vecino not in visitados_tramo:
                # Se añade vecino ya visitado al camino actual
                camino_actual.append(arista)
                visitados_tramo.add(vecino)

                # Llamada recursiva a backtrackinf con la nueva/mejor distancia
                nueva_distancia = dist_actual + arista.Length
                if nueva_distancia < mejor_distancia[0]:
                    backtrack(vecino, nueva_distancia, pendientes, visitados_tramo)

                # Retroceder al estado anterior y siguiente ruta
                camino_actual.pop()
                visitados_tramo.remove(vecino)

    # Llamada inicial a backtracking con distancia 0 i tramo vacío (solo origen)
    visitados_tramo = set([origen])
    backtrack(origen, 0, visitas_intermedias, visitados_tramo)


    track_resultado = graph.Track(g) 
    if mejor_camino[0] is not None:
        for arista in mejor_camino[0]:
            track_resultado.AddLast(arista)

    return track_resultado # camino completo más corto encontrado

# ==============================================================================

def reconstruir_camino(origen, destino):
    """
    Reconstruye el camino desde el origen hasta el destino utilizando 
    la información de DijkstraQueue.
    """
    camino = []
    actual = destino
    while actual != origen:
        if actual.previousEdge is None:
            return []  # No existe camino
        camino.append(actual.previousEdge)
        actual = actual.previousNode # Retrocede hasta origen
    camino.reverse() # Invierte para orden correcto
    return camino

def SalesmanTrackBacktrackingGreedy(g, visits):
    """
    Solución exacta al TSP sobre la lista 'visits' usando pre-cálculo con Dijkstra
    y backtracking para ordenar las visitas intermedias.
    """
    n = len(visits.Vertices) # n es num_visitas

    # Caso simple (solo origen y destino: Dijkstra + reconstrucción)
    if n == 2:
        dijkstra.DijkstraQueue(g, visits.Vertices[0])
        camino_simple = reconstruir_camino(visits.Vertices[0], visits.Vertices[1])

        track_resultado = graph.Track(g)
        for arista in camino_simple:
            track_resultado.AddLast(arista)
        return track_resultado # Track continee origen y destino
    
    # Contenedores mutables
    mejor_distancia = [math.inf]   # mejor_distancia[0] guarda la mínima encontrada
    mejor_camino    = [[]]         # mejor_camino[0] guarda el camino mínimo encontrado

    # Inicializa matrices de distancias y caminos
    distancias = [[math.inf]*n for _ in range(n)]
    caminos = [[[] for _ in range(n)] for _ in range(n)]

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

    # Estado de backtracking
    visitado = [False]*n
    visitado[0] = True          # marcamos origen como ya “visitado”
    camino_actual = []          # aristas del recorrido parcial
    distancia_actual = [0]      # acumulado de longitud en el tramo actual

    def backtrack(visita_actual, nivel):
        """Explora permutaciones de visitas intermedias, podando por distancia."""
        
        # Caso base: todas las intermedias cubiertas
        if nivel == n - 1:
            if distancias[visita_actual][n - 1] == math.inf:
                return  # no existe camino final
            distancia_total = distancia_actual[0] + distancias[visita_actual][n - 1]
            if distancia_total < mejor_distancia[0]:
                mejor_distancia[0] = distancia_total
                mejor_camino[0] = camino_actual + caminos[visita_actual][n - 1]
            return

        # Probar cada visita intermedia no visitada
        for sig_visita in range(1, n - 1):
            if not visitado[sig_visita] and distancias[visita_actual][sig_visita] != math.inf:
                nueva_distancia = distancia_actual[0] + distancias[visita_actual][sig_visita]
                if nueva_distancia >= mejor_distancia[0]:
                    continue

                # seleccionamos esa visita
                visitado[sig_visita] = True
                # añadimos el tramo precalculado
                camino_actual.extend(caminos[visita_actual][sig_visita])
                # Actualizamos distancia
                distancia_actual[0] = nueva_distancia

                backtrack(sig_visita, nivel + 1)

                # deshacemos cambios (backtrack)
                for _ in caminos[visita_actual][sig_visita]:
                    camino_actual.pop()
                distancia_actual[0] -= distancias[visita_actual][sig_visita]
                visitado[sig_visita] = False

    # Arrancamos la búsqueda desde el origen, nivel=1
    backtrack(0, 1)

    track_resultado = graph.Track(g) # creamos track con mejor solucion
    for arista in mejor_camino[0]:
        track_resultado.AddLast(arista)

    return track_resultado

