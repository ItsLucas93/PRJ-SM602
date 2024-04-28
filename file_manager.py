"""
Projet : PRJ-SM602 - Recherche Opérationnelle - 2023/2024 - Thème sur le problème de transport
Auteurs: KOCOGLU Lucas, BAUDET Antoine, HOUEE Adrien
Description: Ce fichier est le fichier qui lit les tableaux de contraintes, il permet de lister les fichiers .txt disponibles dans le dossier "tables" ainsi que de le convertir en tableau de contraintes.
Version de Python: 3.12
"""

import os
from termcolor import colored

folder_path = "tables/"

def files_list(path=folder_path):
    """
    * Fonction: files_list
    * --------------------
    * Lit et renvoie la liste des fichiers de test disponibles dans le dossier enregistré dans la variable path.
    * Renvoie un message d'erreur si le dossier/fichiers n'est pas trouvé.
    * :param path: Chemin du dossier contenant les fichiers de test.
    * :return: Liste des fichiers de test disponibles, Dictionnaire des fichiers de test | En cas d'échec : Message d'erreur, None
    """
    # Dictionnaire des fichiers de test
    index_test_files = {}

    # Récupération de la liste de fichier
    try:
        files = os.listdir(path)
        if len(files) == 0:
            return colored(
                "Aucun fichier n'a été trouvé dans le dossier de " + colored(str(path), attrs=["bold", "underline"]),
                "red"), None
        # Construction d'une variable string pour l'affichage
        string = "\nFichiers disponibles dans le dossier : " + colored(str(path), attrs=["underline"]) + "\n"

        # Ajout de l'option de retour au menu principal
        index_test_files[0] = "Retour au menu principal"
        string += str(0) + ".\t" + index_test_files[0] + "\n"

        # Filtrage des fichiers .txt
        for i in files:
            if i.split('.')[-1] != 'txt':
                files.remove(i)

        # Tri des fichiers par ordre croissant
        files.sort(key=lambda str: int(str.split()[1].split('.')[0]))  # ['table', 'x', '.txt']

        # Ajout des fichiers à la liste des fichiers de test & à la variable string
        for i, file in enumerate(files):
            index_test_files[i + 1] = file
            string += str(i + 1) + ".\t" + file + "\n"
        return string, index_test_files
    except FileNotFoundError:
        return colored("Le dossier de ", "red") + colored(str(path), "red", attrs=["bold", "underline"]) + colored(
            " n'a pas été trouvé.", "red"), None
    except Exception as e:
        return colored("Une erreur est survenue : " + str(e), "red"), None


def read_file(file, path=folder_path):
    tab_matrix = tab_to_matrix(file, path)
    return tab_matrix


def tab_to_matrix(file, path=folder_path):
    matrix_cost = []
    list_provisions = []
    list_orders = []

    try:
        with open(path + file, 'r') as file:
            n, m = map(int, file.readline().strip().split())

            # Ajout de la matrice des coûts, avec en dernière position les provisions
            for i in range(n):
                line = file.readline().strip()
                line = list(map(int, line.split()))
                temp = []
                for j in range(len(line) - 1):
                    temp.append([0, line[j]])
                matrix_cost.append(temp)
                list_provisions.append(line[-1])

            # Dernière ligne : Ajout des commandes
            list_orders = list(map(int, file.readline().strip().split()))

        return [matrix_cost, list_provisions, list_orders]
    except FileNotFoundError:
        print(colored("Le fichier " + file + " n'a pas été trouvé.", "red"))
        return None
    except Exception as e:
        print(colored("Une erreur est survenue : " + str(e), "red"))
        return None
