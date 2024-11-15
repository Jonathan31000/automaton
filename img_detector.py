import cv2
import numpy as np
import os
import time
import shutil

# Dimensions de l'écran de bluestack
screen_width = 900
screen_height = 1600

# Dimensions de la capture d'écran
capture_width = 549  # La largeur de la capture d'écran (incluant la barre d'actions)
capture_height = 950  # La hauteur de la capture d'écran (incluant la barre d'actions)

"""scale_x = screen_width / capture_width
scale_y = screen_height / capture_height"""
scale_x = 1
scale_y = 1

def find_pass_center(template_folder_path, image_path):
    center_pos = []  # Liste pour stocker les centres trouvés
    # Charger l'image sur laquelle effectuer la recherche
    img = cv2.imread(image_path, 0)  # Charger en niveaux de gris

    # Vérifier si l'image capturée est correctement chargée
    if img is None:
        print(f"Erreur : L'image '{image_path}' n'a pas pu être chargée.")
        return center_pos  # Retourner une liste vide si l'image est invalide

    # Vérifier si le dossier contenant les templates existe
    if not os.path.exists(template_folder_path):
        print(f"Erreur : Le dossier '{template_folder_path}' n'existe pas.")
        return center_pos  # Retourner une liste vide si le dossier n'existe pas

    # Parcourir tous les fichiers dans le dossier des templates
    for template_name in os.listdir(template_folder_path):
        template_path = os.path.join(template_folder_path, template_name)
        
        # Vérifier si c'est un fichier image
        if not template_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        
        # Charger le template
        template = cv2.imread(template_path, 0)  # Charger en niveaux de gris

        # Vérifier si le template a été correctement chargé
        if template is None:
            print(f"Erreur : Le template '{template_name}' n'a pas pu être chargé.")
            continue  # Passer au template suivant si celui-ci est invalide

        #print(f"Test du template : {template_name}")

        # Effectuer la correspondance de modèle
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

        # Trouver les endroits où la correspondance est élevée
        threshold = 0.8
        loc = np.where(res >= threshold)

        # Afficher les résultats pour ce template
        for pt in zip(*loc[::-1]):  # Pour chaque correspondance
            # Calculer les coordonnées du centre du rectangle
            center_x = pt[0] + template.shape[1] / 2
            center_y = pt[1] + template.shape[0] / 2
                    
            x_emulateur = center_x * scale_x
            y_emulateur = center_y * scale_y
            # Ajouter le centre à la liste
            center_pos.append((int(x_emulateur), int(y_emulateur)))  # Ajout d'un tuple (x, y) dans la liste
         # Vérifier s'il n'y a eu aucun match trouvé
        """if not center_pos:
            # Créer le dossier img_treatment s'il n'existe pas
            unmatch_folder = "img_treatment"
            os.makedirs(unmatch_folder, exist_ok=True)
            
            # Compter les fichiers "unmatch" déjà présents pour le nommage
            unmatch_count = len([f for f in os.listdir(unmatch_folder) if f.startswith("unmatch")])
            
            # Sauvegarder l'image dans img_treatment
            unmatch_filename = f"unmatch{unmatch_count}.png"
            unmatch_path = os.path.join(unmatch_folder, unmatch_filename)
            cv2.imwrite(unmatch_path, img)  # Sauvegarder l'image originale
            print(f"Aucun match trouvé. Image sauvegardée sous '{unmatch_filename}'.")"""
    return center_pos

def detect_template_color(image_path, template_folder_path):
    # Charger l'image en couleur (BGR)
    img = cv2.imread(image_path)  # Chargement en BGR (par défaut OpenCV charge en BGR)

    # Vérifier si l'image a été correctement chargée
    if img is None:
        print(f"Erreur : L'image '{image_path}' n'a pas pu être chargée.")
        return False

    # Obtenir tous les fichiers dans le dossier template_folder_path
    templates = [f for f in os.listdir(template_folder_path) if os.path.isfile(os.path.join(template_folder_path, f))]

    # Parcourir tous les templates du dossier
    for template_file in templates:
        template_path = os.path.join(template_folder_path, template_file)
        
        # Charger le template
        template = cv2.imread(template_path)

        # Vérifier si le template a été correctement chargé
        if template is None:
            print(f"Erreur : Le template '{template_path}' n'a pas pu être chargé.")
            continue  # Passer au prochain template si celui-ci ne peut être chargé

        # Effectuer la correspondance de modèle en couleur
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

        # Trouver les endroits où la correspondance est élevée
        threshold = 0.8
        loc = np.where(res >= threshold)

        # Si une correspondance est trouvée, retourner True
        if len(loc[0]) > 0:
            print(f"Template trouvé : {template_file}")
            return True  # Si une correspondance est trouvée, on retourne immédiatement True

    # Si aucun template n'a trouvé de correspondance, retourner False
    return False

def detect_templates_with_gradient(template_folder, image_path, threshold=0.8):
    # Charger l'image principale en couleur (BGR)
    img = cv2.imread(image_path)

    # Vérifier si l'image principale est correctement chargée
    if img is None:
        print(f"Erreur : L'image '{image_path}' n'a pas pu être chargée.")
        return False

    # Convertir l'image principale en niveaux de gris et calculer son gradient
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grad_img_x = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)  # Gradient en x
    grad_img_y = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)  # Gradient en y
    grad_img = cv2.magnitude(grad_img_x, grad_img_y)  # Magnitude du gradient (en combinant x et y)

    # Vérifier si le dossier de templates existe
    if not os.path.exists(template_folder):
        print(f"Erreur : Le dossier '{template_folder}' n'existe pas.")
        return False

    # Parcourir tous les fichiers dans le dossier de templates
    for template_name in os.listdir(template_folder):
        template_path = os.path.join(template_folder, template_name)

        # Vérifier si c'est un fichier image
        if not template_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        # Charger le template
        template = cv2.imread(template_path)

        # Vérifier si le template est correctement chargé
        if template is None:
            print(f"Erreur : Le template '{template_name}' n'a pas pu être chargé.")
            continue

        # Convertir le template en niveaux de gris et calculer son gradient
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        grad_template_x = cv2.Sobel(template_gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_template_y = cv2.Sobel(template_gray, cv2.CV_64F, 0, 1, ksize=3)
        grad_template = cv2.magnitude(grad_template_x, grad_template_y)

        # Effectuer la correspondance de modèle avec les gradients
        res = cv2.matchTemplate(grad_img.astype(np.float32), grad_template.astype(np.float32), cv2.TM_CCOEFF_NORMED)

        # Trouver les endroits où la correspondance est élevée
        loc = np.where(res >= threshold)

        # Si une correspondance est trouvée, afficher le template correspondant et retourner True
        if len(loc[0]) > 0:
            print(f"Correspondance trouvée avec le template '{template_name}'")
            return True

    # Si aucune correspondance n'a été trouvée pour aucun template, retourner False
    print("Aucune correspondance trouvée.")
    return False

def load_and_resize_image(image_path, target_width, target_height):
    # Charger l'image en niveaux de gris (0 signifie niveaux de gris)
    img = cv2.imread(image_path, 0)

    # Vérifier si l'image a été chargée
    if img is None:
        print(f"Erreur : L'image '{image_path}' n'a pas pu être chargée.")
        return None
    
    # Redimensionner l'image
    resized_img = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_AREA)

    return resized_img

def capture_and_compare_screenshots(driver, capture_folder="screenshots"):
    """
    Cette fonction prend des captures d'écran toutes les 15 secondes,
    les stocke dans un dossier créé à la volée et compare les deux dernières captures.
    Si les images sont identiques, elle retourne True et supprime le dossier.
    """
    # Créer le dossier pour les captures d'écran s'il n'existe pas
    if not os.path.exists(capture_folder):
        os.makedirs(capture_folder)
    
    # Variables pour les noms des captures d'écran
    photo1_path = os.path.join(capture_folder, "photo1.png")
    photo2_path = os.path.join(capture_folder, "photo2.png")

    # Boucle infinie pour prendre des captures toutes les 15 secondes
    while True:
        # Si la photo1 existe, on la supprime avant de prendre la nouvelle photo
        if os.path.exists(photo1_path):
            os.remove(photo1_path)

        # Prendre la capture d'écran et la stocker dans photo2
        screenshot = driver.get_screenshot_as_file(photo2_path)
        if not screenshot:
            print("Erreur lors de la capture d'écran")
            break

        # Déplacer la photo2 vers photo1 (avant de prendre une nouvelle photo)
        if os.path.exists(photo2_path):
            shutil.move(photo2_path, photo1_path)
        
        # Attendre 15 secondes avant de capturer une nouvelle image
        time.sleep(15)

        # Après le 2ème tour, on compare les images
        if os.path.exists(photo1_path) and os.path.exists(photo2_path):
            # Comparer les deux images
            if compare_images(photo1_path, photo2_path):
                print("Les deux captures sont identiques.")
                # Supprimer le dossier
                shutil.rmtree(capture_folder)
                return True  # Retourner True si les images sont identiques
        
        # Après le premier tour, on continue la boucle pour le deuxième tour

def compare_images(image1_path, image2_path):
    img1 = cv2.imread(image1_path, 0)
    img2 = cv2.imread(image2_path, 0)

    if img1 is None or img2 is None:
        print("Erreur lors du chargement des images.")
        return False

    # Comparer les deux images en utilisant la méthode de comparaison de différence d'images
    difference = cv2.absdiff(img1, img2)
    return cv2.countNonZero(difference) == 0  # Si aucune différence, les images sont identiques