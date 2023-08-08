import logging
import random
import time
from utils.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class CommonPage(BasePage):
	testdata = ['前開衩扭結洋裝', '透肌澎澎防曬襯衫', '小扇紋細織上衣', '活力花紋長筒牛仔褲', 
	    		'純色輕薄百搭襯衫', '時尚輕鬆休閒西裝', '經典商務西裝', '夏日海灘戶外遮陽帽', 
				'經典牛仔帽', '卡哇伊多功能隨身包', '柔軟氣質羊毛圍巾', '精緻扭結洋裝', 
				'透肌澎澎薄紗襯衫', '小扇紋質感上衣', '經典修身長筒牛仔褲']
    
	logo = (By.CLASS_NAME, 'header__logo')
	cart = (By.CLASS_NAME, 'header__link-icon-cart')
	member_icon = (By.XPATH, '//div[@class="header__link-icon-profile"]')
	copyright_footer = (By.XPATH, '//div[contains(text(),"All rights reserved.")]')


	def click_to_view_cart_item(self):
		self.find_element(self.cart).click()


	def click_member_button(self):
		self.find_clickable_element(self.member_icon).click()


	def click_category_link(self, category):
		logging.info(f'Click {category} link')
		category_elem = self.find_clickable_element((By.LINK_TEXT, category))
		category_elem.click()


	def search_by_keyword(self, keyword):
		self.find_element((By.CLASS_NAME,'header__search-input')).send_keys(keyword + Keys.ENTER)


	def open_a_random_product_page(self):
		logging.info('open a random product page')
		title = random.choice(self.testdata)
		self.search_by_keyword(title)
		self.driver.execute_script("window.scrollTo(0, 900);")
		self.find_element((By.XPATH, f'//div[text()="{title}"]/parent::a')).click()


	def get_logo(self):
		return self.find_element(self.logo)


	
