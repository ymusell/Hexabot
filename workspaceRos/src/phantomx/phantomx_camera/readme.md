# phantomx_camera

Ce package regroupe tous les scrits et fichiers relatifs au traitement d'image des fissur, à leur localisation et à leur positionnement.

## test_images

Images de test permettant de tester les algorithmes de traitement d'image en dehors de l'architecture ROS

## src

Dossier contenant les scripts.

### visualize_camera

Programme qui s'abonne à la caméra rgbd du robot et qui retourne des points d'une faille (si il en détecte) dans le repère du robot.

Ce fichier est à inclure dans le .launch général.

### camera_lib

Librairie utilisée par visualize_camera.

### id_on_test_image

Librairie utilisée par tester les algorithmes de traitement d'image.