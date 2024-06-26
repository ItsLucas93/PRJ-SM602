"""
Projet : PRJ-SM602 - Recherche Opérationnelle - 2023/2024 - Thème sur le problème de transport
Auteurs: KOCOGLU Lucas, BAUDET Antoine, HOUEE Adrien
Description: Ce fichier contient l'affichage du coût total de la proposition de transport
Version de Python: 3.12
"""


def totalcost(tab_matrix):
    """
    * Fonction : totalcost
    * --------------------
    * Cette fonction permet de calculer le coût total de la proposition de transport
    * :param tab_matrix: Tableau contenant les coûts unitaires et les quantités à transporter
    * :return: Le coût total de la proposition de transport
    """
    matrixtotalcost = 0
    for i in range(len(tab_matrix[1])):
        for j in range(len(tab_matrix[2])):
            matrixtotalcost += tab_matrix[0][i][j][0] * tab_matrix[0][i][j][1]
    return matrixtotalcost
