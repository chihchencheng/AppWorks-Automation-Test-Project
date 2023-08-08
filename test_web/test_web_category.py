import pytest
import allure

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
import logging

from page_objects.home_page import HomePage



testdata = [
	("女裝",['前開衩扭結洋裝','透肌澎澎防曬襯衫','小扇紋細織上衣','活力花紋長筒牛仔褲','精緻扭結洋裝','透肌澎澎薄紗襯衫','小扇紋質感上衣','經典修身長筒牛仔褲']),
	("男裝",['純色輕薄百搭襯衫','時尚輕鬆休閒西裝','經典商務西裝']),
	("配件",['夏日海灘戶外遮陽帽','經典牛仔帽','卡哇伊多功能隨身包','柔軟氣質羊毛圍巾'])
]


@pytest.mark.parametrize("category, expected_product", testdata)  
def test_products(home_page, common_page, category, expected_product):
	logging.info('Go to Stylish website')
	
	common_page.click_category_link(category)
	common_page.find_element((By.XPATH, '//div[@class="carousel__campaign-story-content"]'))

	home_page.scroll_to_load_all_product()
	product_title = home_page.find_all_product_title()
	assert product_title == expected_product






