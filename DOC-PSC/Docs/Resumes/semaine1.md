# Chapitre 1 : Introduction à Python#

Ce chapitre introduit les fondamentaux de Python et de l’environnement de développement :
**Installation**: Utilisation recommandée de la distribution Anaconda (inclut Python, Jupyter, Spyder, NumPy, etc.).
**Éditeurs:Python** pour l’interaction directe ; Spyder pour coder comme dans un Scripts Python : fichiers .py contenant du code exécuté avec python script.py
**Commentaires** : tout ce qui suit # n’est pas exécuté.
**Fonctions** : bloc de code réutilisable avec def :
**Contrôle de flux** : if, else, for, while
 
# Chapitre 2 : Variables et types de base 
**Variables** : une variable stocke une valeur (ex : a = 3).
**Types numériques** :
**int** : nombres entiers
**float** : nombres décimaux
**complex** : nombres complexes (ex: 3 + 2j)
**Booléens** : True, False, utilisés dans les conditions.
**Chaînes de caractères** : textes entre guillemets (ex: 'Bonjour').
**Conversions** : convertir entre types avec float(), int()…
**Tableaux avec NumPy**: NumPy introduit un nouveau type numérique appelé array, qui est plus performant que les listes standards pour le calcul scientifique.
**Création** :
import numpy as np
a = np.array([1, 2, 3])
b = np.array([[1, 2], [3, 4]])
Types de données : les tableaux peuvent contenir des float, int, ou même des complex.
Opérations : elles sont vectorisées (plus rapides) 
Accès aux éléments : identique aux listes, mais possible sur plusieurs dimensions :
      b[0, 1]  # deuxième élément de la première ligne
Les arrays permettent d'améliorer les performances dans les calculs scientifiques et numériques.

# Chapitre 3 : Types conteneurs 
**Listes** : [1, 2, 3], peuvent contenir n’importe quoi (nombres, texte, autres listes). On peut les parcourir avec une boucle for.
**Méthodes utiles** : append(), len(), zip().
**Tuples** : comme des listes mais immuables.
**Dictionnaires** : {'clé': 'valeur'} pour stocker des paires d’informations.
**Ensembles (sets)** : collection non ordonnée sans doublons.
**Conversions** : on peut transformer une liste en tuple, un set en liste...

# Notions que je maîtrise déjà :
    • Variables et types (int, float, bool)
    • Boucles for
    • Fonctions simples avec def
    • Utilisation basique de print()
    • Utilisation NumPy
# Notions à approfondir :
    • Manipulation de dictionnaires
    • Utilisation des modules et de l’espace de noms
    • Gestion des erreurs (try, except)
    • Complexité et performance des types conteneurs


# Codes Python associés
**Exercices Chap2**/Notebooks/Wxercices_2.6.ipynb
**Exercices Chap3**Notebooks/Wxercices_3.9.ipynb


# 1. Ce que nous avons fait 
    • Les bases de Python
    • Les types de données
    • Les conteneurs (listes, tuples, dictionnaires, ensembles)
    • Mise en place du dépôt GitHub
    • Création du fichier semaine1.md.
      
# 2. Ce que j’ai appris
    • Syntaxe de base Python (indentation, print, commentaires).
    • Types de données : int, float, bool, str.
    • Utilisation de variables, boucles (for, while) et conditions (if, else).
    • Création de fonctions simples avec def.
    • Premiers pas avec les listes, dictionnaires et tuples.
    • Importance de travailler dans un environnement isolé (conda, venv).
    • Utilisation de math.isclose() pour gérer les erreurs d’arrondi avec les float.
    • Introduction à NumPy : création de tableaux et opérations vectorisées.
      
# 3. Mes attentes pour les prochaines semaines
    • Approfondir NumPy avec les tableaux multidimensionnels, le slicing et la performance.
    • Découvrir Pandas pour la manipulation de données tabulaires.
    • Explorer Matplotlib pour la visualisation des résultats.
    • Comprendre les outils d’optimisation, calcul scientifique et calcul parallèle avec SciPy.
    • Continuer à structurer le projet dans le dépôt GitHub avec de bons exemples.
# 4. Les difficultés rencontrées
    • Faire la différence entre listes (modifiables) et tuples (immuables).
    • Choisir entre les structures de contrôle for, while ou if selon le contexte.
    • Maîtriser la syntaxe de Python, parfois sensible aux espaces et indentations.
    • Distinguer copies et vues dans NumPy.
    • Mémoriser des syntaxes complexes comme le slicing .
    • Adapter le niveau de détail dans les résumés (ni trop simple, ni trop long).
