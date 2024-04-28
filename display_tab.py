"""
Projet : PRJ-SM602 - Recherche Opérationnelle - 2023/2024 - Thème sur le problème de transport
Auteurs: KOCOGLU Lucas, BAUDET Antoine, HOUEE Adrien
Description: Fichier contenant les fonctions d'affichage du graphe.
Version de Python : 3.12
"""

from termcolor import colored
from tabulate import tabulate

def display_tab_matrix(tab_matrix, tab_num, option =""):
    """
    * Fonction: display_tab_matrix
    * --------------------
    * Fonction permettant d'afficher le tableau de contraintes.
    * :param tab_matrix: Tableau de contraintes à afficher
    * :param option: Option pour l'affichage
    """
    if tab_matrix is not None:
        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        header = [str(tab_num)] + [colored("C" + str(i + 1).translate(SUB), "cyan", attrs=["bold"]) for i in range(len(tab_matrix[0][0]))] + [colored("Provisions Pᵢ", "green", attrs=["bold"])]

        body = []
        for i in range(len(tab_matrix[0])):
            body.append([colored("P" + str(i + 1).translate(SUB), "cyan", attrs=["bold"])])
            for j in range(len(tab_matrix[0][i])):
                body[i].append(str(tab_matrix[0][i][j][0]) + " " + colored(str(tab_matrix[0][i][j][1]).translate(SUB), "green" ))
            body[i].append(tab_matrix[1][i])

        body.append([colored("Commandes Cᵢ", "green", attrs=["bold"])] + [str(tab_matrix[2][i]) for i in range(len(tab_matrix[2]))] + [""])

        print(tabulate(body, headers=header, tablefmt="mixed_grid", numalign="center", stralign="center"))
