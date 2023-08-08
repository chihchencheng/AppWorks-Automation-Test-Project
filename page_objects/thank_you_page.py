
import logging
from utils.base_page import BasePage
from selenium.webdriver.common.by import By


class ThankYouPage(BasePage):
	
	thankyou_title = (By.CLASS_NAME, 'thankyou__title')
	product_title = (By.CLASS_NAME, 'cart__item-name')
	product_qty = (By.XPATH, '//div[@class="cart__item-quantity"]/div[2]')
	product_unit_price = (By.CLASS_NAME, 'cart__item-price-content')
	product_subtotal = (By.CLASS_NAME, 'cart__item-subtotal-content')
	subtotal_value = (By.XPATH, '//div[@class="total"]/div[@class="total__amount"]')
	total_paid_value = (By.XPATH, '//div[@class="payable"]/div[@class="total__amount"]')
	order_number = (By.XPATH, '//*[contains(text(), "請記住訂單編號") ]')

	receiver = (By.XPATH, '//div[text()="收件人: "]/parent::div/div[@class="form__field-value"]')
	email = (By.XPATH, '//div[text()="Email: "]/parent::div/div[@class="form__field-value"]')
	phone_number = (By.XPATH, '//div[text()="手機: "]/parent::div/div[@class="form__field-value"]')
	address = (By.XPATH, '//div[text()="地址: "]/parent::div/div[@class="form__field-value"]')
	deliver_time = (By.XPATH, '//div[text()="配送時間: "]/parent::div/div[@class="form__field-value"]')


	def get_receiver_info(self):
		receiver = self.find_element(self.receiver).text
		email = self.find_element(self.email).text
		phone_number = self.find_element(self.phone_number).text
		address = self.find_element(self.address).text
		deliver_time = self.find_element(self.deliver_time).text.replace(" ", "")
		return {
			'receiver': receiver,
			'email': email,
			'mobile': phone_number,
			'address': address,
			'deliver_time': deliver_time
		}


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
		logging.info('Get all product title in thank you page')
		product_obj = self.find_all_elements(self.product_title)
		return [obj.text for obj in product_obj]


	def get_all_product_price(self):
		product_price_obj = self.find_all_elements(self.product_unit_price) 
		return [obj.text.split(".")[1] for obj in product_price_obj]


	def get_all_product_qty(self):
		qty_obj = self.find_all_elements(self.product_qty)
		return [obj.text for obj in qty_obj ]


	def get_subtotal(self):
		return self.find_element(self.subtotal_value).text


	def get_product_unit_price(self):
		return self.find_element(self.product_unit_price).text.split(".")[1]
	

	def get_product_subtotal(self):
		return self.find_element(self.product_subtotal).text.split(".")[1]
	
	
	def get_order_number(self):
		return self.find_element(self.order_number).text
	

		

        