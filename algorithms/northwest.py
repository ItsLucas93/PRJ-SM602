"""
Projet : PRJ-SM602 - Recherche Opérationnelle - 2023/2024 - Thème sur le problème de transport
Auteurs: KOCOGLU Lucas, BAUDET Antoine, HOUEE Adrien
Description: Ce fichier contient l'algorithme de Nord-Ouest
Version de Python: 3.12
"""


def northwest(tab_matrix):
    """
    * Fonction : northwest
    * -------------------
    * Cette fonction implémente l'algorithme de Nord-Ouest pour résoudre le problème de transport
    * :param tab_matrix: La matrice du problème de transport
    * :return: La matrice du problème de transport résolu
    """
    # Initialisation des variables
    num_provisions = len(tab_matrix[1])
    num_orders = len(tab_matrix[2])

    # Deep copy of the tab_matrix
    northwest_matrix = [[[0, tab_matrix[0][i][j][1]] for j in range(0, num_orders)] for i in range(0, num_provisions)]
    list_provisions = [tab_matrix[1][i] for i in range(0, num_provisions)]
    list_orders = [tab_matrix[2][j] for j in range(0, num_orders)]

    # Algorithme de Nord-Ouest
    i, j = 0, 0
    while i < num_provisions and j < num_orders:
        # Si une des deux listes est vide, on passe à la suivante
        if list_provisions[i] == 0:
            i += 1
            continue
        if list_orders[j] == 0:
            j += 1
            continue

        # Calcul de la quantité à transporter
        quantity = min(list_provisions[i], list_orders[j])
        northwest_matrix[i][j][0] = quantity
        list_provisions[i] -= quantity
        list_orders[j] -= quantity

        # Passage à la case suivante
        if list_provisions[i] == 0 and list_orders[j] == 0:
            i += 1
            j += 1
        elif list_provisions[i] == 0:
            i += 1
        elif list_orders[j] == 0:
            j += 1

    return [northwest_matrix, tab_matrix[1], tab_matrix[2]]
