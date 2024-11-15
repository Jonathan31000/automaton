import mss
import pygetwindow as gw
from PIL import Image
from screeninfo import get_monitors


def screen_maker(capture_name):
    window_name = ""
    if capture_name == "capture1.png":
        window_name = "Machine_num_1"
    elif capture_name == "capture2.png":
        window_name = "Machina_del_numero_1"
    # Récupérer les informations sur les moniteurs
    moniteurs = get_monitors()

    # Afficher les informations des écrans
    for i, monitor in enumerate(moniteurs):
        print(f"Moniteur {i+1}: {monitor}")

    # Supposons que nous voulons capturer le deuxième moniteur (écran secondaire)
    if len(moniteurs) > 1:
        monitor = moniteurs[1]  # Deuxième écran
        
        # Récupérer la fenêtre Bluestacks (en arrière-plan)
        try:
            window = gw.getWindowsWithTitle(window_name)[0]  # Trouver Bluestacks
        except IndexError:
            print("Erreur : Aucune fenêtre Bluestacks trouvée.")
            exit()

        # Récupérer les coordonnées de la fenêtre Bluestacks sur l'écran secondaire
        left, top, right, bottom = window.left, window.top, window.right, window.bottom

        # Ajuster les coordonnées pour s'assurer que la capture correspond au moniteur secondaire
        if left >= monitor.x and top >= monitor.y:  # Si la fenêtre est sur le deuxième écran
            width = right - left
            height = bottom - top
            
            # Capture de l'écran sur le deuxième moniteur (coordonnées ajustées)
            with mss.mss() as sct:
                # Capture de la région
                screenshot = sct.grab({
                    "left": left,
                    "top": top,
                    "width": width,
                    "height": height
                })

                # Sauvegarder l'image dans 'capture.png'
                screenshot_image = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
                screenshot_image.save(capture_name)

                # Afficher l'image capturée
                #screenshot_image.show()

        else:
            print("La fenêtre Bluestacks n'est pas sur le deuxième écran.")
    else:
        print("Aucun moniteur secondaire trouvé.")
