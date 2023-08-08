import os
import logging
import requests
import allure
from api_objects.login_api import LoginApi
from api_objects.logout_api import LogOutApi
from api_objects.profile_api import ProfileApi
import pytest
from jsonschema import validate


from test_data.get_data_from_excel import get_api_data

base_url = os.getenv('HOME_PAGE_URL')

email = f"{os.getenv('USER1_EMAIL')}"

fail_test_data =  get_api_data('API login Failed')


def get_db_data(connect_db, keyword):
	with connect_db.cursor() as cursor:
		sql = f"""
			SELECT * FROM user WHERE email='{keyword}';
		"""
		cursor.execute(sql)
		data = cursor.fetchall()
		user = {
			'id': data[0]['id'],
			'provider': data[0]['provider'],
			'name': data[0]['name'],
			'email': data[0]['email'],
			'picture': data[0]['picture']
		}

		return user


# Scenario: Login and Logout Success
@allure.feature('Login feature')
@allure.story('Login and Logout Success')
def test_login_and_logout_success(connect_db, session, login):
	logout_api = LogOutApi(session)
	db_data = get_db_data(connect_db, email)
	logging.info(f'get data from db: {db_data}')

	with allure.step('send POST request to login end point'):
		response = login['response']
		logging.info(f'response: {response.json()}')

		response_user = response.json()['data']['user']
		logging.info(f'get response user: {response_user}')
		assert response.status_code == 200
		assert response_user == db_data

	with allure.step('send the POST request to logout'):	
		logout_response = logout_api.user_logout()

	logging.info(logout_response.json())
	assert logout_response.status_code == 200
	assert logout_response.json()['message'] == 'Logout Success'
	

# Scenario: Fail to login
@allure.feature('Login feature')
@allure.story('Fail to Login')
@pytest.mark.parametrize('data', fail_test_data)
def test_fail_login(session, login_api, data):
	logging.info(f'test data: {data}')
	payload = {
		"provider": data['provider'],
		"email": data['email'],
		"password": data['password']
		}
	
	with allure.step('post request to test invalid login credential'):
		response = login_api.user_login(data['provider'], data['email'], data['password'])

	status_code = response['response'].status_code
	errorMsg = response['response'].json()['errorMsg']

	with allure.step('assert status code and errorMsg'):
		assert status_code == int(data['status_code'])
		assert errorMsg == data['errorMsg']


# Scenario: get user profile successfully
def test_get_user_profile_successfully(connect_db, session, login):
	profile_api = ProfileApi(session)
	logging.info(f'test get user profile successfully')
	db_data = get_db_data(connect_db, email)
	logging.info(f'db data: {db_data}')

	with allure.step('get user profile'):
		profile_response = profile_api.get_user_profile()
		json_data = profile_response.json()['data']

	with allure.step('assert response body with db'):
		assert profile_response.status_code == 200
		assert json_data['provider'] == db_data['provider']
		assert json_data['name'] == db_data['name']
		assert json_data['email'] == db_data['email']
		assert json_data['picture'] == db_data['picture']


# Scenario: Get profile with invalid bearer token
@allure.feature('Get profile feature')
@allure.story('Get profile with invalid bearer token')
def test_fail_get_profile_with_invalid_token(session, login):
	logout_api = LogOutApi(session)
	profile_api = ProfileApi(session)

	with allure.step('login and get bearer token'):
		login_response = login
		bearer_token = login_response['response'].json()['data']['access_token']

	with allure.step('logout and get profile with invalid token'):
		logout_api.user_logout()
		profile_response = profile_api.get_user_profile_with_token(bearer_token)
		errorMsg = profile_response.json()['errorMsg']

	logging.info(f'expect token: Invalid Access Token, actual: {errorMsg} ')
	assert errorMsg == 'Invalid Access Token'
	
