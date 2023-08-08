import os
import logging
import allure

base_url = os.getenv('HOME_PAGE_URL')
login_page_url = f"{base_url}/login.html"
profile_page_url = f"{base_url}/profile.html"

# Scenario: Login and Logout Success
@allure.feature('Login feature')
@allure.story('Login and Logout Success')
def test_login_and_logout_success(login):
	login_page = login

	alert_msg = login_page.get_alert_msg()
	assert alert_msg == 'Login Success',\
	f'expect: Login Success, actual: {alert_msg}'

	jwt_token = login_page.get_jwt_token()
	assert jwt_token is not None, \
		f'cannot find jwt token, jwt token return as {jwt_token}'

	logging.info('click logout')
	with allure.step("Click Logout"):
		login_page.click_logout_btn()
		alert_msg = login_page.get_alert_msg()
		assert alert_msg == 'Logout Success',\
		f'expect: Logout Success, actual: {alert_msg}'


# Scenario: Login Failed with incorrect email or password
@allure.feature('Login feature')
@allure.story('Login fail with invalid credential')
def test_login_fail(driver, login_page):
	driver.get(login_page_url)
	with allure.step("Fill invalid credential"):
		login_page.fill_email('chen@chen.com')
		login_page.fill_password('secret')
		login_page.click_login_btn()

	with allure.step("Show Login"):
		alert_msg = login_page.get_alert_msg()
		assert alert_msg == 'Login Failed',\
			f'expect: Login Failed, actual: {alert_msg}'
		

# Scenario: Login with invalid access token
@allure.feature('Login feature')
@allure.story('Login fail with invalid token')
def test_login_with_invalid_token(driver, login):
	login_page = login
	login_page.get_alert_msg()

	jwt_token = login_page.get_jwt_token()
	logging.info(f'get local storage token: {jwt_token}')

	with allure.step("Click Logout"):
		logging.info('click to logout')
		login_page.click_logout_btn()
		login_page.get_alert_msg()

	with allure.step("Login with previous login jwt token"):
		login_page.set_jwt_token(jwt_token)
		driver.get(profile_page_url)

	alert_msg = login_page.get_alert_msg()
	assert alert_msg == 'Invalid Access Token',\
	f'expect: Invalid Access Token, actual: {alert_msg}'

	

	
	
