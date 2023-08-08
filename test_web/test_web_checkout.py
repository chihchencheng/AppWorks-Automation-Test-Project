import allure
import pytest
import logging
from test_data.get_data_from_excel import get_test_data_from_file
from selenium.webdriver.common.by import By


# Scenario: Checkout with empty cart
@allure.feature('Checkout Feature')
@allure.story('Test Checkout with empty cart')
def test_checkout_with_empty_cart(login, login_page, common_page, cart_page):

    login_page  = login
    alert_msg = login_page.get_alert_msg()
    logging.info(f'login in alert_msg: {alert_msg}')
 

    logging.info('Go to Checkout page')
    with allure.step('Go to Checkout page'):
        common_page.click_to_view_cart_item()

    logging.info('Click 確認付款')
    with allure.step('Click 確認付款'):
        cart_page.click_confirm_checkout()

    alert_msg = cart_page.get_alert_msg()

    logging.info(f'alert message: {alert_msg}')
    with allure.step('Assert 尚未選購商品 alert message'):
        assert alert_msg == '尚未選購商品', \
            f'expect: 尚未選購商品, actual: {alert_msg}'


invalid_test_data = get_test_data_from_file('Checkout with Invalid Value')
# Scenario: Checkout with invalid values (17 Test Cases)
@allure.feature('Checkout Feature')
@allure.story('Test Checkout with invalid value')
@pytest.mark.parametrize('data', invalid_test_data)
def test_checkout_with_invalid_value(login, common_page, product_page, cart_page, data): 

    with allure.step('Login with invalid credential'):
        login_page  = login
        alert_msg = login_page.get_alert_msg()
        assert alert_msg == 'Login Success',\
        f'expect: Login Success, actual: {alert_msg}'

    with allure.step('Add a product to shopping Cart'):
        common_page.open_a_random_product_page()
        product_page.add_product_to_cart()
        alert_msg = product_page.get_alert_msg()
        assert alert_msg == '已加入購物車',\
            f'expect: 已加入購物車, actual: {alert_msg}'
    
    with allure.step('Fill in receiver info'):
        product_page.go_to_checkout_page()
        cart_page.fill_receiver_info(data['receiver'], data['email'], data['mobile'], data['address'])
        cart_page.select_deliver_time(data['deliver_time'])

    with allure.step('Fill in card detail'):
        cart_page.fill_card_detail(data['credit_card_no'], data['expiry_date'], data['security_code'])

    with allure.step('Click 確認付款'):
        cart_page.click_confirm_checkout()

    actual_alert_msg = cart_page.get_alert_msg()
    expect_alert_msg = data["alert_msg"]
    assert actual_alert_msg == expect_alert_msg, \
        f'expect: {expect_alert_msg}, actual: {actual_alert_msg}'


valid_test_data = get_test_data_from_file('Checkout with Valid Value')
# Scenario: Checkout with valid values (3 Test Cases)
@allure.feature('Checkout Feature')
@allure.story('Test Checkout with valid value')
@pytest.mark.parametrize('data',valid_test_data)
def test_checkout_with_valid_values(login, common_page, product_page, cart_page, thank_you_page, data):
    with allure.step('Login with valid credential'):
        logged_in_page = login
        alert_msg =  logged_in_page.get_alert_msg()
        assert alert_msg == 'Login Success',\
        f'expect: Login Success, actual: {alert_msg}'

    with allure.step('Add a product to shopping Cart'):
        common_page.open_a_random_product_page()
        product_page.add_product_to_cart()
        alert_msg = product_page.get_alert_msg()
        assert alert_msg == '已加入購物車',\
        f'expect: 已加入購物車, actual: {alert_msg}'

    with allure.step('Go to cart page'):
        product_page.go_to_checkout_page()
        product_to_checkout = cart_page.get_all_item_in_cart()
        logging.info(f'checkout product: {product_to_checkout}')

    with allure.step('Fill receiver detail and deliver time'):
        cart_page.fill_receiver_info(data['receiver'], data['email'], data['mobile'], data['address'])
        cart_page.select_deliver_time(data['deliver_time'])
        
    with allure.step('Fill card detail'):
        cart_page.scroll_to_element((By.XPATH, '//div[text()="付款資料"]'))
        cart_page.fill_card_detail(data["credit_card_no"], data["expiry_date"], data["security_code"])

    with allure.step('Proceed to checkout'):
        cart_page.click_confirm_checkout()
    
    paid_alert_msg = cart_page.get_alert_msg()
    assert paid_alert_msg == '付款成功', \
        f'expect: 付款成功, actual: {paid_alert_msg}'
    
    items = thank_you_page.get_all_item_in_cart()
    receiver_info = thank_you_page.get_receiver_info()  
    assert  product_to_checkout == items
    logging.info(f"""expect item: {product_to_checkout},
                 actual item: {items}""")
    expect_receiver = {'receiver': data['receiver'], 
                       'email': data['email'], 
                       'mobile': data['mobile'],
                       'address': data['address'], 
                       'deliver_time': data['deliver_time']}
    assert receiver_info == expect_receiver
    logging.info(f"""expect receiver info: {expect_receiver},
                    actual: thank you page {receiver_info}""")

    

