from img_detector import find_pass_center
import time


class Method:
   def click_boutique_from_map_screen(driver):
      driver.tap([(106, 1400)])
      
   def swipe_pub(driver):
      driver.swipe(216, 830, 200, 100, 2000) 

   def click_pub(driver):
      driver.tap([(456, 1136)])

   def first_screen_pass(driver):
      driver.tap([(866, 35)])

   def clean_reward_screen(driver):
      driver.tap([(307, 1281)])
   
   def click_bonus_incom(driver):
      driver.tap([(789, 123)])
   
   def go_to_income_bonus_pub(driver):
      driver.tap([(473, 1428)])
   
   def pass_pub_income(driver):
      driver.tap([(816, 82)])
      
   def go_back_to_map_view(driver):
      driver.tap([(276, 888)])
      
   """ def handle_click(driver, capture_name):
      screen_maker(capture_name)
      center = find_pass_center("image/image_test", capture_name)
      coord = center[0]
      driver.tap([(coord[0] + 50, coord[1] - 50)])"""
   
   def click_on_trigger(driver, capture_name, folder_path):
      #screen_maker(capture_name)
      driver.get_screenshot_as_file(capture_name)
      center = find_pass_center(folder_path, capture_name)
      if center is not None and len(center) > 0:
         coord = center[0]
         driver.tap([(coord[0], coord[1])])
         print("Clic effectué avec coord :", coord, "et center :", center)
      else:
         return
   
   def lock_store_verify(capture_name):
      center = find_pass_center("image/recovery/img_lock", capture_name)
      if center is None or len(center) == 0:
         return False
      else:
         return True
   
   def crash_verify(capture_name):
      print("je sais pas frère !")
   
   
   def am_I_struggle(i):
      while i < 5:
         i + 1
         if i == 5:
            return True
         else:
            return i