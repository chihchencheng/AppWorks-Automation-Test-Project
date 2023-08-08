import logging
import os
import time
import allure
import pytest
from test_data.get_data_from_excel import get_test_data_from_file

success_product_data = get_test_data_from_file('Create Product Success')
# Scenario: Create Product Success (3 Test Cases) 
@allure.feature('Create Product Feature')
@allure.story('Test Create Product with valid data')
@pytest.mark.parametrize('data', success_product_data)
def test_create_product_success(driver,login, create_product_page, create_a_new_product_page, data):
    logging.info(data)

    login_page = login
    login_page.get_alert_msg()
    login_page.go_to_create_product_page()
    create_product_page.open_create_a_product_page()

    driver.switch_to.window(driver.window_handles[-1])
    try:
        create_a_new_product_page.fill_in_product_info(data)
        create_a_new_product_page.click_create_btn()
        created_success_msg = create_a_new_product_page.get_alert_msg()
        logging.info(f'alert msg: {created_success_msg}')
        assert created_success_msg == 'Create Product Success'

        driver.switch_to.window(driver.window_handles[0])
        driver.refresh()

        product_title_list = create_product_page.find_product_title()
        assert data['title'] in product_title_list, \
            f'create product title: {data["title"]}, product_title_list: {product_title_list}'
    except Exception as e:
        logging.error(f'Unable to create product {data["title"]}: {str(e)}')
        raise e
    finally:
        create_product_page.delete_created_product(data['title'])
    

invalid_product_data = get_test_data_from_file('Create Product Failed')
# Scenario: Create Product with Invalid Value (20 Test Cases)
@pytest.mark.flaky(reruns=1, reruns_delay=2)
@allure.feature('Create Product Feature')
@allure.story('Test Create Product with invalid data')
@pytest.mark.parametrize('data', invalid_product_data)
def test_create_product_with_invalid_value(driver,login, create_product_page, create_a_new_product_page, data):
    logging.info(f'create product with invalid data: {data}')

    login_page = login
    login_page.get_alert_msg()
    login_page.go_to_create_product_page()
    create_product_page.open_create_a_product_page()

    driver.switch_to.window(driver.window_handles[-1])

    create_a_new_product_page.fill_in_product_info(data)

    try:
        create_a_new_product_page.click_create_btn()
        actual_msg = create_a_new_product_page.get_alert_msg()

        if actual_msg == 'Create Product Success':
            driver.switch_to.window(driver.window_handles[0])
            driver.refresh()
            product = create_product_page.find_product_title()
            create_product_page.delete_created_product(product)
            assert actual_msg == data['alert_msg'], \
            f'expect: {data["alert_msg"]}, actual msg: {actual_msg}'
            logging.info(f'expect: {data["alert_msg"]}, actual msg: {actual_msg}')
    except Exception as e:
        logging.error(f'Unable to create product {data["title"]}: {str(e)}')  
        raise e
    finally:
        create_product_page.delete_created_product(data['title'])



# Scenario: Create Product without login
@allure.feature('Create Product Feature')
@allure.story('Test Create Product without login')
def test_create_product_without_login(driver, create_product_page, create_a_new_product_page):
    data = {
        'category': 'Women',
        'title': '連身裙', 
        'description': '詳細內容', 
        'price': '100', 
        'texture': '棉質', 
        'wash': '手洗', 
        'place_of_product': 'Taiwan', 
        'note': 'Notes', 
        'colors': ['白色'], 
        'sizes': ['F'], 
        'story': 'Story Content', 
        'main_image': 'os.path.abspath("test_data/otherImage0.jpg")', 
        'other_image_1': '/Users/chihchencheng/development/Automation-Test-Program-Batch2-Project/test_data/otherImage0.jpg', 
        'other_image_2': '/Users/chihchencheng/development/Automation-Test-Program-Batch2-Project/test_data/otherImage1.jpg'
    }
    driver.get(f'{os.getenv("HOME_PAGE_URL")}/admin/products.html')
    create_product_page.get_alert_msg()
    create_product_page.open_create_a_product_page()

    window_handles = create_product_page.driver.window_handles
    create_product_page.driver.switch_to.window( window_handles[-1])

    create_a_new_product_page.fill_in_product_info(data)
    create_a_new_product_page.click_create_btn()
    alert_msg = create_a_new_product_page.get_alert_msg()
    assert alert_msg == 'Please Login First', \
        f'expect: Please Login First, actual: {alert_msg}'
