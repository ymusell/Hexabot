# Debrief du 15/01/2020

PO: Philibert ADAM


## Bilan

Pourcentage de tâches réalisées: 80%

### Ce qui a fonctionné

- Données de positionnement du robot par l'IMU publiées 
- Amélioration de l'éclairage avec un spot plus puissant
- Traitement des images en temps réel, catégorisation des fissure par nombre minimal de points
- Positionnement des fissures par rapport au robot, publiées sous forme de marker
- Mapping de la grotte grâce au lidar


### Ce qui n'a pas fonctionné

- Acquisition et traitement des données d'accélerations de l'IMU pour obtenir la vitesse
- Le lidar voit le sol ou le plafond à cause des mouvements du robot (variation de l'assiette)
- Actualisation de la position du robot sur rviz, non synchronisation entre affichage des fissures et positionnement du robot


### Retour d'expérience du PO

- Amélioration de l'utilisation du git mais le PO ne le gère pas
- L'estimation de la durée et du travail demandé pour les tâches est hasardeuse, certaines font apparaître de nouveaux problèmes imprévus
- Une tâche qui n'avance pas bloque le dévelopement du reste, difficile de bien rediriger les effeectifs afin d'aider 


### Conseils pour le prochain PO

- Mieux anticiper la longueur de chaque tâche afin de ne pas avoir de membre inactif ou ne sachant que faire
- Faire bien attention à la gestion du git
- Le PO doit gérer les pull requests


## Nouvelles mesures

- Nom des fichiers et des dossiers en anglais
- Contenu des README en français
- Nom de package en cohérence avec le contenu
- Le PO doit gérer lui-même les pulls requests
