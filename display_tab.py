"""
Projet : PRJ-SM602 - Recherche Opérationnelle - 2023/2024 - Thème sur le problème de transport
Auteurs: KOCOGLU Lucas, BAUDET Antoine, HOUEE Adrien
Description: Fichier contenant les fonctions d'affichage du graphe.
Version de Python : 3.12
"""

from termcolor import colored
from tabulate import tabulate


def display_tab_matrix(tab_matrix, tab_num, option="", optionvalue=[]):
    """
    * Fonction: display_tab_matrix
    * --------------------
    * Fonction permettant d'afficher le tableau de contraintes.
    * :param tab_matrix: Tableau de contraintes à afficher
    * :param option: Option pour l'affichage
    """
    if tab_matrix is not None:
        if option == "potential":
            P = len(tab_matrix)
            C = len(tab_matrix[0])
            print(P, C, tab_matrix)
            header = [str(tab_num)] + [colored("C" + str(i + 1), "cyan", attrs=["bold"]) for i in range(C)]
            body = []

            for i in range(P):
                body.append([colored("P" + str(i + 1), "cyan", attrs=["bold"])])
                for j in range(C):
                    body[i].append(tab_matrix[i][j])

            print(tabulate(body, headers=header, tablefmt="mixed_grid", numalign="center", stralign="center"))
        elif option == "marginal":
            P = len(tab_matrix)
            C = len(tab_matrix[0])
            header = [str(tab_num)] + [colored("C" + str(i + 1), "cyan", attrs=["bold"]) for i in range(C)]
            body = []

            for i in range(P):
                body.append([colored("P" + str(i + 1), "cyan", attrs=["bold"])])
                for j in range(C):
                    body[i].append(tab_matrix[i][j])

            print(tabulate(body, headers=header, tablefmt="mixed_grid", numalign="center", stralign="center"))
        elif option == "balas_hammer":
            SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
            header = [str(tab_num)] + [colored("C" + str(i + 1).translate(SUB), "cyan", attrs=["bold"]) for i in range(len(tab_matrix[0][0]))] + [colored("Provisions Pᵢ", "green", attrs=["bold"])] + [colored("Pénalités", "red", attrs=["bold"])]

            body = []
            for i in range(len(tab_matrix[0])):
                body.append([colored("P" + str(i + 1).translate(SUB), "cyan", attrs=["bold"])])
                for j in range(len(tab_matrix[0][i])):
                    if len(optionvalue) > 2:
                        if optionvalue[2]:
                            if (optionvalue[2][0] == j and optionvalue[2][1] == i and optionvalue[2][2] == "row") or (optionvalue[2][0] == i and optionvalue[2][1] == j and optionvalue[2][2] == "column"):
                                body[i].append(colored(str(tab_matrix[0][i][j][0]), "white", "on_yellow", attrs=["bold"]) + " " + colored(str(tab_matrix[0][i][j][1]).translate(SUB), "green", attrs=["bold"]))
                            else:
                                body[i].append(str(tab_matrix[0][i][j][0]) + " " + colored(str(tab_matrix[0][i][j][1]).translate(SUB), "green"))
                        else:
                            body[i].append(str(tab_matrix[0][i][j][0]) + " " + colored(str(tab_matrix[0][i][j][1]).translate(SUB), "green"))
                    else:
                        body[i].append(str(tab_matrix[0][i][j][0]) + " " + colored(str(tab_matrix[0][i][j][1]).translate(SUB), "green"))
                body[i].append(tab_matrix[1][i])
                if optionvalue[0]:
                    if optionvalue[0][i] == '-':
                        body[i].append(colored(optionvalue[0][i], "dark_grey"))
                    else:
                        if optionvalue[3]:
                            if optionvalue[3][1] == i and optionvalue[3][2] == "row":
                                body[i].append(colored(optionvalue[0][i], "white", "on_red", attrs=["bold"]))
                            else:
                                body[i].append(colored(optionvalue[0][i], "red"))
                        else:
                            body[i].append(colored(optionvalue[0][i], "red"))

            body.append([colored("Commandes Cᵢ", "green", attrs=["bold"])] + [str(tab_matrix[2][i]) for i in range(len(tab_matrix[2]))] + [""])

            if optionvalue[1]:
                body.append([colored("Pénalités", "red", attrs=["bold"])])
                for i in range(len(optionvalue[1])):
                    if optionvalue[1][i] == '-':
                        body[-1].append(colored(optionvalue[1][i], "dark_grey"))
                    else:
                        if optionvalue[3]:
                            if optionvalue[3][1] == i and optionvalue[3][2] == "column":
                                body[-1].append(colored(optionvalue[1][i], "white", "on_red", attrs=["bold"]))
                            else:
                                body[-1].append(colored(optionvalue[1][i], "red"))
                        else:
                            body[-1].append(colored(optionvalue[1][i], "red"))
                body[-1].append("")

            print(tabulate(body, headers=header, tablefmt="mixed_grid", numalign="center", stralign="center"))
        else:
            SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
            header = [str(tab_num)] + [colored("C" + str(i + 1).translate(SUB), "cyan", attrs=["bold"]) for i in range(len(tab_matrix[0][0]))] + [colored("Provisions Pᵢ", "green", attrs=["bold"])]

            body = []
            for i in range(len(tab_matrix[0])):
                body.append([colored("P" + str(i + 1).translate(SUB), "cyan", attrs=["bold"])])
                for j in range(len(tab_matrix[0][i])):
                    body[i].append(str(tab_matrix[0][i][j][0]) + " " + colored(str(tab_matrix[0][i][j][1]).translate(SUB), "green"))
                body[i].append(tab_matrix[1][i])

            body.append([colored("Commandes Cᵢ", "green", attrs=["bold"])] + [str(tab_matrix[2][i]) for i in range(len(tab_matrix[2]))] + [""])

            print(tabulate(body, headers=header, tablefmt="mixed_grid", numalign="center", stralign="center"))
