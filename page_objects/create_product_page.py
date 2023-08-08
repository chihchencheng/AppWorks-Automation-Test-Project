
import logging
from selenium.webdriver.common.by import By
from utils.base_page import BasePage


class CreateProductPage(BasePage):

    create_product_btn = (By.XPATH, '//button[text()="Create New Product"]')
    product_title = (By.ID, 'product_title')
    category = (By.ID, 'product_category')
    delete_btn = (By.XPATH, '//button[text()="刪除"]')
    

    def open_create_a_product_page(self):
        self.find_clickable_element(self.create_product_btn).click()


    def find_product_title(self):
       product_title_elem = self.find_all_elements(self.product_title)
       return [obj.text for obj in product_title_elem]
        

    def delete_created_product(self, title):
        self.find_clickable_element((By.XPATH, f'//td[text()="{title}"]/parent::tr/td/button[text()="刪除"]')).click()
        logging.info(f'delete product: {title}')
