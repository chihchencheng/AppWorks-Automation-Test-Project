import pytest
import allure
from pytest_unordered import unordered

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

testdata= ['洋裝','', 'Hello']


def get_db_data_by_keyword(connect_db, keyword):
	with connect_db.cursor() as cursor:
		sql = f"""
		SELECT title FROM product WHERE title LIKE '%{keyword}%';
		"""
		cursor.execute(sql)
		data = cursor.fetchall()
	return [obj['title'] for obj in data]


@pytest.mark.parametrize("keyword", testdata)
def test_search(connect_db, home_page, common_page, keyword):
	data = get_db_data_by_keyword(connect_db, keyword)
	common_page.search_by_keyword(keyword)
	home_page.scroll_to_load_all_product()
	product_titles = home_page.find_all_product_title()
	assert product_titles == unordered(data)


