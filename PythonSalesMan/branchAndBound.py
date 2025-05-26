import graph
import math
import sys
import heapq
import dijkstra
   
# SalesmanTrackBranchAndBound1 ===================================================

def SalesmanTrackBranchAndBound1(g, visits):
    return graph.Track(g)


# SalesmanTrackBranchAndBound2 ===================================================

def SalesmanTrackBranchAndBound2(g, visits):
    # Creamos el Track vacío que devolveremos si no hay solución
    result_track = graph.Track(g)
    
    n = len(visits.Vertices)
    if n < 2:
        # Si solo hay un vértice o ninguno, no hay ruta que calcular
        return result_track

    # Lista de los vértices que debemos visitar (origen, intermedios, destino)
    required = visits.Vertices
    num_required = n

    # -------------------------------------------------------------------------
    # PRE-CÁLCULO: distancias mínimas y rutas entre cada par de vértices
    # dist[i][j] = coste mínimo de i a j
    # route[i][j] = lista de aristas que forman ese camino
    # -------------------------------------------------------------------------
    dist  = [[math.inf] * num_required for _ in range(num_required)]
    route = [[None]       * num_required for _ in range(num_required)]

    for i, ori in enumerate(required):
        # Ejecuto Dijkstra una vez por cada vértice como punto de partida
        dijkstra.DijkstraQueue(g, ori)
        for j, dest in enumerate(required):
            if i == j:
                # La distancia de un vértice a sí mismo es 0, el camino vacío
                dist[i][j]  = 0.0
                route[i][j] = []
            else:
                # Si dest es alcanzable, reconstruyo el camino
                if dest.DijkstraDistance < math.inf:
                    dist[i][j]  = dest.DijkstraDistance
                    # reconstrucción usando los punteros que dejó Dijkstra
                    path = []
                    curr = dest
                    while curr != ori:
                        e = curr.previousEdge
                        path.append(e)
                        curr = curr.previousNode
                    path.reverse()
                    route[i][j] = path
                else:
                    # si no es alcanzable, dejamos infinito y ruta None
                    dist[i][j]  = math.inf
                    route[i][j] = None

    # -------------------------------------------------------------------------
    # COMPROBACIÓN DE ACCESIBILIDAD
    # Si algún vértice no puede ser llegado desde ninguno de los demás,
    # no hay solución completa y salgo.
    # -------------------------------------------------------------------------
    for j in range(1, num_required):
        if all(dist[i][j] == math.inf for i in range(num_required) if i != j):
            return result_track

    # -------------------------------------------------------------------------
    # HEURÍSTICA INICIAL: cost mínimo entrante para cada vértice
    # Esto nos sirve para calcular una cota inferior (LB) rápida.
    # -------------------------------------------------------------------------
    min_to = [math.inf] * num_required
    for j in range(num_required):
        for i in range(num_required):
            if i != j and dist[i][j] < min_to[j]:
                min_to[j] = dist[i][j]

    start_idx = 0
    end_idx   = num_required - 1
    start_mask = 1 << start_idx  # bitmask que marca el inicio como visitado

    # Cálculo de la LB inicial: sumamos el coste mínimo entrante para
    # todos los vértices que aún no hemos visitado.
    initial_lb = sum(
        min_to[j]
        for j in range(num_required)
        if not (start_mask & (1 << j)) and min_to[j] < math.inf
    )
    initial_cost = 0.0

    # -------------------------------------------------------------------------
    # ESTRUCTURA DE RÁFAGA DE RAMIFICACIÓN Y PODA (Branch & Bound)
    # Usamos heapq para priorizar el nodo con menor LB
    # Cada entrada es (LB, coste_acumulado, índice_actual, máscara, camino_indices)
    # -------------------------------------------------------------------------
    pq = []
    heapq.heappush(pq, (initial_lb, initial_cost, start_idx, start_mask, [start_idx]))

    best_cost  = math.inf
    best_path  = None
    best_state = {}  # memoria para evitar re-explorar estados peores

    while pq:
        lb, cost, curr, mask, path = heapq.heappop(pq)
        # Si la LB ya excede la mejor solución encontrada, podemos detener
        if lb >= best_cost:
            break

        full_mask = (1 << num_required) - 1
        # Caso de finalización: máscara completa y estamos en el destino
        if mask == full_mask and curr == end_idx:
            if cost < best_cost:
                best_cost = cost
                best_path = path
            continue

        # ---------------------------------------------------------------------
        # Generar ramas: intentar visitar cada vértice no aún en la máscara
        # ---------------------------------------------------------------------
        for j in range(num_required):
            if mask & (1 << j):
                continue  # ya visitado
            # solo permitir visitar final_idx al final
            if j == end_idx and mask != (full_mask ^ (1 << end_idx)):
                continue
            d = dist[curr][j]
            if d == math.inf:
                continue
            new_cost = cost + d
            if new_cost >= best_cost:
                continue  # poda por coste
            new_mask = mask | (1 << j)
            # ajustamos LB: sustituimos la contribución de min_to[j] por la real d
            reduction = min_to[j] if min_to[j] < math.inf else 0.0
            new_lb = lb - reduction + d
            if new_lb >= best_cost:
                continue  # poda por LB

            state_key = (j, new_mask)
            prev_cost = best_state.get(state_key)
            if prev_cost is not None and prev_cost <= new_cost:
                continue  # ya vimos este estado con menor coste
            best_state[state_key] = new_cost

            # añadimos nueva rama a la cola
            heapq.heappush(pq, (new_lb, new_cost, j, new_mask, path + [j]))

    # Si no encontramos ningún camino válido, devolvemos vacío
    if best_path is None:
        return result_track

    # -------------------------------------------------------------------------
    # RECONSTRUIR EL Track FINAL a partir de best_path (lista de índices)
    # -------------------------------------------------------------------------
    for u, v in zip(best_path, best_path[1:]):
        segment = route[u][v]
        if segment is None:
            # falla la reconstrucción, devolvemos vacío
            return graph.Track(g)
        for e in segment:
            result_track.AddLast(e)

    return result_track



# SalesmanTrackBranchAndBound3 ===================================================

def SalesmanTrackBranchAndBound3(g, visits):
    return graph.Track(g)
	