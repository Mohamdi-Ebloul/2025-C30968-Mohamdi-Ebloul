# Differentiable physics-enabled_closure modeling for Burgers turbulence – Synthèse

## 1. Problématique  
Modéliser la turbulence avec précision reste un défi majeur. Ce travail se concentre sur le modèle de closure—la représentation de l’impact des petites échelles sur les grandes—dans le contexte de la turbulence de Burgers, un modèle 1D emblématique abordant la dynamique de l’advection–dissipation. Les approches purement basées sur l’apprentissage automatique échouent souvent par manque de structure physique, et les méthodes traditionnelles brident les possibilités. L’enjeu : concevoir un modèle de closure à la fois généralisable, interprétable, et indépendant de la résolution de grille.

## 2. Approche proposée  
**Introduction du differentiable physics** : intégrer un solveur PDE compatible avec l’autodifférentiation, permettant un entraînement en a posteriori directement sur les champs de vitesse 
**Utilisation de neural operators non-locaux pour assurer l’indépendance à la résolution (la grille)** : le modèle apprend globalement, pas seulement localement.
**Exploration d’une gamme de modèles** : des architectures « boîte noire » jusqu’à celles imposant des contraintes physiques explicites (injectant des approximations comme Boussinesq ou Smagorinsky).

## 3. Technologies utilisées  
**1**. Solveur PDE différentiable couplé à un réseau neuronal afin d’effectuer l’entraînement end-to-end avec gradients rétropropagés à travers la simulation .
**2**.Neural operators non-locaux pour capturer les interactions à distance et pour fonctionner sur plusieurs résolutions de grille .
**3**.Inductive bias physique : incorporation de lois de conservation, invariance, et ajustement du modèle de Smagorinsky avec un coefficient calculé par le réseau . 


## 4. Perspectives de recherche  
**Performance largement améliorée** : le modèle entraîné via differentiable physics dépasse les closures classiques et les modèles ML non structurés sur divers nombres de Reynolds et résolutions 
**Robustesse multi-grille** : résultat maintenu sans réentrainement sur différentes résolutions.
**Interprétabilité** via la structure du modèle, facilitant la compréhension physique.
Étendre à des systèmes PDE plus complexes (Navier–Stokes 2D ou 3D).
Améliorer la scalabilité du differentiable physics à des simulations volumineuses.
Etudier la structure du réseau pour une meilleure interprétation physique dans des modèles réalistes.
