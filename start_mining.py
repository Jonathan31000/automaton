import threading
from datetime import datetime
from boucle_multibot_v1 import loop_shoop, loop_incomme, look_check_stuck

locks = {}
task_state = {}

# Fonction 1, exécutée par le premier sous-thread
def task_one(device_name, capture_name, port):
    # Enregistre l'heure de début au format datetime
    start_time = datetime.now()

    # Crée un verrou pour le device_name s'il n'existe pas encore
    if device_name not in locks:
        locks[device_name] = threading.Lock()

    with locks[device_name]:
        print(f"Thread 1 pour {device_name} commence à {start_time}.")
        loop_shoop(device_name, capture_name, port)
        print(f"Thread 1 pour {device_name} terminé.")
        
        # Mettre à jour l'état de la tâche task_one pour indiquer qu'elle est terminée
        task_state[device_name]["task_one_active"] = False  

    # Redémarrer la tâche en ajustant le temps en fonction du délai de 20 minutes
    if not task_state[device_name]["task_one_active"]:
        task_state[device_name]["task_one_active"] = True

        # Calcul de l'heure actuelle et du délai restant
        now = datetime.now()
        elapsed_time = (now - start_time).total_seconds()
        delay = max(0, 1300 - elapsed_time)  # Délai restant en secondes
        # Lancer le redémarrage de la tâche après le délai calculé
        threading.Timer(delay, task_one, args=(device_name, capture_name, port)).start()
"""def task_one(device_name, capture_name, port):
    if device_name not in locks:
        locks[device_name] = threading.Lock()
    with locks[device_name]:
        print(f"Thread 1 pour {device_name} commence.")
        loop_shoop(device_name, capture_name, port)
        print(f"Thread 1 pour {device_name} terminé.")
        
        # Mettre à jour l'état de la tâche task_one
        task_state[device_name]["task_one_active"] = False  # Task one est terminée

    # Redémarrer la tâche toutes les 20 minutes si elle n'est pas déjà en cours
    if not task_state[device_name]["task_one_active"]:
        task_state[device_name]["task_one_active"] = True
        threading.Timer(20 * 60, task_one, args=(device_name, capture_name, port)).start()"""

# Fonction 2, exécutée par le deuxième sous-thread
def task_two(device_name, capture_name, port):
    if device_name not in locks:
        locks[device_name] = threading.Lock()
    with locks[device_name]:
        print(f"Thread 2 pour {device_name} commence.")
        loop_incomme(device_name, capture_name, port)
        print(f"Thread 2 pour {device_name} terminé.")
        
        # Mettre à jour l'état de la tâche task_two
        task_state[device_name]["task_two_active"] = False  # Task two est terminée

    # Redémarrer la tâche toutes les 5 heures si elle n'est pas déjà en cours
    if not task_state[device_name]["task_two_active"]:
        task_state[device_name]["task_two_active"] = True
        threading.Timer(60 * 60 * 5, task_two, args=(device_name, capture_name, port)).start()

def start_mining(device_names, capture_names, ports):
    def mining_task_for_device(device_name, capture_name, port):
        # Initialiser l'état de chaque tâche pour le périphérique
        task_state[device_name] = {
            "task_one_active": False,  # Initialement inactive
            "task_two_active": False   # Initialement inactive
        }
        
        # Crée les sous-threads pour chaque périphérique
        sub_threads = []
        
        # Sous-thread 1 pour task_one
        thread_1 = threading.Thread(target=task_one, args=(device_name, capture_name, port))
        sub_threads.append(thread_1)
        thread_1.start()
        
        # Sous-thread 2 pour task_two
        thread_2 = threading.Thread(target=task_two, args=(device_name, capture_name, port))
        sub_threads.append(thread_2)
        thread_2.start()
        
        # Attendre que les sous-threads se terminent (ceci pourrait être optionnel
        # selon le comportement souhaité)
        
        print(f"Tâches pour {device_name} terminées.")
    
    # Crée un thread principal pour chaque périphérique
    threads = []
    for (device_name, capture_name, port) in zip(device_names, capture_names, ports):
        thread = threading.Thread(target=mining_task_for_device, args=(device_name, capture_name, port))
        threads.append(thread)
        thread.start()
        
    # Attendre que tous les threads principaux terminent
    for thread in threads:
        thread.join()

# Exemple d'utilisation
device_names = ["127.0.0.1:5555", "127.0.0.1:5585", "127.0.0.1:5595"]  # Liste des périphériques
capture_names = ["capture1.png", "capture2.png", "capture3.png"]
ports = ["http://127.0.0.1:4723", "http://127.0.0.1:4724", "http://127.0.0.1:4725"]
start_mining(device_names, capture_names, ports)
