from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException

import logging


class BasePage:

	def __init__(self, driver):
		self.driver = driver
    
	def find_all_elements(self, locator, waiting_time=10):
		elem = WebDriverWait(self.driver, waiting_time).until(
		EC.presence_of_all_elements_located(locator)
		)
		return elem

	def find_element(self, locator, waiting_time=10):
		elem = WebDriverWait(self.driver, waiting_time).until(
		EC.presence_of_element_located(locator)
		)
		return elem

	def find_clickable_element(self, locator, waiting_time=10):
		elem = WebDriverWait(self.driver, waiting_time).until(
			EC.element_to_be_clickable(locator)
		)
		return elem
	
	def scroll_down(self):
		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	def scroll_to_element(self, locator):
		element = self.find_element(locator)
		self.driver.execute_script("arguments[0].scrollIntoView();", element)

	def alert(self):
		try:
			alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present(),
			'Timed out waiting for PA creation ' +
			'confirmation popup to appear.')
			return alert
		except TimeoutException:
			print("no alert")

	def get_alert_msg(self):
		alert_obj = self.alert()
		if alert_obj is not None:
			alert_msg = alert_obj.text
		alert_obj.accept()
		return alert_msg
	
	def get_jwt_token(self):
		return self.driver.execute_script(f"return window.localStorage.getItem('jwtToken');")
	
	def set_jwt_token(self, jwt_token_value):
		self.driver.execute_script(f"window.localStorage.setItem('jwtToken', '{jwt_token_value}');")
	
	def switch_to_iframe(self, locator, waiting_time=10):
		elem = WebDriverWait(self.driver, waiting_time).until(
			EC.frame_to_be_available_and_switch_to_it(locator)
			)
		
	