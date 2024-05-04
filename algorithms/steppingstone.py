"""
Projet : PRJ-SM602 - Recherche Opérationnelle - 2023/2024 - Thème sur le problème de transport
Auteurs: KOCOGLU Lucas, BAUDET Antoine, HOUEE Adrien
Description: Ce fichier contient l'algorithme de la méthode de marche pied
Version de Python: 3.12
"""
from termcolor import colored

from algorithms.totalcost import totalcost
from display_tab import display_tab_matrix


def steppingstone(tab_matrix, complexity_bool=False):
    global complexity
    complexity = complexity_bool
    try:
        # Initialisation des variables
        num_provisions = len(tab_matrix[1])
        num_orders = len(tab_matrix[2])

        source_map = {f'P{i + 1}': i for i in range(num_provisions)}
        destination_map = {f'C{j + 1}': j for j in range(num_orders)}

        # Deep copy of the tab_matrix
        list_provisions = [tab_matrix[1][i] for i in range(0, num_provisions)]
        list_orders = [tab_matrix[2][j] for j in range(0, num_orders)]
        tab_matrix = [[[tab_matrix[0][i][j][0], tab_matrix[0][i][j][1]] for j in range(0, num_orders)] for i in
                      range(0, num_provisions)]

        graph = extract_graph(tab_matrix, num_provisions, num_orders)
        fictive_edge = []
        # Affichage de la proposition de transport initiale

        while True:
            graph = extract_graph(tab_matrix, num_provisions, num_orders)
            print(colored(graph, "yellow")) if not complexity else None if not complexity else None
            components = find_connected_components(graph)
            print(components) if not complexity else None
            if len(components) > 1:
                print(colored("The graph is not connected. Connecting the graph...",
                              "red")) if not complexity else None if not complexity else None
                graph, fictive_edge = connect_graph_components(graph, components, tab_matrix, source_map,
                                                               destination_map)
                print(colored("Graph connected successfully.",
                              "green")) if not complexity else None if not complexity else None
                print(colored(fictive_edge, "yellow")) if not complexity else None if not complexity else None
                print(colored(graph, "yellow")) if not complexity else None if not complexity else None
            else:
                print(
                    colored("The graph is connected.", "green")) if not complexity else None if not complexity else None

            # Find a cycle in the graph
            cycle = bfs_detect_cycle(graph, 'P1')
            if cycle:
                print("Cycle found:", cycle) if not complexity else None if not complexity else None
                # Transportation maximization if a cycle has been detected. The conditions for each box are displayed. Then we display the deleted edge (possibly several) at the end of maximization.
                maximize_transportation(tab_matrix, graph, cycle, source_map, destination_map)
                print("HIT maximize_transportation") if not complexity else None if not complexity else None
            else:
                print("No cycle found.") if not complexity else None if not complexity else None

            # Calculate potentials
            potentials_dict = calculate_potentials(tab_matrix, num_provisions, num_orders, graph)
            print("Potentials:", potentials_dict) if not complexity else None if not complexity else None

            # Calculate the matrix of potential costs
            matrix_potential = matrix_potential_cost(potentials_dict, num_provisions, num_orders)
            print("Potential cost matrix: ", matrix_potential) if not complexity else None if not complexity else None
            display_tab_matrix(matrix_potential, "Potential", "potential") if not complexity else None

            # Calculate marginal costs
            matrix_marginal = matrix_marginal_cost(tab_matrix, matrix_potential, num_provisions, num_orders)
            print("Marginal cost matrix: ", matrix_marginal) if not complexity else None if not complexity else None
            display_tab_matrix(matrix_marginal, "Marginal", "marginal") if not complexity else None

            # Proposition optimale ?
            if not all(marginal >= 0 for row in matrix_marginal for marginal in row):
                improved = False
                best_edge = find_best_improving_edge(matrix_marginal)
                print(
                    f"Trying edge: P{best_edge[0] + 1}C{best_edge[1] + 1} with marginal cost {matrix_marginal[best_edge[0]][best_edge[1]]}") if not complexity else None
                if improve_transport_proposal(tab_matrix, graph, best_edge, source_map, destination_map):
                    improved = True
                if not improved:
                    print(colored("No further improvements possible with any negative margins.",
                                  "red")) if not complexity else None if not complexity else None
                    break
            else:
                print("Optimal solution found.") if not complexity else None if not complexity else None
                break
            display_tab_matrix([tab_matrix, list_provisions, list_orders], "Step") if not complexity else None
            input("Press Enter to continue...") if not complexity else None

        return [tab_matrix, list_provisions, list_orders]
    except Exception as e:
        print(colored("Une erreur est survenue : " + str(e), "red")) if not complexity else None
        return None


def find_all_negative_margins(matrix_marginal):
    return [(i, j) for i in range(len(matrix_marginal)) for j in range(len(matrix_marginal[i])) if
            matrix_marginal[i][j] < 0]


def calculate_potentials(tab_matrix, num_provisions, num_orders, graph={}):
    # Initial potential values - Set the node C with the maximum number of edges to 0
    potentials = {}
    max_edges = max(len(edges) for edges in graph.values())
    for vertex, edges in graph.items():
        if len(edges) == max_edges:
            if vertex.startswith('C'):
                potentials[vertex] = 0
                break
    if not potentials:
        potentials['C1'] = 0

    # A simple system to calculate potentials could be based on starting from an arbitrary potential (e.g., P1)
    # and performing a series of updates based on the costs of moving between connected nodes.
    changes = True
    while changes:
        changes = False
        for i in range(num_provisions):
            if 'P' + str(i + 1) in potentials:
                for j in range(num_orders):
                    if tab_matrix[i][j][0] > 0 or (f'P{i + 1}' in graph and f'C{j + 1}' in graph[f'P{i + 1}']):
                        cost = tab_matrix[i][j][1]
                        if 'C' + str(j + 1) not in potentials:
                            """print(potentials) if not complexity else None
                            print(f"E(P{i + 1}) - E(C{j + 1}) = {cost}") if not complexity else None
                            print(colored(f"E(C{j + 1}) = E(P{i + 1}) - {cost}", attrs=["bold"]))"""
                            potentials['C' + str(j + 1)] = potentials['P' + str(i + 1)] - cost
                            changes = True
                        elif potentials['C' + str(j + 1)] != potentials['P' + str(i + 1)] - cost:
                            print(
                                f"Inconsistency found at C{j + 1}") if not complexity else None if not complexity else None

        for j in range(num_orders):
            if 'C' + str(j + 1) in potentials:
                for i in range(num_provisions):
                    if tab_matrix[i][j][0] > 0 or (f'C{j + 1}' in graph and f'P{i + 1}' in graph[f'C{j + 1}']):
                        cost = tab_matrix[i][j][1]
                        if 'P' + str(i + 1) not in potentials:
                            """print(potentials) if not complexity else None
                            print(f"E(P{i + 1}) - E(C{j + 1}) = {cost}") if not complexity else None
                            print(colored(f"E(P{i + 1}) = E(C{j + 1}) + {cost}", attrs=["bold"]))"""
                            potentials['P' + str(i + 1)] = potentials['C' + str(j + 1)] + cost
                            changes = True
                        # Check for inconsistencies: P(i) - C(j) = cost
                        elif potentials['P' + str(i + 1)] != potentials['C' + str(j + 1)] + cost:
                            print(
                                f"Inconsistency found at P{i + 1}") if not complexity else None if not complexity else None

    # Print all calculated potentials if not complexity else None
    for vertex, potential in potentials.items():
        print(f"Potential for E({vertex}): {potential}") if not complexity else None if not complexity else None

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
    """ Use a BFS to detect a cycle including start node """
    from collections import deque
    visited = set()
    parent = {}
    queue = deque([(start_vertex, None)])

    while queue:
        current, pred = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        for neighbor in graph[current]:
            if neighbor not in visited:
                parent[neighbor] = current
                queue.append((neighbor, current))
            elif neighbor != pred:
                # Cycle found
                cycle_path = []
                step = current
                while step != neighbor:
                    cycle_path.append(step)
                    step = parent[step]
                cycle_path.append(neighbor)
                cycle_path.append(current)
                return cycle_path
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


def improve_transport_proposal(tab_matrix, graph, best_edge, source_map, destination_map):
    # Deep copy of graph to avoid modifying the original
    graph = {vertex: neighbors[:] for vertex, neighbors in graph.items()}

    # Temporarily modify the graph to include the potential edge for cycle detection
    start_vertex, end_vertex = f'C{best_edge[1] + 1}', f'P{best_edge[0] + 1}'
    graph[start_vertex].append(end_vertex)
    graph[end_vertex].append(start_vertex)

    # Detect cycle including the temporary edge
    cycle = detect_cycle_including_edge(graph, start_vertex, end_vertex)

    if not cycle:
        print("No cycle found including the edge, check the edge detection logic.") if not complexity else None
        return

    # Reorder the cycle to start with a consumer and ensure correct alternation
    ordered_cycle = reorder_cycle(graph, cycle, best_edge)

    print("Ordered cycle:", ordered_cycle) if not complexity else None

    # Remove the temporary edge
    graph[start_vertex].remove(end_vertex)
    graph[end_vertex].remove(start_vertex)

    # Calculate the maximum delta that can be applied to this cycle
    delta = calculate_delta(tab_matrix, ordered_cycle)
    print(f"Maximum delta for the cycle: {delta}") if not complexity else None
    if delta is None or delta <= 0:
        print("No positive delta available to optimize the transport.") if not complexity else None
        return False

    # Apply delta adjustments along the reordered cycle
    if not apply_cycle_delta(tab_matrix, ordered_cycle, delta, source_map, destination_map, graph):
        print("Error applying cycle adjustments.") if not complexity else None
        return False

    # Print the updated matrix to check improvements if not complexity else None
    print("Updated transport matrix with improved cycle:") if not complexity else None
    for row in tab_matrix:
        print(row) if not complexity else None
    return True


def apply_cycle_delta(tab_matrix, ordered_cycle, delta, source_map, destination_map, graph):
    add = True  # Start with addition for the first element, adjust this logic if needed based on cycle direction

    for i in range(len(ordered_cycle) - 1):
        from_node = ordered_cycle[i]
        to_node = ordered_cycle[i + 1]

        if 'P' in from_node and 'C' in to_node:
            from_index = source_map[from_node] if 'P' in from_node else destination_map[from_node]
            to_index = destination_map[to_node] if 'C' in to_node else source_map[to_node]
        else:
            from_index = source_map[to_node] if 'P' in to_node else destination_map[to_node]
            to_index = destination_map[from_node] if 'C' in from_node else source_map[from_node]

        print(
            f"Adjusting shipment from {from_node} to {to_node} by delta {delta}, add: {add}") if not complexity else None
        print(f"Current shipment: {tab_matrix[from_index][to_index][0]}", from_index,
              to_index) if not complexity else None

        # Check to ensure we are not subtracting where the shipment is zero or less than delta
        if tab_matrix[from_index][to_index][0] - delta < 0 and not add:
            print(
                f"Attempt to subtract delta from an edge with insufficient shipment: {from_node} to {to_node}") if not complexity else None
            return False

        # Apply delta
        if add:
            tab_matrix[from_index][to_index][0] += delta
        else:
            tab_matrix[from_index][to_index][0] -= delta
            # Remove the edge if the shipment is zero
            if tab_matrix[from_index][to_index][0] == 0:
                if graph[from_node].count(to_node) > 0:
                    graph[from_node].remove(to_node) if to_node in graph[from_node] else None
                    graph[to_node].remove(from_node) if from_node in graph[to_node] else None

        add = not add  # Alternate between addition and subtraction

        # Error check moved to a safer place before modification
        if tab_matrix[from_index][to_index][0] < 0:
            print(
                f"Attempt to subtract delta from an edge with insufficient shipment: {from_node} to {to_node}") if not complexity else None
            return False

    return True


def calculate_delta(tab_matrix, ordered_cycle):
    delta = float('inf')  # Start with the largest possible value
    for i in range(len(ordered_cycle) - 1):
        from_node = ordered_cycle[i]
        to_node = ordered_cycle[i + 1]

        # Extract indices from node labels
        if 'P' in from_node and 'C' in to_node:
            from_index = int(from_node[1:]) - 1
            to_index = int(to_node[1:]) - 1
        else:
            from_index = int(to_node[1:]) - 1
            to_index = int(from_node[1:]) - 1

        # Check if we need to reduce this edge
        if needs_reduction(i):  # Assuming a simple alternation
            shipment = tab_matrix[from_index][to_index][0]
            if shipment > 0:  # Consider only positive shipments for reduction
                delta = min(delta, shipment)

    if delta == float('inf') or delta <= 0:
        # If delta is still inf, it means no eligible edge was found or all shipments were zero
        print("No positive shipment found for reduction or incorrect cycle path.") if not complexity else None
        return None  # Returning 0 or another suitable fallback value

    return delta


def needs_reduction(index):
    return index % 2 == 1


def reorder_cycle(graph, cycle, best_edge):
    print("Reordering cycle : ", cycle) if not complexity else None
    # Find the first node with double occurrence or use the first node
    cycle_count = {node: cycle.count(node) for node in cycle}
    print("Cycle count : ", cycle_count) if not complexity else None
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
            print(f"Checking edge from {current_node} to {next_node}") if not complexity else None
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

    best_edge_tuple = (f'P{best_edge[0] + 1}', f'C{best_edge[1] + 1}')
    for i in range(len(reordered_cycle) - 1):
        if reordered_cycle[i] == best_edge_tuple[1] and reordered_cycle[i + 1] == best_edge_tuple[0]:
            reordered_cycle.reverse()
            break

    return reordered_cycle


def test_connectivity(graph):
    components = find_connected_components(graph)
    if len(components) == 1:
        print("The graph is connected.") if not complexity else None
    else:
        print("The graph is not connected. Here are the connected components:") if not complexity else None
        for i, component in enumerate(components, 1):
            print(f"Component {i}: {component}") if not complexity else None


def find_connected_components(graph):
    visited = set()
    components = []

    # Helper function to perform BFS
    def bfs(start):
        queue = [start]
        connected_component = []
        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)
                connected_component.append(node)
                # Enqueue all unvisited adjacent nodes
                queue.extend([n for n in graph[node] if n not in visited])
        return connected_component

    # Main loop to start BFS from all unvisited nodes
    for node in graph:
        if node not in visited:
            component = bfs(node)
            components.append(component)

    return components


def connect_graph_components(graph, components, tab_matrix, source_map, destination_map, fictive_edges=[]):
    # Initial check if the graph is already a tree
    if len(components[0]) - 1 == len(graph) - len(components):
        print("The graph is already optimally connected as a tree.") if not complexity else None
        return graph, fictive_edges

    for edge in fictive_edges:
        graph.setdefault(edge[0], []).append(edge[1]) if edge[1] not in graph[edge[0]] else None
        graph.setdefault(edge[1], []).append(edge[0]) if edge[0] not in graph[edge[1]] else None

    # Check again if adding fictive edges has connected the graph as a tree
    components = find_connected_components(graph)
    if len(components[0]) - 1 == len(graph) - len(components):
        print("The graph is already optimally connected as a tree.") if not complexity else None
        return graph, fictive_edges

    base_component = components[0]  # Use the first component as the base

    # Connect each other component to the base
    for other_component in components[1:]:
        min_cost = float('inf')
        best_connection = None

        # Check connections both from P to C and C to P
        for base_node in base_component:
            for other_node in other_component:
                # Determine if base_node is P and other_node is C or vice versa
                if base_node.startswith('P') and other_node.startswith('C'):
                    p_index = source_map[base_node]
                    c_index = destination_map[other_node]
                elif base_node.startswith('C') and other_node.startswith('P'):
                    p_index = source_map[other_node]
                    c_index = destination_map[base_node]
                else:
                    continue  # Skip if the pairing is not between P and C

                edge_cost = tab_matrix[p_index][c_index][1]
                print(
                    f"Checking connection from {base_node} to {other_node}, cost: {edge_cost}") if not complexity else None

                # Check for the minimum cost connection
                if edge_cost < min_cost:
                    min_cost = edge_cost
                    best_connection = (base_node, other_node)

        # Connect the best nodes found
        if best_connection:
            p, c = best_connection
            graph.setdefault(p, []).append(c)
            graph.setdefault(c, []).append(p)
            print(f"Connecting {p} to {c} with cost {min_cost}") if not complexity else None
            fictive_edges.append([p, c])

    return graph, fictive_edges


def maximize_transportation(tab_matrix, graph, cycle, source_map, destination_map):
    if not cycle:
        print("No cycle found. No maximization possible.") if not complexity else None
        return

    print("Cycle detected for maximization: ", cycle) if not complexity else None

    # Calculate the minimum shipment in the detected cycle that can be adjusted
    delta = calculate_delta(tab_matrix, cycle)
    print(f"Delta for adjustment: {delta}") if not complexity else None

    if delta <= 0:
        print("No adjustment possible, all shipments are at minimum in the cycle.") if not complexity else None
        return

    # Apply the cycle adjustment: alternating between subtraction and addition
    adjust_shipments(tab_matrix, cycle, delta, source_map, destination_map)

    # Print updated matrix and check for any zero shipments (deleted edges
    print("Updated transportation matrix after maximization:") if not complexity else None
    deleted_edges = []
    for i in range(len(cycle) - 1):
        from_node = cycle[i]
        to_node = cycle[i + 1]
        from_index, to_index = get_indices(from_node, to_node, source_map, destination_map)
        shipment = tab_matrix[from_index][to_index][0]
        print(f"{from_node} -> {to_node}: {shipment}") if not complexity else None
        if shipment == 0:
            deleted_edges.append((from_node, to_node))

    if deleted_edges:
        print("Deleted edges after maximization:") if not complexity else None
        for edge in deleted_edges:
            print(f"{edge[0]} -> {edge[1]}") if not complexity else None
    else:
        print("No edges deleted.") if not complexity else None


def get_indices(from_node, to_node, source_map, destination_map):
    # Helper function to get indices from node labels
    from_index = source_map.get(from_node, destination_map.get(from_node))
    to_index = destination_map.get(to_node, source_map.get(to_node))
    return from_index, to_index


def adjust_shipments(tab_matrix, cycle, delta, source_map, destination_map):
    # Apply adjustments in a cycle based on calculated delta
    add = True  # Start with subtraction according to cycle's direction
    for i in range(len(cycle) - 1):
        from_node = cycle[i]
        to_node = cycle[i + 1]
        from_index, to_index = get_indices(from_node, to_node, source_map, destination_map)

        if add:
            tab_matrix[from_index][to_index][0] += delta
        else:
            tab_matrix[from_index][to_index][0] -= delta

        add = not add  # Alternate between addition and subtraction
