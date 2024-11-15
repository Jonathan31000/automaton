import cv2
import numpy as np
import os
import cv2
import os
import numpy as np

def detect_templates_in_folder(capture_path, template_folder, threshold=0.8):
    # Charger l'image capturée
    img = cv2.imread(capture_path, 0)  # Charger en noir et blanc
    # Vérifier si l'image capturée est correctement chargée
    if img is None:
        print("Erreur : L'image capturée n'a pas pu être chargée.")
        exit()  # Quitter si l'image capturée est invalide

    # Afficher l'image capturée pour débogage
    cv2.imshow("Captured Image", img)
    cv2.waitKey(0)  # Attendre que l'utilisateur ferme la fenêtre
    cv2.destroyAllWindows()

    # Vérifier si le dossier existe
    if not os.path.exists(template_folder):
        print(f"Erreur : Le dossier '{template_folder}' n'existe pas.")
        exit()

    # Afficher les dimensions de l'image capturée pour débogage
    print(f"Dimensions de l'image capturée : {img.shape}")

    # Parcourir tous les fichiers dans le dossier de templates
    for template_name in os.listdir(template_folder):
        template_path = os.path.join(template_folder, template_name)

        # Vérifier si c'est un fichier image (ajustez les extensions si nécessaire)
        if not template_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        
        # Charger le template
        template = cv2.imread(template_path, 0)  # Charger en noir et blanc

        # Vérifier si le template est correctement chargé
        if template is None:
            print(f"Erreur : Le template '{template_name}' n'a pas pu être chargé.")
            continue  # Passer au template suivant si celui-ci est invalide

        # Afficher les dimensions du template pour débogage
        print(f"Dimensions du template '{template_name}' : {template.shape}")

        # Effectuer la correspondance de modèle avec le template redimensionné
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

        # Afficher la sortie de matchTemplate pour voir les résultats
        cv2.imshow("Template Match Result", res)
        cv2.waitKey(0)  # Attendre que l'utilisateur ferme la fenêtre
        cv2.destroyAllWindows()

        # Trouver les endroits où la correspondance est élevée
        loc = np.where(res >= threshold)

        # Afficher les résultats pour chaque correspondance
        for pt in zip(*loc[::-1]):
            print("in")
            # Calculer les coordonnées du centre du rectangle
            center_x = pt[0] + template.shape[1] / 2
            center_y = pt[1] + template.shape[0] / 2

            # Afficher le centre
            print(f"Centre trouvé pour '{template_name}' à : ({center_x}, {center_y})")

            # Dessiner un rectangle autour de la correspondance
            cv2.rectangle(img, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 0, 255), 2)

            # Dessiner un cercle au centre
            cv2.circle(img, (int(center_x), int(center_y)), 5, (0, 255, 0), -1)

    # Afficher l'image avec les résultats
    cv2.imshow("Detected", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
capture_path = 'capture1.png'  # Chemin vers l'image capturée
template_folder = 'image/image_income/'  # Chemin vers le dossier contenant les templates
detect_templates_in_folder(capture_path, template_folder, threshold=0.8)
# Exécution de la fonction avec le chemin de l'image capturée et le dossier de templates
"""capture_path = 'capture1.png'  # Chemin vers l'image capturée
template_folder = 'image/test/'  # Chemin vers le dossier contenant les templates
img = cv2.imread('capture1.png', 0)  # Charger en noir et blanc
if img is None:
    print("Erreur de chargement de l'image.")
else:
    print(f"Taille de l'image : {img.shape}")

    # Redimensionner l'image si elle est trop grande pour l'affichage
    img = cv2.resize(img, (img.shape[1] // 2, img.shape[0] // 2))  # Divise par 2 les dimensions

    cv2.imshow("capture1", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
"""