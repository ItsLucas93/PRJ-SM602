"""
Projet : PRJ-SM602 - Recherche Opérationnelle - 2023/2024 - Thème sur le problème de transport
Auteurs: KOCOGLU Lucas, BAUDET Antoine, HOUEE Adrien
Description: Ce fichier contient l'algorithme de la méthode de marche pied
Version de Python: 3.12
"""
from termcolor import colored

from algorithms.totalcost import totalcost
from display_tab import display_tab_matrix
from collections import deque


def steppingstone(tab_matrix):
    try:
        print(tab_matrix)
        # Initialisation des variables
        num_provisions = len(tab_matrix[1])
        num_orders = len(tab_matrix[2])

        source_map = {f'P{i+1}': i for i in range(num_provisions)}
        destination_map = {f'C{j+1}': j for j in range(num_orders)}

        # Deep copy of the tab_matrix
        list_provisions = [tab_matrix[1][i] for i in range(0, num_provisions)]
        list_orders = [tab_matrix[2][j] for j in range(0, num_orders)]
        tab_matrix = [[[tab_matrix[0][i][j][0], tab_matrix[0][i][j][1]] for j in range(0, num_orders)] for i in range(0, num_provisions)]

        graph = extract_graph(tab_matrix, num_provisions, num_orders)
        # Affichage de la proposition de transport initiale
        print(totalcost([tab_matrix, list_provisions, list_orders]))

        while True:
            # Find a cycle in the graph
            cycle = bfs_detect_cycle(graph, 'P1')
            print(cycle)

            # Calculate potentials
            potentials_dict = calculate_potentials(tab_matrix, num_provisions, num_orders)
            print(potentials_dict)

            potentials_list = separate_potentials(potentials_dict)
            print(potentials_list)

            # Calculate the matrix of potential costs
            matrix_potential = matrix_potential_cost(potentials_dict, num_provisions, num_orders)
            print(matrix_potential)
            display_tab_matrix(matrix_potential, "Potential", "potential")

            # Calculate marginal costs
            matrix_marginal = matrix_marginal_cost(tab_matrix, matrix_potential, num_provisions, num_orders)
            print(matrix_marginal)
            display_tab_matrix(matrix_marginal, "Marginal", "marginal")

            # Proposition optimale ?
            if not all(marginal >= 0 for row in matrix_marginal for marginal in row):
                print("Not an optimal solution.")
                best_edge = find_best_improving_edge(matrix_marginal)
                if best_edge is not None:
                    print(f"Best edge to improve: P{best_edge[0] + 1}C{best_edge[1] + 1}")
                    improve_transport_proposal(tab_matrix, num_provisions, num_orders, best_edge, source_map, destination_map)
            else:
                print("Optimal solution found.")
                break
            display_tab_matrix([tab_matrix, list_provisions, list_orders], "Step")
            input("Press Enter to continue...")

        return [tab_matrix, list_provisions, list_orders]
    except Exception as e:
        print(colored("Une erreur est survenue : " + str(e), "red"))
        return None


def calculate_potentials(tab_matrix, num_provisions, num_orders):
    # Initial potential values (can initialize arbitrarily, here setting source 1 to potential 0)
    potentials = {'C1': 0}

    # A simple system to calculate potentials could be based on starting from an arbitrary potential (e.g., P1)
    # and performing a series of updates based on the costs of moving between connected nodes.
    changes = True
    while changes:
        changes = False
        for i in range(num_provisions):
            if 'P' + str(i + 1) in potentials:
                for j in range(num_orders):
                    if tab_matrix[i][j][0] > 0:
                        cost = tab_matrix[i][j][1]
                        if 'C' + str(j + 1) not in potentials:
                            # print(potentials)
                            # print(f"E(P{i + 1}) - E(C{j + 1}) = {cost}")
                            # print(colored(f"E(C{j + 1}) = E(P{i + 1}) - {cost}", attrs=["bold"]))
                            potentials['C' + str(j + 1)] = potentials['P' + str(i + 1)] - cost
                            changes = True
                        elif potentials['C' + str(j + 1)] != potentials['P' + str(i + 1)] - cost:
                            print(f"Inconsistency found at C{j+1}")

        for j in range(num_orders):
            if 'C' + str(j + 1) in potentials:
                for i in range(num_provisions):
                    if tab_matrix[i][j][0] > 0:
                        cost = tab_matrix[i][j][1]
                        if 'P' + str(i + 1) not in potentials:
                            # print(potentials)
                            # print(f"E(P{i + 1}) - E(C{j + 1}) = {cost}")
                            # print(colored(f"E(P{i + 1}) = E(C{j + 1}) + {cost}", attrs=["bold"]))
                            potentials['P' + str(i + 1)] = potentials['C' + str(j + 1)] + cost
                            changes = True
                        elif potentials['P' + str(i + 1)] != potentials['C' + str(j + 1)] + cost:
                            print(f"Inconsistency found at P{i+1}")

    # Print all calculated potentials
    # for vertex, potential in potentials.items():
    #     print(f"Potential for E({vertex}): {potential}")

    return potentials


def matrix_potential_cost(potentials, num_provisions, num_orders):
    # Initialize the matrix of potential costs
    potential_cost_matrix = [[0 for _ in range(num_orders)] for _ in range(num_provisions)]

    for i in range(num_provisions):
        for j in range(num_orders):
            potential_cost_matrix[i][j] = potentials['P' + str(i + 1)] - potentials['C' + str(j + 1)]
    return potential_cost_matrix


def matrix_marginal_cost(tab_matrix, matrix_potentials, num_provisions, num_orders):
    # Initialize the matrix of marginal costs
    marginal_cost_matrix = [[0 for _ in range(num_orders)] for _ in range(num_provisions)]

    for i in range(num_provisions):
        for j in range(num_orders):
            marginal_cost_matrix[i][j] = tab_matrix[i][j][1] - matrix_potentials[i][j]
    return marginal_cost_matrix


def separate_potentials(potentials):
    # Initialize lists for suppliers (P) and consumers (C)
    P = []
    C = []

    # Iterate over the potentials dictionary
    for vertex, value in potentials.items():
        if vertex.startswith('P'):  # Check if the key starts with 'P' for suppliers
            # Append the potential to the suppliers list
            # Convert vertex label 'P1', 'P2', ... to index 0, 1, ... for list
            index = int(vertex[1:]) - 1  # Convert 'P1' to 0, 'P2' to 1, etc.
            # Ensure the list is long enough
            if len(P) <= index:
                P.extend([None] * (index + 1 - len(P)))
            P[index] = value
        elif vertex.startswith('C'):  # Check if the key starts with 'C' for consumers
            # Append the potential to the consumers list
            # Convert vertex label 'C1', 'C2', ... to index 0, 1, ... for list
            index = int(vertex[1:]) - 1  # Convert 'C1' to 0, 'C2' to 1, etc.
            # Ensure the list is long enough
            if len(C) <= index:
                C.extend([None] * (index + 1 - len(C)))
            C[index] = value

    return [P, C]


def find_best_improving_edge(marginal_costs):
    min_cost = float('inf')
    best_edge = None
    for i in range(len(marginal_costs)):
        for j in range(len(marginal_costs[i])):
            if marginal_costs[i][j] < min_cost:
                min_cost = marginal_costs[i][j]
                best_edge = (i, j)
    return best_edge


def extract_graph(tab_matrix, num_provisions, num_orders):
    graph = {}

    # Initialize the graph dictionary
    for i in range(num_provisions):
        graph[f'P{i + 1}'] = []
    for j in range(num_orders):
        graph[f'C{j + 1}'] = []

    # Fill the graph with edges based on tab_matrix non-zero entries
    for i in range(num_provisions):
        for j in range(num_orders):
            if tab_matrix[i][j][0] > 0:  # If there's a shipment from Pi to Cj
                graph[f'P{i + 1}'].append(f'C{j + 1}')
                graph[f'C{j + 1}'].append(f'P{i + 1}')  # Add both directions for undirected graph

    return graph


def bfs_detect_cycle(graph, start_vertex):
    visited = {}
    parent = {}
    queue = []

    # Initialize visited and parent dictionaries
    for vertex in graph:
        visited[vertex] = False
        parent[vertex] = None

    # Start BFS from the given start vertex
    queue.append((start_vertex, None))

    while queue:
        current, pred = queue.pop(0)  # Dequeue the first element

        if visited[current]:
            continue

        visited[current] = True
        parent[current] = pred

        for neighbor in graph[current]:
            if not visited[neighbor]:
                queue.append((neighbor, current))
            elif neighbor != pred:  # Found a cycle
                # Cycle detected, print cycle
                cycle = []
                step = current
                while step != neighbor:
                    cycle.append(step)
                    step = parent[step]
                cycle.append(neighbor)
                cycle.append(current)
                print("Cycle detected:", cycle)
                return cycle

    return None


def detect_cycle_including_edge(graph, start_vertex, end_vertex):
    visited = {}
    parent = {}
    queue = []

    # Initialize visited and parent dictionaries
    for vertex in graph:
        visited[vertex] = False
        parent[vertex] = None

    # Start BFS from the start_vertex
    queue.append(start_vertex)
    visited[start_vertex] = True
    parent[start_vertex] = None

    while queue:
        current = queue.pop(0)  # Dequeue the first element

        # Explore each neighbor
        for neighbor in graph[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                parent[neighbor] = current
                queue.append(neighbor)
            elif neighbor != parent[current]:
                # A cycle is detected
                if current == end_vertex or neighbor == end_vertex:
                    # Verify the cycle includes both the start and end vertex
                    cycle = []
                    # Trace the cycle starting from current
                    trace_back = current
                    while trace_back is not None:
                        cycle.append(trace_back)
                        trace_back = parent[trace_back]

                    # Trace from neighbor to start to ensure it forms a complete loop
                    trace_back = neighbor
                    while trace_back is not None and trace_back not in cycle:
                        cycle.append(trace_back)
                        trace_back = parent[trace_back]

                    # Close the cycle if it's valid
                    if start_vertex in cycle and end_vertex in cycle:
                        cycle.append(current)  # To make the cycle complete
                        return cycle[::-1]  # Reverse to start with the start_vertex

    return None  # No cycle found that includes the given edge


def improve_transport_proposal(tab_matrix, num_provisions, num_orders, best_edge, source_map, destination_map):
    # Extract and prepare the graph
    graph = extract_graph(tab_matrix, num_provisions, num_orders)

    # Temporarily modify the graph to include the potential edge for cycle detection
    start_vertex, end_vertex = f'C{best_edge[1] + 1}', f'P{best_edge[0] + 1}'
    graph[start_vertex].append(end_vertex)
    graph[end_vertex].append(start_vertex)

    # Detect cycle including the temporary edge
    cycle = detect_cycle_including_edge(graph, start_vertex, end_vertex)

    if not cycle:
        print("No cycle found including the edge, check the edge detection logic.")
        return

    # Reorder the cycle to start with a consumer and ensure correct alternation
    ordered_cycle = reorder_cycle(graph, cycle, best_edge)

    print("Ordered cycle:", ordered_cycle)

    # Remove the temporary edge
    graph[start_vertex].remove(end_vertex)
    graph[end_vertex].remove(start_vertex)

    # Calculate the maximum delta that can be applied to this cycle
    delta = calculate_delta(tab_matrix, ordered_cycle)
    print(f"Maximum delta for the cycle: {delta}")
    if delta <= 0:
        print("No positive delta available to optimize the transport.")
        return

    # Apply delta adjustments along the reordered cycle
    apply_cycle_delta(tab_matrix, ordered_cycle, delta, source_map, destination_map)

    # Print the updated matrix to check improvements
    print("Updated transport matrix with improved cycle:")
    for row in tab_matrix:
        print(row)


def apply_cycle_delta(tab_matrix, ordered_cycle, delta, source_map, destination_map):
    add = True  # Start with addition for the first element, adjust this logic if needed based on cycle direction

    for i in range(len(ordered_cycle) - 1):
        from_node = ordered_cycle[i]
        to_node = ordered_cycle[i + 1]

        from_index = source_map[from_node] if 'P' in from_node else destination_map[from_node]
        to_index = destination_map[to_node] if 'C' in to_node else source_map[to_node]

        # Check to ensure we are not subtracting where the shipment is zero or less than delta
        if tab_matrix[from_index][to_index][0] - delta < 0 and not add:
            raise ValueError(f"Attempt to subtract delta from an edge with insufficient shipment: {from_node} to {to_node}")

        # Apply delta
        if add:
            tab_matrix[from_index][to_index][0] += delta
        else:
            tab_matrix[from_index][to_index][0] -= delta

        add = not add  # Alternate between addition and subtraction

        # Error check moved to a safer place before modification
        if tab_matrix[from_index][to_index][0] < 0:
            raise ValueError(f"Negative shipment amount detected at edge ({from_node}, {to_node}) after applying delta")


def calculate_delta(tab_matrix, cycle):
    delta = float('inf')
    # Iterate over edges in the cycle
    for index in range(len(cycle) - 1):
        from_node, to_node = int(cycle[index][1:]) - 1, int(cycle[index + 1][1:]) - 1
        if needs_reduction(cycle, index):
            shipment = tab_matrix[from_node][to_node][0]
            print(f"Checking edge from {cycle[index]} to {cycle[index + 1]} with shipment {shipment}")
            if shipment == 0:
                continue
            else:
                delta = min(delta, shipment)

    if delta == float('inf') or delta == 0:
        print("No positive shipment found for reduction or incorrect cycle path.")
    return delta


def needs_reduction(cycle, index):
    # Determine the direction of flow and whether reduction is needed
    # This example assumes a simple alternation of addition and reduction
    return index % 2 == 0  # Assuming every alternate edge in the cycle needs a reduction


def reorder_cycle(graph, cycle, best_edge):
    print("Reordering cycle : ", cycle)
    # Find the first node with double occurrence or use the first node
    cycle_count = {node: cycle.count(node) for node in cycle}
    print("Cycle count : ", cycle_count)
    start_node = None
    for node, count in cycle_count.items():
        if count > 1:
            start_node = node
            break

    if not start_node:
        start_node = cycle[0]  # fallback to the first node if no doubles found

    # Initialize the reordered cycle
    reordered_cycle = []
    visited = set()
    current_node = start_node
    best_edge_visited = False

    # Use a set to manage visited nodes to prevent loops
    while len(reordered_cycle) < len(cycle):
        reordered_cycle.append(current_node)
        visited.add(current_node)

        # Get the next node in the cycle that is connected and not visited
        for next_node in graph[current_node]:
            print(f"Checking edge from {current_node} to {next_node}")
            if not best_edge_visited and current_node == f'P{best_edge[0] + 1}' and next_node == f'C{best_edge[1] + 1}':
                best_edge_visited = True
                current_node = next_node
                break
            elif next_node in cycle and next_node not in visited:
                current_node = next_node
                break
        else:
            # If no unvisited connected nodes, break the loop to avoid infinite loops
            break

    # Close the cycle by appending the start node if necessary
    if reordered_cycle and reordered_cycle[0] != reordered_cycle[-1]:
        reordered_cycle.append(reordered_cycle[0])

    return reordered_cycle

