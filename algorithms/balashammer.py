"""
Projet : PRJ-SM602 - Recherche Opérationnelle - 2023/2024 - Thème sur le problème de transport
Auteurs: KOCOGLU Lucas, BAUDET Antoine, HOUEE Adrien
Description: Ce fichier contient l'algorithme de Balas-Hammer
Version de Python: 3.12
"""

from tabulate import tabulate
from termcolor import colored
from display_tab import display_tab_matrix


def balashammer(tab_matrix):
    # Initialisation des variables
    num_provisions = len(tab_matrix[1])
    num_orders = len(tab_matrix[2])

    # Deep copy of the tab_matrix
    balas_hammer_matrix = [[[0, tab_matrix[0][i][j][1]] for j in range(0, num_orders)] for i in range(0, num_provisions)]
    list_provisions = [tab_matrix[1][i] for i in range(0, num_provisions)]
    list_orders = [tab_matrix[2][j] for j in range(0, num_orders)]

    k = 1
    while sum(list_provisions) != 0 and sum(list_orders) != 0:
        print(colored("\n* Itération n°" + str(k), attrs=["bold", "underline"]))
        k += 1

        penalties = []

        for i in range(num_provisions):
            row = [tab_matrix[0][i][j][1] for j in range(num_orders) if list_provisions[i] > 0 if balas_hammer_matrix[i][j][1] > -1]
            if len(row) > 1:
                row = sorted(row)
                penalties.append((row[1] - row[0], i, "row"))
            else:
                penalties.append((float('-inf'), i, None))

        for j in range(num_orders):
            column = [tab_matrix[0][i][j][1] for i in range(num_provisions) if list_orders[j] > 0 if balas_hammer_matrix[i][j][1] > -1]
            if len(column) > 1:
                column = sorted(column)
                penalties.append((column[1] - column[0], j, "column"))
            else:
                penalties.append((float('-inf'), j, None))

        # Max Penalty
        max_penalty, max_index, mode = max_penalties(penalties)
        min_quantity, min_index = float('inf'), -1

        # Affichage à chaque étape
        print_penalty = [[], []]
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
                if list_provisions[max_index] == 0:
                    for j in range(num_orders):
                        balas_hammer_matrix[max_index][j][1] = -1
            case "column":
                for i in range(num_provisions):
                    if list_provisions[i] > 0 and tab_matrix[0][i][max_index][1] < min_quantity:
                        min_quantity = tab_matrix[0][i][max_index][1]
                        min_index = i
                quantity = min(list_provisions[min_index], list_orders[max_index])
                balas_hammer_matrix[min_index][max_index][0] += quantity
                list_provisions[min_index] -= quantity
                list_orders[max_index] -= quantity
                if list_orders[max_index] == 0:
                    for i in range(num_provisions):
                        balas_hammer_matrix[i][max_index][1] = -1
            case _:
                pass

        # Affichage à chaque étape
        print_penalty = [[], []]
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
        display_tab_matrix([balas_hammer_matrix, tab_matrix[1], tab_matrix[2]], "Balas-Hammer", option="balas_hammer", optionvalue=print_penalty)

    # Réinitialisation des coûts à l'original
    for i in range(num_provisions):
        for j in range(num_orders):
            if balas_hammer_matrix[i][j][1] == -1:
                balas_hammer_matrix[i][j][1] = tab_matrix[0][i][j][1]

    print(colored("\n* Fin en n°" + str(k) + " itérations.", attrs=["bold", "underline"]))
    return [balas_hammer_matrix, tab_matrix[1], tab_matrix[2]]


def max_penalties(penalties):
    max_penalty = float('-inf')
    max_index = -1
    mode = None
    for i in range(len(penalties)):
        if penalties[i][0] > max_penalty:
            max_penalty = penalties[i][0]
            max_index = penalties[i][1]
            mode = penalties[i][2]
    return max_penalty, max_index, mode
