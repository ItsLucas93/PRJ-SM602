"""
Projet : PRJ-SM602 - Recherche Opérationnelle - 2023/2024 - Thème sur le problème de transport
Auteurs: KOCOGLU Lucas, BAUDET Antoine, HOUEE Adrien
Description: Ce fichier contient l'algorithme de la méthode de marche pied
Version de Python: 3.12
"""

from termcolor import colored

from display_tab import display_tab_matrix


def steppingstone(tab_matrix, complexity_bool=False):
    """
    * Fonction : steppingstone
    * -----------------------
    * Cette fonction implémente l'algorithme de la méthode de marche pied pour résoudre le problème de transport.
    * Elle prend en paramètre la matrice des coûts de transport, et un booléen pour activer ou désactiver l'affichage
    * des étapes intermédiaires de l'algorithme.
    * Elle retourne la matrice des coûts de transport optimisée.
    * :param tab_matrix: La matrice des coûts de transport
    * :param complexity_bool: Booléen pour activer ou désactiver l'affichage des étapes intermédiaires
    * :return: La matrice des coûts de transport optimisée
    """
    # Initialisation de la variable
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
            components = find_connected_components(graph)
            if len(components) > 1:
                print(colored("Le graphe n'est pas connexe, connexion des composants...",
                              "red")) if not complexity else None if not complexity else None
                graph, fictive_edge = connect_graph_components(graph, components, tab_matrix, source_map,
                                                               destination_map)
                print(colored("Connexion des composants avec succès.",
                              "green")) if not complexity else None if not complexity else None
            else:
                print(
                    colored("Le graph est connecté", "green")) if not complexity else None if not complexity else None

            # Find a cycle in the graph
            cycle = bfs_detect_cycle(graph, 'P1')
            if cycle:
                print(colored("Présence de cycle: " + str(cycle),
                              "red")) if not complexity else None if not complexity else None
                # Transportation maximization if a cycle has been detected. The conditions for each box are displayed. Then we display the deleted edge (possibly several) at the end of maximization.
                maximize_transportation(tab_matrix, graph, cycle, source_map, destination_map)
            else:
                print(colored("Pas de cycle trouvé.", "green")) if not complexity else None if not complexity else None

            # Calculate potentials
            potentials_dict = calculate_potentials(tab_matrix, num_provisions, num_orders, graph)

            # Calculate the matrix of potential costs
            matrix_potential = matrix_potential_cost(potentials_dict, num_provisions, num_orders)
            display_tab_matrix(matrix_potential, "Potential", "potential") if not complexity else None

            # Calculate marginal costs
            matrix_marginal = matrix_marginal_cost(tab_matrix, matrix_potential, num_provisions, num_orders)
            display_tab_matrix(matrix_marginal, "Marginal", "marginal") if not complexity else None

            # Proposition optimale ?
            if not all(marginal >= 0 for row in matrix_marginal for marginal in row):
                improved = False
                best_edge = find_best_improving_edge(matrix_marginal)
                print(
                    f"Essai sur l'arrête : P{best_edge[0] + 1}C{best_edge[1] + 1} avec un coût marginal {matrix_marginal[best_edge[0]][best_edge[1]]}") if not complexity else None
                if improve_transport_proposal(tab_matrix, graph, best_edge, source_map, destination_map,
                                              list_provisions, list_orders):
                    improved = True
                if not improved:
                    print(colored("Aucune amélioration possible.", "red")) if not complexity else None
                    break
            else:
                print("Solution optimale trouvée.") if not complexity else None if not complexity else None
                break
            display_tab_matrix([tab_matrix, list_provisions, list_orders], "Step") if not complexity else None

        return [tab_matrix, list_provisions, list_orders]
    except Exception as e:
        print(colored("Une erreur est survenue : " + str(e), "red")) if not complexity else None
        return None


def find_all_negative_margins(matrix_marginal):
    """
    * Fonction : find_all_negative_margins
    * -------------------------------------
    * Cette fonction trouve toutes les marges négatives dans la matrice marginale.
    * Elle prend en paramètre la matrice marginale.
    * Elle retourne une liste de tuples contenant les indices des marges négatives.
    * :param matrix_marginal: La matrice marginale
    * :return: Une liste de tuples contenant les indices des marges négatives
    """
    return [(i, j) for i in range(len(matrix_marginal)) for j in range(len(matrix_marginal[i])) if
            matrix_marginal[i][j] < 0]


def calculate_potentials(tab_matrix, num_provisions, num_orders, graph={}):
    """
    * Fonction : calculate_potentials
    * --------------------------------
    * Cette fonction calcule les potentiels pour chaque nœud du graphe.
    * Elle prend en paramètre la matrice des coûts de transport, le nombre de fournisseurs, le nombre de commandes et le graphe.
    * Elle retourne un dictionnaire contenant les potentiels de chaque nœud.
    * :param tab_matrix: La matrice des coûts de transport
    * :param num_provisions: Le nombre de fournisseurs
    * :param num_orders: Le nombre de commandes
    * :param graph: Le graphe
    * :return: Un dictionnaire contenant les potentiels de chaque nœud
    """
    # Initialisation des potentiels avec un nœud arbitraire
    potentials = {}
    max_edges = max(len(edges) for edges in graph.values())
    for vertex, edges in graph.items():
        if len(edges) == max_edges:
            if vertex.startswith('C'):
                potentials[vertex] = 0
                break
    if not potentials:
        potentials['C1'] = 0

    # Initialisation des variables pour les changements
    # On continue tant qu'il y a des changements
    changes = True
    while changes:
        changes = False
        # Calcul des potentiels pour chaque nœud
        for i in range(num_provisions):
            if 'P' + str(i + 1) in potentials:
                for j in range(num_orders):
                    if tab_matrix[i][j][0] > 0 or (f'P{i + 1}' in graph and f'C{j + 1}' in graph[f'P{i + 1}']):
                        cost = tab_matrix[i][j][1]
                        # Vérifier si le nœud Cj a déjà un potentiel, sinon le calculer
                        if 'C' + str(j + 1) not in potentials:
                            """print(potentials) if not complexity else None
                            print(f"E(P{i + 1}) - E(C{j + 1}) = {cost}") if not complexity else None
                            print(colored(f"E(C{j + 1}) = E(P{i + 1}) - {cost}", attrs=["bold"]))"""
                            potentials['C' + str(j + 1)] = potentials['P' + str(i + 1)] - cost
                            changes = True
                        elif potentials['C' + str(j + 1)] != potentials['P' + str(i + 1)] - cost:
                            print(
                                f"Inconsistency found at C{j + 1}") if not complexity else None if not complexity else None

        # Calcul des potentiels pour chaque nœud
        for j in range(num_orders):
            if 'C' + str(j + 1) in potentials:
                for i in range(num_provisions):
                    if tab_matrix[i][j][0] > 0 or (f'C{j + 1}' in graph and f'P{i + 1}' in graph[f'C{j + 1}']):
                        cost = tab_matrix[i][j][1]
                        # Vérifier si le nœud Pi a déjà un potentiel, sinon le calculer
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

    # Affichage des potentiels calculés
    print("\n-------") if not complexity else None if not complexity else None
    for vertex, potential in potentials.items():
        print(f"| E({vertex}) = {potential}") if not complexity else None if not complexity else None
    print("-------") if not complexity else None if not complexity else None

    return potentials


def matrix_potential_cost(potentials, num_provisions, num_orders):
    """
    * Fonction : matrix_potential_cost
    * ---------------------------------
    * Cette fonction calcule la matrice des coûts potentiels.
    * Elle prend en paramètre les potentiels, le nombre de fournisseurs et le nombre de commandes.
    * Elle retourne la matrice des coûts potentiels.
    * :param potentials: Les potentiels
    * :param num_provisions: Le nombre de fournisseurs
    * :param num_orders: Le nombre de commandes
    * :return: La matrice des coûts potentiels
    """
    # Initialisation de la matrice des coûts potentiels à 0
    potential_cost_matrix = [[0 for _ in range(num_orders)] for _ in range(num_provisions)]

    # Calcul de la matrice des coûts potentiels
    for i in range(num_provisions):
        for j in range(num_orders):
            potential_cost_matrix[i][j] = potentials['P' + str(i + 1)] - potentials['C' + str(j + 1)]
    return potential_cost_matrix


def matrix_marginal_cost(tab_matrix, matrix_potentials, num_provisions, num_orders):
    """
    * Fonction : matrix_marginal_cost
    * --------------------------------
    * Cette fonction calcule la matrice des coûts marginaux.
    * Elle prend en paramètre la matrice des coûts de transport, la matrice des coûts potentiels, le nombre de fournisseurs
    * et le nombre de commandes.
    * Elle retourne la matrice des coûts marginaux.
    * :param tab_matrix: La matrice des coûts de transport
    * :param matrix_potentials: La matrice des coûts potentiels
    * :param num_provisions: Le nombre de fournisseurs
    * :param num_orders: Le nombre de commandes
    * :return: La matrice des coûts marginaux
    """
    # Initialisation de la matrice des coûts marginaux à 0
    marginal_cost_matrix = [[0 for _ in range(num_orders)] for _ in range(num_provisions)]

    # Calcul de la matrice des coûts marginaux
    for i in range(num_provisions):
        for j in range(num_orders):
            marginal_cost_matrix[i][j] = tab_matrix[i][j][1] - matrix_potentials[i][j]
    return marginal_cost_matrix


def separate_potentials(potentials):
    """
    * Fonction : separate_potentials
    * ------------------------------
    * Cette fonction sépare les potentiels des fournisseurs et des commandes.
    * Elle prend en paramètre les potentiels.
    * Elle retourne une liste contenant les potentiels des fournisseurs et des commandes.
    * :param potentials: Dict contenant les potentiels
    * :return: Une liste contenant les potentiels des fournisseurs et des commandes
    """
    # Initialisation des listes des potentiels des fournisseurs et des commandes
    P = []
    C = []

    # Séparation des potentiels des fournisseurs et des commandes
    for vertex, value in potentials.items():
        # Si valeur = 'P', ajouter le potentiel à la liste des fournisseurs
        if vertex.startswith('P'):
            index = int(vertex[1:]) - 1
            # Vérifier si l'index est supérieur à la taille de la liste, si oui, ajouter des valeurs None pour
            # agrandir la liste
            if len(P) <= index:
                P.extend([None] * (index + 1 - len(P)))
            P[index] = value
        # Si valeur = 'C', ajouter le potentiel à la liste des commandes
        elif vertex.startswith('C'):
            index = int(vertex[1:]) - 1
            # Vérifier si l'index est supérieur à la taille de la liste, si oui, ajouter des valeurs None pour
            # agrandir la liste
            if len(C) <= index:
                C.extend([None] * (index + 1 - len(C)))
            C[index] = value

    return [P, C]


def find_best_improving_edge(marginal_costs):
    """
    * Fonction : find_best_improving_edge
    * -----------------------------------
    * Cette fonction trouve l'arrête qui améliore le plus le coût marginal.
    * Elle prend en paramètre les coûts marginaux.
    * Elle retourne l'arrête qui améliore le plus le coût marginal.
    * :param marginal_costs: Les coûts marginaux
    * :return: L'arrête qui améliore le plus le coût marginal
    """
    # Initialisation du coût minimal et de la meilleure arrête
    min_cost = float('inf')
    best_edge = None

    # Recherche de l'arrête qui améliore le plus le coût marginal
    for i in range(len(marginal_costs)):
        for j in range(len(marginal_costs[i])):
            if marginal_costs[i][j] < min_cost:
                min_cost = marginal_costs[i][j]
                best_edge = (i, j)
    return best_edge


def extract_graph(tab_matrix, num_provisions, num_orders):
    """
    * Fonction : extract_graph
    * ------------------------
    * Cette fonction extrait un graphe à partir de la matrice des coûts de transport.
    * Elle prend en paramètre la matrice des coûts de transport, le nombre de fournisseurs et le nombre de commandes.
    * Elle retourne le graphe.
    * Il s'agit d'un graphe non orienté (les arêtes sont bidirectionnelles).
    * :param tab_matrix: La matrice des coûts de transport
    * :param num_provisions: Le nombre de fournisseurs
    * :param num_orders: Le nombre de commandes
    * :return: Le graphe
    """
    graph = {}

    # Initialisation des nœuds du graphe
    for i in range(num_provisions):
        graph[f'P{i + 1}'] = []
    for j in range(num_orders):
        graph[f'C{j + 1}'] = []

    # Ajout des arêtes au graphe, si le coût de transport est supérieur à 0
    for i in range(num_provisions):
        for j in range(num_orders):
            if tab_matrix[i][j][0] > 0:
                # Ajout des arêtes entre les fournisseurs et les commandes
                graph[f'P{i + 1}'].append(f'C{j + 1}')
                graph[f'C{j + 1}'].append(f'P{i + 1}')

    return graph


def bfs_detect_cycle(graph, start_vertex):
    """
    * Fonction : bfs_detect_cycle
    * ---------------------------
    * Cette fonction détecte un cycle dans un graphe en utilisant la méthode de parcours en largeur (BFS).
    * Elle prend en paramètre le graphe et le nœud de départ.
    * Elle retourne le cycle trouvé.
    * :param graph: Le graphe
    * :param start_vertex: Le nœud de départ
    * :return: Le cycle trouvé
    """
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
    """
    * Fonction : detect_cycle_including_edge
    * -------------------------------------
    * Cette fonction détecte un cycle dans un graphe en incluant une arête donnée.
    * Elle prend en paramètre le graphe, le nœud de départ et le nœud d'arrivée.
    * Elle retourne le cycle trouvé.
    * :param graph: Le graphe
    * :param start_vertex: Le nœud de départ
    * :param end_vertex: Le nœud d'arrivée
    * :return: Le cycle trouvé
    """
    visited = {}
    parent = {}
    queue = []

    for vertex in graph:
        visited[vertex] = False
        parent[vertex] = None

    queue.append(start_vertex)
    visited[start_vertex] = True
    parent[start_vertex] = None

    while queue:
        current = queue.pop(0)

        for neighbor in graph[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                parent[neighbor] = current
                queue.append(neighbor)
            elif neighbor != parent[current]:
                # Vérifie si le cycle inclut l'arête donnée
                if current == end_vertex or neighbor == end_vertex:
                    # Vérifie si le cycle est valide
                    cycle = []
                    # Trace depuis le nœud actuel jusqu'au début pour s'assurer qu'il forme une boucle complète
                    trace_back = current
                    while trace_back is not None:
                        cycle.append(trace_back)
                        trace_back = parent[trace_back]

                    trace_back = neighbor
                    while trace_back is not None and trace_back not in cycle:
                        cycle.append(trace_back)
                        trace_back = parent[trace_back]

                    # Ferme la boucle si le cycle est valide
                    if start_vertex in cycle and end_vertex in cycle:
                        cycle.append(current)
                        return cycle[::-1]

    # Si pas de cycle trouvé
    return None


def improve_transport_proposal(tab_matrix, graph, best_edge, source_map, destination_map, list_provisions, list_orders):
    """
    * Fonction : improve_transport_proposal
    * -------------------------------------
    * Cette fonction améliore la proposition de transport le long d'un cycle.
    * Elle prend en paramètre la matrice des coûts de transport, le graphe, la meilleure arrête, la carte source,
    * la carte de destination, la liste des fournisseurs et la liste des commandes.
    * Elle retourne True si l'amélioration est réussie, False sinon.
    * :param tab_matrix: La matrice des coûts de transport
    * :param graph: Le graphe
    * :param best_edge: La meilleure arrête
    * :param source_map: La carte source
    * :param destination_map: La carte de destination
    * :param list_provisions: La liste des fournisseurs
    * :param list_orders: La liste des commandes
    * :return: True si l'amélioration est réussie, False sinon
    """
    # Deep copy of the graph
    graph = {vertex: neighbors[:] for vertex, neighbors in graph.items()}

    # Ajoute une arête temporaire pour former un cycle
    start_vertex, end_vertex = f'C{best_edge[1] + 1}', f'P{best_edge[0] + 1}'
    graph[start_vertex].append(end_vertex)
    graph[end_vertex].append(start_vertex)

    # Trouve un cycle incluant l'arête
    cycle = detect_cycle_including_edge(graph, start_vertex, end_vertex)

    if not cycle:
        print("No cycle found including the edge") if not complexity else None
        return

    # Réordonne le cycle pour commencer par la meilleure arête
    ordered_cycle = reorder_cycle(graph, cycle, best_edge)

    # Affiche le cycle
    if not complexity and ordered_cycle:
        print(colored("* Cycle :", attrs=["bold"]), end=' ')
        print(f"{ordered_cycle[0]}", end=' ') if not complexity else None
        for i in range(1, len(ordered_cycle) - 1):
            print(f"→ {ordered_cycle[i]}", end=' ') if not complexity else None
        print(f"→ {ordered_cycle[-1]}") if not complexity else None

    # Supprime l'arête temporaire
    graph[start_vertex].remove(end_vertex)
    graph[end_vertex].remove(start_vertex)

    # Calcul du delta
    delta = calculate_delta(tab_matrix, ordered_cycle)
    print(f"* δₘₐₓ = {delta}") if not complexity else None
    if delta is None or delta <= 0:
        print(f"Pas de valeur de delta trouvée pour le transport (δ = {delta})") if not complexity else None
        return False

    # Affiche les indices pour le delta
    indices = [[get_indices(ordered_cycle[i], ordered_cycle[i + 1], source_map, destination_map) for i in
                range(len(ordered_cycle) - 1)]]
    indices.append(delta)
    display_tab_matrix([tab_matrix, list_provisions, list_orders], "δ", "delta", indices) if not complexity else None
    # Applique le delta le long du cycle
    if not apply_cycle_delta(tab_matrix, ordered_cycle, delta, source_map, destination_map, graph):
        print("Erreur lors de l'application du cycle.") if not complexity else None
        return False

    return True


def apply_cycle_delta(tab_matrix, ordered_cycle, delta, source_map, destination_map, graph):
    """
    * Fonction : apply_cycle_delta
    * ----------------------------
    * Cette fonction applique le delta le long du cycle.
    * Elle prend en paramètre la matrice des coûts de transport, le cycle ordonné, le delta, la carte source, la carte de destination
    * et le graphe.
    * Elle retourne True si l'application du delta est réussie, False sinon.
    * :param tab_matrix: La matrice des coûts de transport
    * :param ordered_cycle: Le cycle ordonné
    * :param delta: Le delta
    * :param source_map: La carte source
    * :param destination_map: La carte de destination
    * :param graph: Le graphe
    * :return: True si l'application du delta est réussie, False sinon
    """
    # Initialisation de la variable add
    add = True

    # Parcours du cycle pour appliquer le delta
    for i in range(len(ordered_cycle) - 1):
        from_node = ordered_cycle[i]
        to_node = ordered_cycle[i + 1]

        if 'P' in from_node and 'C' in to_node:
            from_index = source_map[from_node] if 'P' in from_node else destination_map[from_node]
            to_index = destination_map[to_node] if 'C' in to_node else source_map[to_node]
        else:
            from_index = source_map[to_node] if 'P' in to_node else destination_map[to_node]
            to_index = destination_map[from_node] if 'C' in from_node else source_map[from_node]

        # Vérifie si l'envoi est suffisant pour la soustraction
        if tab_matrix[from_index][to_index][0] - delta < 0 and not add:
            print(
                f"Tentative de soustraction du δ d'une arrête dont l'envoi est insuffisant : {from_node} → {to_node}") if not complexity else None
            return False

        # Applique le delta
        if add:
            tab_matrix[from_index][to_index][0] += delta
        else:
            tab_matrix[from_index][to_index][0] -= delta
            # Supprime l'arête si l'envoi est nul
            if tab_matrix[from_index][to_index][0] == 0:
                if graph[from_node].count(to_node) > 0:
                    graph[from_node].remove(to_node) if to_node in graph[from_node] else None
                    graph[to_node].remove(from_node) if from_node in graph[to_node] else None

        # Inverse la valeur de add pour la prochaine itération
        add = not add

        if tab_matrix[from_index][to_index][0] < 0:
            print(
                f"Tentative de soustraction du δ d'une arrête dont l'envoi est insuffisant : {from_node} → {to_node}") if not complexity else None
            return False

    return True


def calculate_delta(tab_matrix, ordered_cycle):
    """
    * Fonction : calculate_delta
    * --------------------------
    * Cette fonction calcule le delta pour ajuster les envois le long du cycle.
    * Elle prend en paramètre la matrice des coûts de transport et le cycle ordonné.
    * Elle retourne le delta.
    * :param tab_matrix: La matrice des coûts de transport
    * :param ordered_cycle: Le cycle ordonné
    * :return: Le delta
    """
    # Initialisation de la variable delta
    delta = float('inf')

    # Parcours du cycle pour trouver le delta
    for i in range(len(ordered_cycle) - 1):
        from_node = ordered_cycle[i]
        to_node = ordered_cycle[i + 1]

        # Converti les nœuds en indices pour tab_matrix
        if 'P' in from_node and 'C' in to_node:
            from_index = int(from_node[1:]) - 1
            to_index = int(to_node[1:]) - 1
        else:
            from_index = int(to_node[1:]) - 1
            to_index = int(from_node[1:]) - 1

        # Vérifie si la réduction est nécessaire
        if needs_reduction(i):
            shipment = tab_matrix[from_index][to_index][0]
            if shipment > 0:
                delta = min(delta, shipment)

    if delta == float('inf') or delta <= 0:
        print("No positive shipment found for reduction or incorrect cycle path.") if not complexity else None
        return None

    return delta


def needs_reduction(index):
    return index % 2 == 1


def reorder_cycle(graph, cycle, best_edge):
    """
    * Fonction : reorder_cycle
    * ------------------------
    * Cette fonction réordonne un cycle en commençant par la meilleure arrête.
    * Elle prend en paramètre le graphe, le cycle et la meilleure arrête.
    * Elle retourne le cycle réordonné.
    * :param graph: Le graphe
    * :param cycle: Le cycle
    * :param best_edge: La meilleure arrête
    * :return: Le cycle réordonné
    """
    # Trouver le nœud de départ du cycle
    cycle_count = {node: cycle.count(node) for node in cycle}
    start_node = None
    for node, count in cycle_count.items():
        if count > 1:
            start_node = node
            break

    if not start_node:
        start_node = cycle[0]

    # Initialisation des variables
    reordered_cycle = []
    visited = set()
    current_node = start_node
    best_edge_visited = False

    # Utilise un set pour éviter les boucles infinies
    while len(reordered_cycle) < len(cycle):
        reordered_cycle.append(current_node)
        visited.add(current_node)

        # Trouver le prochain nœud connecté non visité
        for next_node in graph[current_node]:
            if not best_edge_visited and current_node == f'P{best_edge[0] + 1}' and next_node == f'C{best_edge[1] + 1}':
                best_edge_visited = True
                current_node = next_node
                break
            elif next_node in cycle and next_node not in visited:
                current_node = next_node
                break
        else:
            # Si aucun nœud non visité n'est trouvé, arrêter la recherche pour éviter une boucle infinie
            break

    # Ajouter le nœud de départ à la fin pour fermer la boucle
    if reordered_cycle and reordered_cycle[0] != reordered_cycle[-1]:
        reordered_cycle.append(reordered_cycle[0])

    best_edge_tuple = (f'P{best_edge[0] + 1}', f'C{best_edge[1] + 1}')
    for i in range(len(reordered_cycle) - 1):
        if reordered_cycle[i] == best_edge_tuple[1] and reordered_cycle[i + 1] == best_edge_tuple[0]:
            reordered_cycle.reverse()
            break

    return reordered_cycle


def find_connected_components(graph):
    """
    * Fonction : find_connected_components
    * -----------------------------------
    * Cette fonction trouve les composants connexes dans un graphe.
    * Elle prend en paramètre le graphe.
    * Elle retourne les composants connexes.
    * :param graph: Le graphe
    * :return: Les composants connexes
    """
    visited = set()
    components = []

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

    for node in graph:
        if node not in visited:
            component = bfs(node)
            components.append(component)

    return components


def connect_graph_components(graph, components, tab_matrix, source_map, destination_map, fictive_edges=[]):
    """
    * Fonction : connect_graph_components
    * -----------------------------------
    * Cette fonction connecte les composants du graphe pour former un arbre.
    * Elle prend en paramètre le graphe, les composants, la matrice des coûts de transport, la carte source, la carte de destination
    * et les arêtes fictives.
    * Elle retourne le graphe connecté et les arêtes fictives ajoutées.
    * :param graph: Le graphe
    * :param components: Les composants
    * :param tab_matrix: La matrice des coûts de transport
    * :param source_map: La carte source
    * :param destination_map: La carte de destination
    * :param fictive_edges: Les arêtes fictives
    * :return: Le graphe connecté et les arêtes fictives ajoutées
    """
    # Vérifie si le graphe est déjà connecté de manière optimale
    if len(components[0]) - 1 == len(graph) - len(components):
        print("Le graphe est déjà connecté de manière optimale comme un arbre.") if not complexity else None
        return graph, fictive_edges

    for edge in fictive_edges:
        graph.setdefault(edge[0], []).append(edge[1]) if edge[1] not in graph[edge[0]] else None
        graph.setdefault(edge[1], []).append(edge[0]) if edge[0] not in graph[edge[1]] else None

    # Vérifie si le graphe est déjà connecté de manière optimale
    components = find_connected_components(graph)
    if len(components[0]) - 1 == len(graph) - len(components):
        print("Le graphe est déjà connecté de manière optimale comme un arbre.") if not complexity else None
        return graph, fictive_edges

    base_component = components[0]

    # Connecter les composants restants au premier composant
    for other_component in components[1:]:
        min_cost = float('inf')
        best_connection = None

        # Trouver la meilleure connexion entre les composants
        for base_node in base_component:
            for other_node in other_component:
                # Détermine si la connexion est entre un fournisseur et un client ou vice versa
                if base_node.startswith('P') and other_node.startswith('C'):
                    p_index = source_map[base_node]
                    c_index = destination_map[other_node]
                elif base_node.startswith('C') and other_node.startswith('P'):
                    p_index = source_map[other_node]
                    c_index = destination_map[base_node]
                else:
                    continue

                edge_cost = tab_matrix[p_index][c_index][1]

                # Vérifie si le coût de l'arête est inférieur au minimum actuel
                if edge_cost < min_cost:
                    min_cost = edge_cost
                    best_connection = (base_node, other_node)

        # Ajouter la meilleure connexion trouvée
        if best_connection:
            p, c = best_connection
            graph.setdefault(p, []).append(c)
            graph.setdefault(c, []).append(p)
            print(f"Connexion de {p} → {c} avec coût {min_cost}") if not complexity else None
            fictive_edges.append([p, c])

    return graph, fictive_edges


def maximize_transportation(tab_matrix, graph, cycle, source_map, destination_map):
    if not cycle:
        print("No cycle found. No maximization possible.") if not complexity else None
        return

    print("Cycle detected for maximization: ", cycle) if not complexity else None

    delta = calculate_delta(tab_matrix, cycle)
    print(f"Delta for adjustment: {delta}") if not complexity else None

    if delta <= 0:
        print("No adjustment possible, all shipments are at minimum in the cycle.") if not complexity else None
        return

    adjust_shipments(tab_matrix, cycle, delta, source_map, destination_map)

    print("Updated transportation matrix after maximization:") if not complexity else None
    deleted_edges = []
    for i in range(len(cycle) - 1):
        from_node = cycle[i]
        to_node = cycle[i + 1]
        from_index, to_index = get_indices(from_node, to_node, source_map, destination_map)
        shipment = tab_matrix[from_index][to_index][0]
        print(f"{from_node} → {to_node}: {shipment}") if not complexity else None
        if shipment == 0:
            deleted_edges.append((from_node, to_node))

    if deleted_edges:
        print("Deleted edges after maximization:") if not complexity else None
        for edge in deleted_edges:
            print(f"{edge[0]} → {edge[1]}") if not complexity else None
    else:
        print("No edges deleted.") if not complexity else None


def get_indices(from_node, to_node, source_map, destination_map):
    """
    * Fonction : get_indices
    * -----------------------
    * Cette fonction retourne les indices des nœuds source et destination.
    * Elle prend en paramètre les nœuds source et destination, la carte source et la carte de destination.
    * Elle retourne les indices des nœuds source et destination.
    * :param from_node: Le nœud source
    """
    from_index = source_map.get(from_node, destination_map.get(from_node))
    to_index = destination_map.get(to_node, source_map.get(to_node))
    return from_index, to_index


def adjust_shipments(tab_matrix, cycle, delta, source_map, destination_map):
    """
    * Fonction : adjust_shipments
    * ---------------------------
    * Cette fonction ajuste les envois le long du cycle détecté.
    * Elle prend en paramètre la matrice des coûts de transport, le cycle, le delta, la carte source et la carte de destination.
    * :param tab_matrix: La matrice des coûts de transport
    * :param cycle: Le cycle
    * :param delta: Le delta
    * :param source_map: La carte source
    * :param destination_map: La carte de destination
    """
    add = True
    for i in range(len(cycle) - 1):
        from_node = cycle[i]
        to_node = cycle[i + 1]
        from_index, to_index = get_indices(from_node, to_node, source_map, destination_map)

        if add:
            tab_matrix[from_index][to_index][0] += delta
        else:
            tab_matrix[from_index][to_index][0] -= delta

        add = not add
