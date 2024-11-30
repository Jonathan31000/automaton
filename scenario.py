from appium import webdriver
from appium.options.android import UiAutomator2Options
from method import Method
from img_detector import find_pass_center
from img_detector import detect_template_color, compare_images
import time
import numpy as np
import cv2


uiAutoPort = {
    "127.0.0.1:5555": 8200, 
    "127.0.0.1:5585": 8201, 
    "127.0.0.1:5595": 8202
}

options = UiAutomator2Options()
options.set_capability('platformName', 'Android')
options.set_capability('platformVersion', '9')  # Version de ton émulateur Android
options.set_capability('automationName', 'UiAutomator2')
options.set_capability('noReset', True)
options.set_capability('newCommandTimeout', 500)

class Scenario:

    def from_map_to_pub_reward(device_name, capture_name, port):
        options.set_capability('udid', device_name)  # ID de l'émulateur ou appareil réel
        options.set_capability('systemPort', uiAutoPort[device_name]) 
        driver = webdriver.Remote(
            command_executor=port,  # URL du serveur Appium
            options=options  # Pass the options here instead of 'desired_capabilities'
        )
        
        timeout = 2
        Method.go_back_to_map_view(driver)
        time.sleep(timeout)
        driver.tap([(57, 838)])
        center = find_pass_center("image/img_shop", capture_name)
        
        # Attente que la capture soit trouvée
        while len(center) == 0:
            driver.get_screenshot_as_file(capture_name)
            print("I'm waiting")
            time.sleep(1)
            center = find_pass_center("image/img_shop", capture_name)
            
        Method.swipe_pub(driver)
        
        valide = False
        start_time = time.time()  # Temps initial pour vérifier la durée
        previous_image = None  # Variable pour la capture d'écran précédente
        
        while valide is False:
            driver.get_screenshot_as_file(capture_name)
            # Ouvrir l'image capturée avec OpenCV
            current_image = cv2.imread(capture_name)

            elapsed_time = 0
            if previous_image is not None:
                # Comparer les deux images en utilisant la différence absolue
                diff = cv2.absdiff(current_image, previous_image)
                
                # Si l'image n'a pas changé, diff sera une image noire (tous les pixels sont égaux)
                if not np.any(diff):  # Si la différence est nulle (images identiques)
                    print(elapsed_time)
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= 30:
                        driver.press_keycode(3)
                        time.sleep(5)
                        driver.get_screenshot_as_file(capture_name)
                        restarded = detect_template_color(capture_name, "image/image_restart")
                        while restarded is False:
                            time.sleep(15)
                            restarded = detect_template_color(capture_name, "image/image_restart")
                        if restarded is True:
                            Method.click_on_trigger(driver, capture_name, "image/image_restart")
                        return False  
                else:
                    start_time = time.time()  # Réinitialiser le temps lorsque l'image change

            # Mettre à jour l'image précédente pour la prochaine itération
            previous_image = current_image

            # Vérification du verrouillage du magasin
            lock = Method.lock_store_verify(capture_name)
            if lock is True:
                driver.back()
                time.sleep(15)

            valide = detect_template_color(capture_name, "./image/image_test_no")
            if valide is False:
                Method.click_on_trigger(driver, capture_name, "image/image_test")

            if valide is True:
                driver.quit()
                return True

            time.sleep(timeout)  # Pause de 2 secondes entre chaque itération

        
            
    def from_map_to_bonus_income_reward(device_name, capture_name, port):
        options.set_capability('udid', device_name)  # ID de l'émulateur ou appareil réel
        options.set_capability('systemPort', uiAutoPort[device_name])
        driver = webdriver.Remote(
                command_executor= port,  # URL du serveur Appium
                options=options  # On passe les options ici au lieu de 'desired_capabilities
        )        
        timeout = 2  # Délai entre chaque appel de fonction
        Method.go_back_to_map_view(driver)
        time.sleep(timeout)
        valide = False
        start_time = time.time()  # Temps initial pour vérifier la durée
        previous_image = None  # Variable pour la capture d'écran précédente
        while valide is False:
            driver.get_screenshot_as_file(capture_name)
            current_image = cv2.imread(capture_name)

            elapsed_time = 0
            if previous_image is not None:
                # Comparer les deux images en utilisant la différence absolue
                diff = cv2.absdiff(current_image, previous_image)
                
                # Si l'image n'a pas changé, diff sera une image noire (tous les pixels sont égaux)
                if not np.any(diff):  # Si la différence est nulle (images identiques)
                    elapsed_time = time.time() - start_time
                    print(elapsed_time)
                    if elapsed_time >= 30:
                        driver.press_keycode(3)
                        time.sleep(2)
                        restarded = detect_template_color(capture_name, "image/image_restart")
                        while restarded is False:
                            time.sleep(15)
                            restarded = detect_template_color(capture_name, "image/image_restart")
                        if restarded is True:
                            Method.click_on_trigger(driver, capture_name, "image/image_restart")
                        return False
                else:
                    start_time = time.time()  # Réinitialiser le temps lorsque l'image change

            # Mettre à jour l'image précédente pour la prochaine itération
            previous_image = current_image
            lock = Method.lock_store_verify(capture_name)
            if lock is True:
                driver.back()
                time.sleep(15)
            stop = detect_template_color(capture_name, "image/img_stop_income")
            if stop is False:
                Method.click_on_trigger(driver, capture_name, "image/image_income")
                Method.click_on_trigger(driver, capture_name, "image/image_test")
            if stop is True:
                time.sleep(5)
                Method.click_on_trigger(driver, capture_name, "image/img_stop_income")
                valide = True
                driver.quit()
                return
            time.sleep(timeout)  # Pause de 2 secondes entre chaque itération