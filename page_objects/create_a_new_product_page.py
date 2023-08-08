
import logging
import os
from utils.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.file_detector import LocalFileDetector


class CreateANewProductPage(BasePage):
	file_path = 'test_data/stylish_product_image'
    
	category_option = (By.XPATH, '//select[@name="category"]')
	title_text_field = (By.XPATH, '//input[@name="title"]')
	description_textarea = (By.XPATH, '//textarea[@name="description"]')
	price_field = (By.XPATH, '//input[@name="price"]')
	texture_field = (By.XPATH, '//input[@name="texture"]')
	wash_field = (By.XPATH, '//input[@name="wash"]')
	place_of_production_field = (By.XPATH, '//input[@name="place"]')
	note_field = (By.XPATH, '//input[@name="note"]')
	story_field = (By.XPATH, '//input[@name="story"]')

	main_img = (By.XPATH, '//input[@name="main_image"]')
	other_img_0 = (By.XPATH, '//input[@name="other_images"][1]')
	other_img_1 = (By.XPATH, '//input[@name="other_images"][2]')

	create_btn = (By.XPATH, '//input[@value="Create"]')
	
	
	def select_category(self, category):
		category_elem = self.find_element(self.category_option)
		dropdown = Select(category_elem)
		dropdown.select_by_visible_text(category)


	def fill_in_product_info(self, data):
		self.select_category(data['category'])
		self.find_element(self.title_text_field).send_keys(data['title'])
		self.find_element(self.description_textarea).send_keys(data['description'])
		self.find_element(self.price_field).send_keys(data['price'])
		self.find_element(self.texture_field).send_keys(data['texture'])
		self.find_element(self.wash_field).send_keys(data['wash'])
		self.find_element(self.place_of_production_field).send_keys(data['place_of_product'])
		self.find_element(self.note_field).send_keys(data['note'])
		self.select_check_box_by_value('colors', data['colors'])
		self.select_check_box_by_value('sizes', data['sizes'])
		self.find_element(self.story_field).send_keys(data['story'])
		self.upload_image(data['main_image'])
		self.upload_image(data['other_image_1'])
		self.upload_image(data['other_image_2'])



	def select_check_box_by_value(self, type, value):
		logging.info(f'select check box value: {value}')
		if type == 'colors' and value == ['全選']:
			value = ['白色', '亮綠', '淺灰', '淺棕', '淺藍', '深藍', '粉紅']
		elif type == 'sizes' and value == ['全選']:
			value = ['S','M','L','XL','F']
		if type =='colors' and value == [""]:
			return
		else:
			for i in value:
				self.find_element((By.XPATH, f'//span/label[contains(text(),"{i}")]/parent::span/input')).click()


	def upload_image(self, file_path):
		logging.info(f'file upload path {file_path}')
		try:
			if 'main' in file_path:
				logging.info('upload main image')
				self.find_clickable_element(self.main_img).send_keys(file_path)
			elif 'Image0' in file_path: 
				logging.info('upload image 0')
				self.find_clickable_element(self.other_img_0).send_keys(file_path)
			elif 'Image1' in file_path: 
				logging.info('upload image 1')
				self.find_clickable_element(self.other_img_1).send_keys(file_path)
		except:
				logging.info('Cannot upload file')
				return

	def click_create_btn(self):
		self.find_clickable_element(self.create_btn).click()
