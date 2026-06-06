# Chapitre 4 : Algèbre Linéaire – Tableaux (Arrays)

Ce chapitre Apprendre à utiliser les tableaux (arrays) pour représenter des vecteurs et des matrices, essentiels en calcul scientifique.

**Tableaux NumPy** : Représentent des vecteurs, matrices et même des tenseurs.
**Création** : On peut créer un array à partir de listes Python avec np.array.
**Indexation et slices** : Permet d'accéder et de modifier les éléments d'un tableau.
**Opérations élémentaires** : Les opérations (addition, multiplication, etc.) s'appliquent élément par élément.
**Produit scalaire et matriciel** : Utilisation de .dot() ou @.
**Changement de forme** : Avec .reshape(), .transpose(), .stack(), etc.
**Fonctions utiles** : NumPy fournit des fonctions rapides comme np.sum, np.mean, etc.
**SciPy linalg** : Fournit des outils pour résoudre des systèmes d’équations linéaires, faire des décompositions LU ou SVD.
#### Ces outils sont très puissants pour manipuler facilement des données mathématiques sous forme de tableaux.


# Chapitre 5 : Concepts Avancés sur les Tableaux 

Ce chapitre Approfondir les notions d’optimisation et de manipulation avancée des tableaux NumPy. for.

**Copies vs Vues** :
 • Une vue (view) partage la même mémoire que l'original → rapide mais attention aux erreurs !
 • Une copie est indépendante → plus sûre mais plus lente.

**Tableaux booléens** : On peut filtrer les éléments avec des conditions, par exemple :
a[a > 0] retourne tous les éléments positifs.
**Indexation avancée** : Utilisation de np.where() ou des tableaux de booléens pour filtrer.
**Vectorisation** : Écrire du code sans boucles, avec des opérations sur des tableaux entiers → plus rapide.
**Broadcasting** : Permet d'appliquer des opérations entre tableaux de formes différentes (ex : addition d’un vecteur à chaque ligne d’une matrice).
**Matrices creuses (sparse matrices)** :
 • Utiles quand la majorité des valeurs sont nulles.
 • SciPy propose plusieurs formats (CSR, CSC, etc.) pour optimiser la mémoire.

#### Ces techniques rendent les programmes plus rapides, plus courts, et plus lisibles, ce qui est crucial en science des données ou en ingénierie.
