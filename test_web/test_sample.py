import time
import pytest
import allure
import logging
from selenium.webdriver.common.by import By
from page_objects.home_page import HomePage
from allure_commons.types import AttachmentType




@allure.step("Capture Screenshot")
def test_stylish_logo(home_page, common_page):
    stylish_logo = common_page.get_logo()
    assert stylish_logo.is_displayed(), "Logo未顯示"
    logging.info("Find stylish logo")

