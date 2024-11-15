from scenario import Scenario
import time

def loop_shoop(device_name, capture_name, port):
    Scenario.from_map_to_pub_reward(device_name, capture_name, port)

def loop_incomme(device_name,capture_name, port):
    Scenario.from_map_to_bonus_income_reward(device_name,capture_name, port)

def look_check_stuck(device_name, capture_name,port):
    Scenario.check_device_stuck(device_name,capture_name,port)

def run_every_20_minutes(device_name, capture_name):
    while True:
        loop_shoop(device_name,capture_name)
        # Appelle la fonction
        print("Attente de 19 minutes...")
        time.sleep(1140)  # Attend 20 minutes (en secondes)

def run_every_5_hours(device_name, capture_name):
    while True:
        loop_incomme(device_name,capture_name)
        # Appelle la fonction
        print("Attente de 5 heures...")
        time.sleep(18000)  # Attend 20 minutes (en secondes)