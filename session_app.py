from appium import webdriver
from appium.options.android import UiAutomator2Options

class Session:
    def check_and_create_session():
        options = UiAutomator2Options()
        options.set_capability('platformName', 'Android')
        options.set_capability('platformVersion', '9')  # Version de ton émulateur Android
        options.set_capability('deviceName', '127.0.0.1:5555')  # ID de l'émulateur ou appareil réel
        options.set_capability('automationName', 'UiAutomator2')
        options.set_capability('noReset', True)
        global driver
        try:
            driver.current_url
            print("La session est déjà ouverte.")
        except Exception as e:
            print("Aucune session ouverte, création d'une nouvelle session...")
        driver = webdriver.Remote(
                command_executor='http://127.0.0.1:4725', 
                options=options 
            )
        print("Nouvelle session ouverte.")
        return driver