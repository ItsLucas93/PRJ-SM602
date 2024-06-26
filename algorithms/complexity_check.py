"""
Projet : PRJ-SM602 - Recherche Opérationnelle - 2023/2024 - Thème sur le problème de transport
Auteurs: KOCOGLU Lucas, BAUDET Antoine, HOUEE Adrien
Description: Ce fichier contient les calculs de complexité des algorithmes.
Version de Python: 3.12
"""

from algorithms.northwest import northwest
from algorithms.balashammer import balashammer
from algorithms.steppingstone import steppingstone
from termcolor import colored
from random import randint
from time import time
from tqdm import tqdm

folder_path = "./complexity"

def complexity_menu(choice=-1):
    """
    * Fonction : complexity_menu
    * ----------------------
    * Menu de complexité pour les algorithmes de résolution du problème de transport.
    * :param choice:
    """
    while True:
        choice_dict = {
            1: "North west",
            2: "Balas-Hammer",
            3: "Stepping Stone - North West",
            4: "Stepping Stone - Balas-Hammer",
            5: "Stepping Stone - North West (sans calcul de North West dans la complexité)",
            6: "Stepping Stone - Balas-Hammer (avec calcul de Ballas-Hammer dans la complexité)",
            7: "Retour au menu principal"
        }
        n_dict = {
            1: 10,
            2: 40,
            3: 100,
            4: 400,
            5: 1000,
            6: 4000,
            7: 10000
        }
        print("---------------------- Menu de Complexité ----------------------"
              "\n1.\tNorth west"
              "\n2.\tBalas-Hammer"
              "\n3.\tStepping Stone - North West"
              "\n4.\tStepping Stone - Balas-Hammer"
              "\n5.\tStepping Stone - North West (sans calcul de North West dans la complexité)"
              "\n6.\tStepping Stone - Balas-Hammer (avec calcul de Ballas-Hammer dans la complexité)"
              "\n7.\tRetour au menu principal"
              "\n---------------------------------------------------------------")
        choice = int(input(colored("Entrez votre choix : ", "magenta")))
        if choice in choice_dict.keys():
            if choice == 7:
                print(colored("Retour au menu principal...", "yellow"))
                return
            else:
                while True:
                    # Valeurs de n à tester 10 ; 40 ; 100 ; 400 ; 10 000 ; 40 000 ; 100 000
                    print("---------------------- Valeurs de n à tester ----------------------"
                            "\n1.\t10"
                            "\n2.\t40"
                            "\n3.\t100"
                            "\n4.\t400"
                            "\n5.\t1 000"
                            "\n6.\t4 000"
                            "\n7.\t10 000"
                            "\n---------------------------------------------------------------")
                    n = int(input(colored("Choisissez la valeur de n à tester : ", "magenta")))

                    # Exécution de l'algorithme choisi x100
                    if n in n_dict.keys():
                        for i in tqdm(range(100)):
                            start_time = time()
                            tab_matrix = generate_tab(n_dict[n])
                            match choice:
                                case 1:
                                    northwest(tab_matrix)
                                case 2:
                                    balashammer(tab_matrix, True)
                                case 3:
                                    steppingstone(northwest(tab_matrix), True)
                                case 4:
                                    steppingstone(balashammer(tab_matrix, True), True)
                                case 5:
                                    tab_matrix = northwest(tab_matrix)
                                    start_time = time()
                                    steppingstone(tab_matrix, True)
                                case 6:
                                    tab_matrix = balashammer(tab_matrix, True)
                                    start_time = time()
                                    steppingstone(tab_matrix, True)
                            end_time = time()
                            # print(colored("Temps d'exécution : " + str(end_time - start_time) + "s", "green"))

                            # Enregistrement (ajout) du temps d'exécution dans un fichier
                            with open(folder_path + "/" + choice_dict[choice] + "_" + str(n_dict[n]) + ".txt", 'a') as file:
                                file.write(str(end_time - start_time) + "s\n")

                    else:
                        print(colored("Veuillez entrer un choix valide.", "red"))
        else:
            print(colored("Veuillez entrer un choix valide.", "red"))


def generate_tab(n):
    """
    * Fonction : generate_tab
    * ----------------------
    * Génère une matrice de transport, une liste de provisions et une liste de commandes.
    * :param n: Taille de la matrice de transport
    * :return: [tab_matrix, list_provision, list_order] : Matrice de transport, liste de provisions et liste de commandes
    """
    tab_matrix = [[[0, randint(1, 100)] for _ in range(n)] for _ in range(n)]
    list_provision = [randint(1, 100) for _ in range(n)]
    list_order = [randint(1, 100) for _ in range(n)]
    return [tab_matrix, list_provision, list_order]