"""
Projet : PRJ-SM602 - Recherche Opérationnelle - 2023/2024 - Thème sur le problème de transport
Auteurs: KOCOGLU Lucas, BAUDET Antoine, HOUEE Adrien
Description: Ce fichier contient l'algorithme de Balas-Hammer
Version de Python: 3.12
"""

from termcolor import colored

from display_tab import display_tab_matrix


def balashammer(tab_matrix, complexity_calculation=False):
    # Initialisation des variables
    num_provisions = len(tab_matrix[1])
    num_orders = len(tab_matrix[2])

    # Deep copy of the tab_matrix
    balas_hammer_matrix = [[[0, tab_matrix[0][i][j][1]] for j in range(0, num_orders)] for i in range(0, num_provisions)]
    list_provisions = [tab_matrix[1][i] for i in range(0, num_provisions)]
    list_orders = [tab_matrix[2][j] for j in range(0, num_orders)]

    confirm = None
    k = 1
    while sum(list_provisions) != 0 and sum(list_orders) != 0:
        if not complexity_calculation:
            while confirm not in ['y', 'n']:
                confirm = input(colored("Souhaitez-vous afficher les itérations ? (y/n)... ", "magenta"))
                if confirm not in ['y', 'n']:
                    print(colored("Le choix n'a pas été reconnue.", "red"))
        else:
            confirm = 'n'

        if confirm == 'y' and not complexity_calculation:
            print(colored("\n* Itération n°" + str(k), attrs=["bold", "underline"]))
        k += 1

        penalties = []

        for i in range(num_provisions):
            row = [tab_matrix[0][i][j][1] for j in range(num_orders) if list_provisions[i] > 0 if list_orders[j] > 0]
            if len(row) > 1:
                row = sorted(row)
                penalties.append((row[1] - row[0], i, "row"))
            else:
                penalties.append((float('-inf'), i, None))

        for j in range(num_orders):
            column = [tab_matrix[0][i][j][1] for i in range(num_provisions) if list_orders[j] > 0 if list_provisions[i] > 0]
            if len(column) > 1:
                column = sorted(column)
                penalties.append((column[1] - column[0], j, "column"))
            else:
                penalties.append((float('-inf'), j, None))

        # Max Penalty
        candidates = max_penalties(penalties)

        if len(candidates) == 1:
            if candidates[0][0] == float('-inf'):
                for i in range(num_provisions):
                    if list_provisions[i] > 0:
                        max_penalty, max_index, mode = 0, i, "row"
                for j in range(num_orders):
                    if list_orders[j] > 0:
                        max_penalty, max_index, mode = 0, j, "column"
            else:
                max_penalty, max_index, mode = candidates[0][0], candidates[0][1], candidates[0][2]
        else:
            final_candidates = []
            min_cost_index = 0
            min_cost = -1
            for penalty, index, mode in candidates:
                if mode == "row":
                    for i in range(num_orders):
                        if list_provisions[index] > 0 and list_orders[i] > 0:
                            if tab_matrix[0][index][i][1] < min_cost or min_cost == -1:
                                min_cost_index = i
                                min_cost = tab_matrix[0][index][i][1]
                    final_candidates.append(min(list_orders[min_cost_index], list_provisions[index]))
                elif mode == "column":
                    for j in range(num_provisions):
                        if list_orders[index] > 0 and list_provisions[j] > 0:
                            if tab_matrix[0][j][index][1] < min_cost or min_cost == -1:
                                min_cost_index = j
                                min_cost = tab_matrix[0][j][index][1]
                    final_candidates.append([min(list_provisions[min_cost_index], list_orders[index]), min_cost])

            # Choix du maximum, si plusieurs candidats à égalité, on prend le coût minimum
            if len(candidates) > 1:
                max_penalty, max_index, mode = resolve_ties(candidates, tab_matrix, list_provisions, list_orders)
            else:
                max_penalty, max_index, mode = candidates[0][0], candidates[0][1], candidates[0][2]

        min_quantity, min_index = float('inf'), -1
        # input(colored("Appuyez sur une touche pour continuer...", "magenta"))
        # Affichage à chaque étape
        if confirm == 'y':
            print_penalty = [[], [], [], []]
            for penalty in range(len(penalties)):
                match penalties[penalty][2]:
                    case "row":
                        print_penalty[0].append(penalties[penalty][0])
                    case "column":
                        print_penalty[1].append(penalties[penalty][0])
                    case None:
                        if penalty < num_provisions:
                            print_penalty[0].append("-")
                        else:
                            print_penalty[1].append("-")
                print_penalty[3] = [max_penalty, max_index, mode]
            if not complexity_calculation:
                display_tab_matrix([balas_hammer_matrix, tab_matrix[1], tab_matrix[2]], "Balas-Hammer", option="balas_hammer", optionvalue=print_penalty)

        match mode:
            case "row":
                for j in range(num_orders):
                    if list_orders[j] > 0 and tab_matrix[0][max_index][j][1] < min_quantity:
                        min_quantity = tab_matrix[0][max_index][j][1]
                        min_index = j
                quantity = min(list_provisions[max_index], list_orders[min_index])
                balas_hammer_matrix[max_index][min_index][0] += quantity
                list_provisions[max_index] -= quantity
                list_orders[min_index] -= quantity
            case "column":
                for i in range(num_provisions):
                    if list_provisions[i] > 0 and tab_matrix[0][i][max_index][1] < min_quantity:
                        min_quantity = tab_matrix[0][i][max_index][1]
                        min_index = i
                quantity = min(list_provisions[min_index], list_orders[max_index])
                balas_hammer_matrix[min_index][max_index][0] += quantity
                list_provisions[min_index] -= quantity
                list_orders[max_index] -= quantity
            case _:
                pass

        # Affichage à chaque étape
        if confirm == 'y':
            print_penalty = [[], [], [], []]
            for penalty in range(len(penalties)):
                match penalties[penalty][2]:
                    case "row":
                        print_penalty[0].append(penalties[penalty][0])
                    case "column":
                        print_penalty[1].append(penalties[penalty][0])
                    case None:
                        if penalty < num_provisions:
                            print_penalty[0].append("-")
                        else:
                            print_penalty[1].append("-")
            print_penalty[2] = [min_index, max_index, mode]
            if not complexity_calculation:
                display_tab_matrix([balas_hammer_matrix, tab_matrix[1], tab_matrix[2]], "Balas-Hammer", option="balas_hammer", optionvalue=print_penalty)

    if not complexity_calculation:
        print(colored("\n* Fin en " + str(k) + " itérations.", attrs=["bold", "underline"]))
    return [balas_hammer_matrix, tab_matrix[1], tab_matrix[2]]


def max_penalties(penalties):
    candidates = []
    max_penalty = float('-inf')
    max_index = -1
    mode = None
    for i in range(len(penalties)):
        if penalties[i][0] >= max_penalty and penalties[i][0] > 0:
            if penalties[i][0] > max_penalty:
                candidates = []
            max_penalty = penalties[i][0]
            max_index = penalties[i][1]
            mode = penalties[i][2]
            candidates.append([max_penalty, max_index, mode])

    if not candidates:
        candidates.append([max_penalty, max_index, mode])
    return candidates


def resolve_ties(candidates, tab_matrix, list_provisions, list_orders):
    min_cost = float('inf')
    selected_candidate = None
    for penalty, index, mode in candidates:
        if mode == "row":
            costs = [tab_matrix[0][index][j][1] for j in range(len(list_orders)) if list_orders[j] > 0]
        elif mode == "column":
            costs = [tab_matrix[0][i][index][1] for i in range(len(list_provisions)) if list_provisions[i] > 0]
        else:
            continue

        local_min = min(costs) if costs else float('inf')

        if local_min < min_cost:
            min_cost = local_min
            selected_candidate = (penalty, index, mode)

    return selected_candidate
