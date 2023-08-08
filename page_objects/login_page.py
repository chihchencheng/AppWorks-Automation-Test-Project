import logging
import os
from dotenv import load_dotenv
from utils.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
	create_product_url = f"{os.getenv('HOME_PAGE_URL')}/admin/products.html"
    
	email = (By.ID, 'email')
	password = (By.ID, 'pw')
	login_btn = (By.CLASS_NAME, 'login100-form-btn')
	logout_btn = (By.XPATH, '//button[text()="登出"]')


	def fill_email(self, email):
		self.find_element(self.email).send_keys(email)


	def fill_password(self, password):
		self.find_element(self.password).send_keys(password)


	def click_login_btn(self):
		self.find_clickable_element(self.login_btn).click()


	def click_logout_btn(self):
		self.find_clickable_element(self.logout_btn).click()

	def go_to_create_product_page(self):
		self.driver.get(self.create_product_url)
