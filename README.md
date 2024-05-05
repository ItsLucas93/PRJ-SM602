# PRJ-SM602
Projet SM602 - Recherche Opérationnelle, Promotion 2026 (Année 2024)

## Description du projet

L'objectif de ce projet est de résoudre un problème de recherche opérationnelle (problème de transport).
Le projet se base sur des tableaux de données (stockés dans `tables/table x.txt`) qui représentent les coûts de transport entre des points de départ et des points d'arrivée.
Le programme doit déterminer le plan de transport optimal qui minimise les coûts de transport via la **méthode de marche-pieds**, avec un plan de transport initialisé via **Nord-Ouest** ou **Ballas-Hammer**.

## Structure du projet

Les données sont stockées dans le dossier `tables/` sous forme de fichiers texte. Chaque fichier représente un tableau de coûts de transport.

Les traces d'exécution du programme sont stockées dans le dossier `logs/`.

Les données sur la complexité des algorithmes sont stockées dans le dossier `complexity/`.

### Structure du projet :

```bash
├── LICENSE
├── README.md
├── algorithms
│      ├── balashammer.py
│      ├── complexity_check.py
│      ├── northwest.py
│      ├── steppingstone.py
│      └── totalcost.py
├── complexity
│      ├── Balas-Hammer_10.txt
│      ├── Balas-Hammer_100.txt
│      ├ [...]
│      ├── Stepping Stone - North West_400.txt
│      └── Stepping Stone - North West_4000.txt
├── display_tab.py
├── file_manager.py
├── logs
│      ├── D-1-trace1-bh.txt
│      ├── D-1-trace1-no.txt
│      ├ [...]
│      ├── D-1-trace12-bh.txt
│      └── D-1-trace12-no.txt
├── main.py
└── tables
    ├── table 1.txt
    ├ [...]
    └── table 12.txt
```

### Exemple d'exécution :

```python
----------------------------------------------------------
Entrez le numéro du fichier à traiter : 5
┍━━━━━━━━━━━━━━━┯━━━━━━┯━━━━━━┯━━━━━━┯━━━━━━━━━━━━━━━━━┑
│  table 5.txt  │  C₁  │  C₂  │  C₃  │  Provisions Pᵢ  │
┝━━━━━━━━━━━━━━━┿━━━━━━┿━━━━━━┿━━━━━━┿━━━━━━━━━━━━━━━━━┥
│      P₁       │ 0 ₅  │ 0 ₇  │ 0 ₈  │       25        │
├───────────────┼──────┼──────┼──────┼─────────────────┤
│      P₂       │ 0 ₆  │ 0 ₈  │ 0 ₅  │       25        │
├───────────────┼──────┼──────┼──────┼─────────────────┤
│      P₃       │ 0 ₆  │ 0 ₇  │ 0 ₇  │       25        │
├───────────────┼──────┼──────┼──────┼─────────────────┤
│ Commandes Cᵢ  │  35  │  20  │  20  │                 │
┕━━━━━━━━━━━━━━━┷━━━━━━┷━━━━━━┷━━━━━━┷━━━━━━━━━━━━━━━━━┙
Appuyez sur une touche pour continuer...
---------------------- Menu Algorithme ----------------------
0.	Retour au menu précédent
1.	Algorithme de Nord-Ouest
2.	Algorithme de Ballas-Hammer
----------------------------------------------------------
Entrez le numéro de l'algorithme à utiliser : 2
* Algorithme de Ballas-Hammer
Souhaitez-vous afficher les itérations ? (y/n)... y

* Itération n°1
Appuyez sur une touche pour continuer...
┍━━━━━━━━━━━━━━━━┯━━━━━━┯━━━━━━┯━━━━━━┯━━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━┑
│  Balas-Hammer  │  C₁  │  C₂  │  C₃  │  Provisions Pᵢ  │  Pénalités  │
┝━━━━━━━━━━━━━━━━┿━━━━━━┿━━━━━━┿━━━━━━┿━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━┥
│       P₁       │ 0 ₅  │ 0 ₇  │ 0 ₈  │       25        │      2      │
├────────────────┼──────┼──────┼──────┼─────────────────┼─────────────┤
│       P₂       │ 0 ₆  │ 0 ₈  │ 0 ₅  │       25        │      1      │
├────────────────┼──────┼──────┼──────┼─────────────────┼─────────────┤
│       P₃       │ 0 ₆  │ 0 ₇  │ 0 ₇  │       25        │      1      │
├────────────────┼──────┼──────┼──────┼─────────────────┼─────────────┤
│  Commandes Cᵢ  │  35  │  20  │  20  │                 │             │
├────────────────┼──────┼──────┼──────┼─────────────────┼─────────────┤
│   Pénalités    │  1   │  0   │  2   │                 │             │
┕━━━━━━━━━━━━━━━━┷━━━━━━┷━━━━━━┷━━━━━━┷━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━┙
┍━━━━━━━━━━━━━━━━┯━━━━━━┯━━━━━━┯━━━━━━┯━━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━┑
│  Balas-Hammer  │  C₁  │  C₂  │  C₃  │  Provisions Pᵢ  │  Pénalités  │
┝━━━━━━━━━━━━━━━━┿━━━━━━┿━━━━━━┿━━━━━━┿━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━┥
│       P₁       │ 25 ₅ │ 0 ₇  │ 0 ₈  │       25        │      2      │
├────────────────┼──────┼──────┼──────┼─────────────────┼─────────────┤
│       P₂       │ 0 ₆  │ 0 ₈  │ 0 ₅  │       25        │      1      │
├────────────────┼──────┼──────┼──────┼─────────────────┼─────────────┤
│       P₃       │ 0 ₆  │ 0 ₇  │ 0 ₇  │       25        │      1      │
├────────────────┼──────┼──────┼──────┼─────────────────┼─────────────┤
│  Commandes Cᵢ  │  35  │  20  │  20  │                 │             │
├────────────────┼──────┼──────┼──────┼─────────────────┼─────────────┤
│   Pénalités    │  1   │  0   │  2   │                 │             │
┕━━━━━━━━━━━━━━━━┷━━━━━━┷━━━━━━┷━━━━━━┷━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━┙
```

## Exécuter le programme

Le projet a été codé sur la version 3.12 de Python.
Il est demandé à l'utilisateur d'installer la version 3.12 de [Python](https://www.python.org/downloads/).

Pour vérifier la version de Python installée sur votre machine :
```bash
python3 --version
```

Avant de lancer votre programme, des modules tiers doivent être installés : `tabulate`, `termcolor`, `tqdm`. Pour installer ces modules :
```bash
pip3 install tabulate termcolor tqdm
```

Pour lancer le programme, exécutez le fichier `main.py` (Soit par la commande sur votre terminal, soit dans un IDE type [PyCharm](https://www.jetbrains.com/fr-fr/pycharm/download)) :
```bash
python3 main.py
```

## Auteurs du projet

Ce projet est proposé par le département de Mathématiques à l'[Efrei Paris Panthéon Assas Université](https://www.efrei.fr/).

Membres actif du groupe :
- [Antoine BAUDET](https://github.com/Kenix0)
- [Lucas KOCOGLU](https://github.com/ItsLucas93)
