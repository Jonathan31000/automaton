import time
import threading

class Timer:
    def print_timer(timer):
        for i in range (timer):
            time.sleep(1)
            print(timer + 1)
    
    def start_timer(timer):
        thread = threading.Thread(target=print_timer(timer))