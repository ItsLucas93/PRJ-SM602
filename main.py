"""
Projet : PRJ-SM602 - Recherche Opérationnelle - 2023/2024 - Thème sur le problème de transport
Auteurs: KOCOGLU Lucas, BAUDET Antoine, HOUEE Adrien
Description: Ce fichier est le fichier qui lit les tableaux de contraintes, il permet de lister les fichiers .txt disponibles dans le dossier "tables" ainsi que de le convertir en tableau de contraintes.
Version de Python: 3.12
"""

from termcolor import colored

from algorithms.northwest import northwest
from algorithms.balashammer import balashammer
from algorithms.steppingstone import *
from algorithms.totalcost import totalcost
from display_tab import display_tab_matrix
from file_manager import files_list, read_file


def welcome():
    """
     * Fonction: welcome
     * -----------------
     * Fonction permettant d'afficher un message de bienvenue coloré.
    """
    print(colored("\n\\\\\\ Bienvenue dans le Projet"
                  "\n\t\t██████╗░███████╗░█████╗░██╗░░██╗███████╗██████╗░░█████╗░██╗░░██╗███████╗"
                  "\n\t\t██╔══██╗██╔════╝██╔══██╗██║░░██║██╔════╝██╔══██╗██╔══██╗██║░░██║██╔════╝"
                  "\n\t\t██████╔╝█████╗░░██║░░╚═╝███████║█████╗░░██████╔╝██║░░╚═╝███████║█████╗░░"
                  "\n\t\t██╔══██╗██╔══╝░░██║░░██╗██╔══██║██╔══╝░░██╔══██╗██║░░██╗██╔══██║██╔══╝░░"
                  "\n\t\t██║░░██║███████╗╚█████╔╝██║░░██║███████╗██║░░██║╚█████╔╝██║░░██║███████╗"
                  "\n\t\t╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝"
                  "\n"
                  "\n\t\t░█████╗░██████╗░███████╗██████╗░░█████╗░████████╗██╗░█████╗░███╗░░██╗███╗░░██╗███████╗██╗░░░░░██╗░░░░░███████╗"
                  "\n\t\t██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║████╗░██║██╔════╝██║░░░░░██║░░░░░██╔════╝"
                  "\n\t\t██║░░██║██████╔╝█████╗░░██████╔╝███████║░░░██║░░░██║██║░░██║██╔██╗██║██╔██╗██║█████╗░░██║░░░░░██║░░░░░█████╗░░"
                  "\n\t\t██║░░██║██╔═══╝░██╔══╝░░██╔══██╗██╔══██║░░░██║░░░██║██║░░██║██║╚████║██║╚████║██╔══╝░░██║░░░░░██║░░░░░██╔══╝░░"
                  "\n\t\t╚█████╔╝██║░░░░░███████╗██║░░██║██║░░██║░░░██║░░░██║╚█████╔╝██║░╚███║██║░╚███║███████╗███████╗███████╗███████╗"
                  "\n\t\t░╚════╝░╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝╚═╝░░╚══╝╚══════╝╚══════╝╚══════╝╚══════╝"
                  "\n\t\t(Groupe D-1 | BAUDET Antoine, HOUEE Adrien, KOCOGLU Lucas)", "green"))


def menu_principal(choix=0):
    """
     * Fonction: menu_principal
     * -----------------
     * Fonction permettant d'afficher le menu principal.
     * Tant que l’utilisateur décide de tester un tableau de contraintes faire
     * Choix possibles :
     * 1. Lire un tableau de contraintes sur fichier
     * 2. Quitter le programme
    """
    # Boucle principale
    while True:
        print("---------------------- Menu Principal ----------------------"
              "\n1.\tLire un tableau de contraintes sur fichier"
              "\n2.\tQuitter le programme"
              "\n----------------------------------------------------------")
        try:
            # Demande de choix
            choix = int(input(colored("Entrez votre choix : ", "magenta")))
            match choix:
                case 1:
                    menu_choix_tableau()
                case 2:
                    return True
                case _:
                    print(colored("Le choix n'a pas été reconnue.", "red"))
        except ValueError:
            print(colored("Veuillez entrer un nombre entier valide.", "red"))
        except Exception as e:
            print(colored("Une erreur est survenue : " + str(e), "red"))


def menu_choix_tableau(choix=-1):
    string_test_files, index_test_files = files_list()

    if index_test_files is not None:
        print("---------------------- Menu Graphe ----------------------"
              + string_test_files +
              "----------------------------------------------------------")
        while True:
            try:
                # Demande de choix
                choix = int(input(colored("Entrez le numéro du fichier à traiter : ", "magenta")))
                # Sortie du menu
                if index_test_files[choix] == "Retour au menu principal":
                    break
                # Traitement du fichier
                elif choix in index_test_files.keys():
                    menu_choix_algorithme(index_test_files[choix], choix)

                    # Retour au menu
                    print("---------------------- Menu Graphe ----------------------"
                          + string_test_files +
                          "----------------------------------------------------------")
                # Choix non reconnu
                else:
                    print(colored("Le choix " + str(choix) + " n'a pas été reconnue.", "red"))
            except KeyError:
                print(colored("Le choix " + str(choix) + " n'a pas été reconnue.", "red"))
            except ValueError:
                print(colored("Veuillez entrer un nombre entier valide.", "red"))
            except Exception as e:
                print(colored("Une erreur est survenue : " + str(e), "red"))
    else:
        print(string_test_files)


def menu_choix_algorithme(choix_tableau, choix):
    tab_matrix = read_file(choix_tableau)
    # print(tab_matrix)

    if tab_matrix is not None:
        display_tab_matrix(tab_matrix, choix_tableau)
        input(colored("Appuyez sur une touche pour continuer...", "magenta"))

        # Choix de l'algorithme
        choices = {0: "Retour au menu précédent", 1: "Algorithme de Nord-Ouest", 2: "Algorithme de Ballas-Hammer"}
        str_choices = "\n"
        for i in choices:
            str_choices += str(i) + ".\t" + choices[i] + "\n"
        print("---------------------- Menu Algorithme ----------------------"
              + str_choices +
              "----------------------------------------------------------")
        while True:
            try:
                # Demande de choix
                choix = int(input(colored("Entrez le numéro de l'algorithme à utiliser : ", "magenta")))
                match choix:
                    case 0:
                        break
                    case 1:
                        print(colored("* Algorithme de Nord-Ouest", attrs=["bold", "underline"]))
                        northwest_matrix = northwest(tab_matrix)
                        # print(northwest_matrix)
                        display_tab_matrix(northwest_matrix, choix_tableau)
                        matrixtotalcost = totalcost(northwest_matrix)
                        print(colored("* Le coût total de la proposition de transport est de " + str(matrixtotalcost) + ".", "white"))
                        input(colored("Appuyez sur une touche pour continuer...", "magenta"))

                        steppingstone(northwest_matrix)
                    case 2:
                        print(colored("* Algorithme de Ballas-Hammer", attrs=["bold", "underline"]))
                        balas_hammer_matrix = balashammer(tab_matrix)
                        # print(balas_hammer_matrix)
                        display_tab_matrix(balas_hammer_matrix, choix_tableau)
                        matrixtotalcost = totalcost(balas_hammer_matrix)
                        print(colored("* Le coût total de la proposition de transport est de " + str(matrixtotalcost) + ".", "white"))
                        input(colored("Appuyez sur une touche pour continuer...", "magenta"))

                        steppingstone(balas_hammer_matrix)
                    case _:
                        print(colored("Le choix n'a pas été reconnue.", "red"))
                        continue
                break
            except KeyError:
                print(colored("Le choix " + str(choix) + " n'a pas été reconnue.", "red"))
            except ValueError:
                print(colored("Veuillez entrer un nombre entier valide.", "red"))
                continue
            except Exception as e:
                print(colored("Une erreur est survenue : " + str(e), "red"))
                continue


# Programme principal
if __name__ == "__main__":
    try:
        welcome()
        if menu_principal():
            exit(0)
        exit(1)
    except KeyboardInterrupt:
        print(colored("\nLe programme a été interrompu par l'utilisateur.", "red"))
        exit(0)
    except Exception as e:
        print(colored("Une erreur est survenue : " + str(e), "red"))
        exit(1)
