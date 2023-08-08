import random
import random
from utils.base_page import BasePage
from selenium.webdriver.common.by import By


class ProductPage(BasePage):

    product_name = (By.CLASS_NAME, 'product__title')
    product_price = (By.CLASS_NAME, 'product__price')
    quantity_value = (By.CLASS_NAME, 'product__quantity-value')

    quantity_editor = (By.CLASS_NAME,'product__quantity-title')
    quantity_add = (By.CLASS_NAME,'product__quantity-add')
    quantity_minus = (By.CLASS_NAME,'product__quantity-minus')
    
    add_to_cart_btn = (By.CLASS_NAME, 'product__add-to-cart-button')
    in_cart_item_number = (By.CLASS_NAME,'header__link-icon-cart-number')
    color_options = (By.XPATH, "//div[@data_id]")
    size_options = (By.XPATH, '//div[@class="product__size"]')
    cart = (By.CLASS_NAME, 'header__link-icon-cart')

    cart_icon = (By.CLASS_NAME, 'header__link-icon-cart')
    

    def find_all_color_option(self):
        color_obj = self.find_all_elements((By.XPATH, "//div[@data_id]"))
        print(color_obj)
        colors = [obj.get_attribute('data_id') for obj in color_obj]
        return colors
        

    def select_color(self, color_id):
        self.find_element((By.XPATH, f'//div[@data_id="{color_id}"]')).click()


    def get_selected_color(self):
        obj = self.find_element((By.XPATH,f'//div[@class="product__color product__color--selected"]'))
        return obj.get_attribute('data_id')
    

    def select_size(self, size):
        self.find_element((By.XPATH, f'//div[text()="{size}"]')).click()


    def find_all_size_option(self):
        size_obj = self.find_all_elements((By.XPATH, '//div[@class="product__size"]'))
        size_options = [obj.text for obj in size_obj]
        return size_options
    

    def get_selected_size(self):
        obj = self.find_element((By.XPATH,f'//div[@class="product__size product__size--selected"]'))
        return obj.text
    

    def increase_product_qty(self):
        self.find_element(self.quantity_add).click()


    def decrease_product_qty(self):
        self.find_element(self.quantity_minus).click()


    def get_qty_value(self):
        return self.find_element(self.quantity_value).text
    

    def click_add_to_cart(self):
        self.find_element(self.add_to_cart_btn).click()


    def get_in_cart_item_number(self):
        return self.find_element(self.in_cart_item_number).text
    

    def click_to_view_cart_item(self):
        self.find_element(self.cart).click()


    def get_product_detail(self):
        product_name = self.find_element(self.product_name).text
        product_price = (self.find_element(self.product_price).text).split(".")[1]
        product_qty = self.get_qty_value()
        return {'product':product_name , 
                'product_price':product_price,
                'product_qty': product_qty}
    
    
    def select_random_size(self):
        size_options = self.find_all_size_option()
        size = random.choice(size_options)
        self.select_size(size)
    

    def go_to_checkout_page(self):
        self.find_clickable_element(self.cart_icon, 10).click()


    def add_product_to_cart(self):
        self.select_random_size()
        self.find_clickable_element(self.add_to_cart_btn).click()
    
