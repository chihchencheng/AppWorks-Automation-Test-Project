import os
from page_objects.create_a_new_product_page import CreateANewProductPage
import pytest
import allure
from dotenv import load_dotenv
import logging
import time

import pymysql
from pymysql.cursors import DictCursor


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from allure_commons.types import AttachmentType


from page_objects.home_page import HomePage
from page_objects.login_page import LoginPage
from page_objects.product_page import ProductPage
from page_objects.cart_page import CartPage
from page_objects.thank_you_page import ThankYouPage
from page_objects.common_page import CommonPage
from page_objects.create_product_page import CreateProductPage



if 'ENV_FILE' in os.environ:
	env_file = os.environ['ENV_FILE']
	load_dotenv(env_file)
else:
	load_dotenv()


@pytest.fixture
def driver():
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	service = Service(executable_path=ChromeDriverManager().install())
	driver = webdriver.Chrome(service=service, options=chrome_options)
	driver.set_window_size(width = 1920, height = 1080)
	driver.maximize_window()
	yield driver
	driver.quit()


@pytest.fixture
def home_page(driver):
	driver.get(os.getenv('HOME_PAGE_URL'))
	return HomePage(driver)


@pytest.fixture
def product_page(driver):
	return ProductPage(driver)


@pytest.fixture
def cart_page(driver):
	return CartPage(driver)


@pytest.fixture
def login_page(driver):
	return LoginPage(driver)


@pytest.fixture
def thank_you_page(driver):
	return ThankYouPage(driver)


@pytest.fixture
def create_product_page(driver):
	return CreateProductPage(driver)

@pytest.fixture
def create_a_new_product_page(driver):
	return CreateANewProductPage(driver)


@pytest.fixture
def common_page(driver):
	return CommonPage(driver)


@pytest.fixture
def login(driver, login_page, worker_id):
	driver.get(f"{os.getenv('HOME_PAGE_URL')}/login.html")
	if worker_id == 'master':
		email = os.getenv('USER1_EMAIL')
	else:
		email = os.getenv(f'{worker_id}_USER_EMAIL')

	password = os.getenv(f'USER_PWD')

	login_page.fill_email(email)
	login_page.fill_password(password)

	logging.info(f'login email: {email}, click login button')
	login_page.click_login_btn()

	yield login_page
