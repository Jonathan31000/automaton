import threading
import time
import os
import shutil
import cv2
from boucle_multibot_v1 import loop_shoop, loop_incomme

locks = {}

# Fonction pour comparer deux images
def compare_images(image1_path, image2_path):
    img1 = cv2.imread(image1_path, 0)
    img2 = cv2.imread(image2_path, 0)

    if img1 is None or img2 is None:
        print("Erreur lors du chargement des images.")
        return False

    # Comparer les deux images en utilisant la méthode de comparaison de différence d'images
    difference = cv2.absdiff(img1, img2)
    return cv2.countNonZero(difference) == 0  # Si aucune différence, les images sont identiques

# Fonction qui capture une image pour vérifier si le périphérique est bloqué
def capture_screen(device_name, capture_folder="device_screenshots"):
    if not os.path.exists(capture_folder):
        os.makedirs(capture_folder)

    timestamp = int(time.time())
    image_path = os.path.join(capture_folder, f"{device_name}_{timestamp}.png")
    
    # Simuler la capture d'écran, ici il faudra une fonction qui capture l'écran réel
    # Exemple : driver.get_screenshot_as_file(image_path) pour un périphérique réel
    return image_path

# Fonction pour vérifier si le périphérique est bloqué en comparant les images
def check_device_stuck(device_name, capture_folder="device_screenshots"):
    previous_image = None
    
    while True:
        # Capturer une nouvelle image
        new_image = capture_screen(device_name, capture_folder)

        if previous_image:
            # Comparer la nouvelle image avec la précédente
            if compare_images(previous_image, new_image):
                print(f"{device_name} est bloqué.")
                shutil.rmtree(capture_folder)  # Supprimer le dossier des captures
                return True  # Le périphérique est bloqué
            else:
                print(f"{device_name} n'est pas bloqué.")

        previous_image = new_image
        time.sleep(15)  # Attendre 15 secondes avant de capturer à nouveau

# Fonction 1, exécutée par le premier sous-thread
def task_one(device_name, capture_name, port):
    if device_name not in locks:
        locks[device_name] = threading.Lock()
    with locks[device_name]:
        print(f"Thread 1 pour {device_name} commence.")
        loop_shoop(device_name, capture_name, port)
        print(f"Thread 1 pour {device_name} terminé.")
    # Redémarrer la tâche toutes les 20 minutes
    threading.Timer(20 * 60, task_one, args=(device_name, capture_name, port)).start()

# Fonction 2, exécutée par le deuxième sous-thread
def task_two(device_name, capture_name, port):
    if device_name not in locks:
        locks[device_name] = threading.Lock()
    with locks[device_name]:
        print(f"Thread 2 pour {device_name} commence.")
        loop_incomme(device_name, capture_name, port)
        print(f"Thread 2 pour {device_name} terminé.")
    # Redémarrer la tâche toutes les 20 minutes
    threading.Timer(60 * 60 * 5, task_two, args=(device_name, capture_name, port)).start()

# Fonction 3, vérifie périodiquement si le périphérique est "stuck"
def task_three(device_name):
    print(f"Thread 3 pour {device_name} commence.")
    # Cette fonction va régulièrement vérifier si le périphérique est bloqué
    is_stuck = check_device_stuck(device_name)
    if is_stuck:
        print(f"{device_name} est bloqué et a été arrêté.")
    else:
        print(f"{device_name} est en fonctionnement.")
    # Redémarrer la tâche toutes les 15 secondes pour vérifier l'état du périphérique
    threading.Timer(15, task_three, args=(device_name,)).start()

# Fonction qui crée un thread principal pour chaque device_name
def start_mining(device_names, capture_names, ports):
    def mining_task_for_device(device_name, capture_name, port):
        # Crée les trois sous-threads pour chaque périphérique
        sub_threads = []
        
        # Sous-thread 1
        thread_1 = threading.Thread(target=task_one, args=(device_name, capture_name, port))
        sub_threads.append(thread_1)
        thread_1.start()
        
        # Sous-thread 2
        thread_2 = threading.Thread(target=task_two, args=(device_name, capture_name, port))
        sub_threads.append(thread_2)
        thread_2.start()

        # Sous-thread 3 (ajouté pour vérifier si le périphérique est bloqué)
        thread_3 = threading.Thread(target=task_three, args=(device_name,))
        sub_threads.append(thread_3)
        thread_3.start()

        # Attendre que tous les sous-threads se terminent
        for sub_thread in sub_threads:
            sub_thread.join()

        print(f"Tâches pour {device_name} terminées.")

    # Crée un thread principal pour chaque appareil dans la liste
    threads = []
    for (device_name, capture_name, port) in zip(device_names, capture_names, ports):
        thread = threading.Thread(target=mining_task_for_device, args=(device_name, capture_name, port))
        threads.append(thread)
        thread.start()

    # Attendre la fin de tous les threads principaux
    for thread in threads:
        thread.join()

# Exemple d'utilisation
device_names = ["127.0.0.1:5555", "127.0.0.1:5585"]  # Liste des périphériques
capture_names = ["capture1.png", "capture2.png"]
ports = ["http://127.0.0.1:4723", "http://127.0.0.1:4724"]
start_mining(device_names, capture_names, ports)
