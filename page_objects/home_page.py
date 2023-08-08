import time
from utils.base_page import BasePage
from selenium.webdriver.common.by import By
import random


class HomePage(BasePage):
	

	def find_all_product_title(self):
		try:
			product_obj = self.find_all_elements((By.CLASS_NAME, 'product__title'))
			product_title =  [obj.text for obj in product_obj]
		except:
			product_title = []
		return product_title
	
	
	def scroll_to_load_all_product(self):
		current_num = 0
		current_product_list = []
		time.sleep(2)
		while True:
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			try:
				self.find_element(
					(By.XPATH, f"//div[@class='products' and count(a) > {current_num}]"),
				)
				current_product_list = self.find_all_elements((By.CLASS_NAME, 'product__title'))
				current_num = len(current_product_list)

			except:
				return current_product_list
			

	def click_to_open_product_page(self):
		title = random.choice(self.testdata)
		self.search_by_keyword(title)
		self.scroll_to_load_all_product()
		self.find_element((By.XPATH, f'//div[text()="{title}"]/parent::a')).click()
