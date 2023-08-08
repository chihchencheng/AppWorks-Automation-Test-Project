import logging
import random
from utils.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class CartPage(BasePage):

	cart_delete_btn = (By.CLASS_NAME, 'cart__delete-button')
	product_qty = (By.CLASS_NAME, 'cart__item-quantity-selector')
	product_title = (By.CLASS_NAME, 'cart__item-name')
	delete_btn = (By.CLASS_NAME,'cart__delete-button')
	in_cart_item_number = (By.CLASS_NAME,'header__link-icon-cart-number')
	subtotal_value = (By.CLASS_NAME, 'cart__item-subtotal-content')
	product_unit_price = (By.CLASS_NAME, 'cart__item-price-content')
	checkout_btn = (By.CLASS_NAME, 'checkout-button')

	# order customer information
	receiver_name = (By.XPATH, '//div[text()="收件人姓名"]/parent::div/input')
	receiver_email = (By.XPATH, '//div[text()="Email"]/parent::div/input')
	receiver_phone_number = (By.XPATH, '//div[text()="手機"]/parent::div/input')
	receiver_address = (By.XPATH, '//div[text()="地址"]/parent::div/input')
	available_deliver_time = (By.CLASS_NAME,'form__field-radios')

	# card information
	payment_section = (By.XPATH, '//div[text()="付款資料"]')
	card_number = (By.ID, 'cc-number')
	card_expire_date = (By.ID, 'cc-exp')
	card_cvv = (By.ID, 'cc-ccv')

	# iframe
	card_iframe = (By.XPATH, '//div[@id="card-number"]/iframe')
	expiration_date_iframe = (By.XPATH, '//div[@id="card-expiration-date"]/iframe')
	card_ccv_iframe = (By.XPATH, '//div[@id="card-ccv"]/iframe')


	def get_all_item_in_cart(self):
		product_title = self.get_all_product_title()
		product_qty = self.get_all_product_qty()
		product_price = self.get_all_product_price()

		product_list = []
		for i in range(len(product_title)):
			product_list.append(
				{'product':product_title[i],
				 'product_price':product_price[i],
				 'product_qty':product_qty[i]}
			)
		return product_list


	def get_all_product_title(self):
		logging.info('Get all product title')
		product_obj = self.find_all_elements(self.product_title)
		return [obj.text for obj in product_obj]


	def get_all_product_price(self):
		product_price_obj = self.find_all_elements((By.CLASS_NAME, 'cart__item-price-content')) 
		return [obj.text.split(".")[1] for obj in product_price_obj]


	def get_all_product_qty(self):
		qty_obj = self.find_all_elements(self.product_qty)
		qty = []
		for i in qty_obj:
			select = Select(i)
			qty.append(select.first_selected_option.text)
		return qty


	def get_subtotal(self):
		return self.find_element(self.subtotal_value).text.split(".")[1]


	def get_product_unit_price(self):
		return self.find_element(self.product_unit_price).text.split(".")[1]


	def get_product_quantity(self):
		qty_obj = self.find_element(self.product_qty)
		select = Select(qty_obj)
		return select.first_selected_option.text


	def delete_one_product_in_cart(self, product_title ):
		logging.info('刪除購物車商品') 
		del_btn = self.find_clickable_element((By.XPATH,
			f'//div[text()="{product_title}"]/ancestor::div/child::div[@class="cart__delete-button"]'))
		del_btn.click()


	def update_product_quantity(self, qty):
		qty_obj = self.find_element(self.product_qty)
		select = Select(qty_obj)
		select.select_by_visible_text(qty)


	def get_in_cart_item_number(self):
		return self.find_element(self.in_cart_item_number).text
	
	
	def fill_receiver_info(self, name, email, phone, address):
		logging.info(f'Fill in receiver info: {name}, {email}, {phone}, {address}')
		self.find_element(self.receiver_name).send_keys(name)
		self.find_element(self.receiver_email).send_keys(email)
		self.find_element(self.receiver_phone_number).send_keys(phone)
		self.find_element(self.receiver_address).send_keys(address)
	

	def select_deliver_time(self, time):
		logging.info(f'Select deliver time: {time}')

		if time != '':
			self.find_element((By.XPATH, f'//label[text()="{time}"]')).click()


	def fill_card_detail(self,card_number, expire_date, cvv ):
		self.fill_card_number(card_number)
		self.fill_expire_date(expire_date)
		self.fill_cvv(cvv)


	def fill_card_number(self, card_number):
		self.switch_to_iframe(self.card_iframe)
		self.find_clickable_element(self.card_number, 15).send_keys(card_number)
		self.driver.switch_to.parent_frame()


	def fill_expire_date(self, expire_date):
		self.switch_to_iframe(self.expiration_date_iframe)
		self.find_clickable_element(self.card_expire_date, 15).send_keys(expire_date)
		self.driver.switch_to.parent_frame()


	def fill_cvv(self, cvv):
		self.switch_to_iframe(self.card_ccv_iframe)
		self.find_clickable_element(self.card_cvv, 15).send_keys(cvv)
		self.driver.switch_to.parent_frame()


	def click_confirm_checkout(self):
		self.find_clickable_element(self.checkout_btn).click()
	