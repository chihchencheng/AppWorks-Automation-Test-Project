import json
import logging
import allure
from api_objects.get_order_api import GetOrderApi
from api_objects.logout_api import LogOutApi
import pytest
from api_objects.checkout_api import CheckoutApi
from test_data.get_data_from_excel import get_api_data


def get_db_data(connect_db, keyword):
	with connect_db.cursor() as cursor:
		sql = f"""
			SELECT 
			JSON_UNQUOTE(JSON_EXTRACT(details, '$.list[0].id')) AS id,
			JSON_UNQUOTE(JSON_EXTRACT(details, '$.list[0].qty')) AS qty,
			JSON_UNQUOTE(JSON_EXTRACT(details, '$.list[0].name')) AS name,
			JSON_UNQUOTE(JSON_EXTRACT(details, '$.list[0].size')) AS size,
			JSON_UNQUOTE(JSON_EXTRACT(details, '$.list[0].color')) AS color,
			JSON_UNQUOTE(JSON_EXTRACT(details, '$.list[0].image')) AS image,
			JSON_UNQUOTE(JSON_EXTRACT(details, '$.list[0].price')) AS price,
			JSON_UNQUOTE(JSON_EXTRACT(details, '$.total')) AS total,
			JSON_UNQUOTE(JSON_EXTRACT(details, '$.subtotal')) AS subtotal,
			JSON_UNQUOTE(JSON_EXTRACT(details, '$.recipient.name')) AS receiver,
			JSON_UNQUOTE(JSON_EXTRACT(details, '$.recipient.time')) AS deliver_time,
			JSON_UNQUOTE(JSON_EXTRACT(details, '$.recipient.email')) AS email,
			JSON_UNQUOTE(JSON_EXTRACT(details, '$.recipient.phone')) AS mobile,
			JSON_UNQUOTE(JSON_EXTRACT(details, '$.recipient.address')) AS address
			FROM stylish_backend.order_table ot 
			WHERE ot.number = '{keyword}';
		"""
		cursor.execute(sql)
		data = cursor.fetchall()

		order = {
			'qty': int(data[0]['qty']),
			'name': data[0]['name'],
			'size': data[0]['size'],
			'color': data[0]['color'],
			'image': data[0]['image'],
			'price': int(data[0]['price']),
			'total': int(data[0]['total']),
			'subtotal': int(data[0]['subtotal']),
			'receiver': data[0]['receiver'], 
			'email': data[0]['email'],
			'mobile': data[0]['mobile'],
			'address': data[0]['address'],
			'deliver_time': data[0]['deliver_time']
		}
		return order


valid_receiver = get_api_data('API Checkout with Valid Value')
@allure.feature('Checkout API')
@allure.story('Checkout successfully')
@pytest.mark.parametrize('data', valid_receiver)
def test_checkout_successfully(session, login, connect_db, data):
	checkout_api = CheckoutApi(session)
	checkout_api.get_prime()

	with allure.step('Proceed to checkout'):
		response = checkout_api.checkout(receiver = data)

	with allure.step('assert response and order number digits'):
		assert response.status_code == 200
		order_id = response.json()["data"]["number"]
		db_data = get_db_data(connect_db, order_id)
		checkout_info = checkout_api.get_payload_info()

		assert data['receiver'] == db_data['receiver']
		assert data['email'] == db_data['email']
		assert data['mobile'] == db_data['mobile']
		assert data['address'] == db_data['address']
		assert checkout_info['order']['subtotal'] == db_data['subtotal']
		assert checkout_info['order']['total'] == db_data['total']
		assert checkout_info['order']['list'][0]['image'] == db_data['image']
		assert checkout_info['order']['list'][0]['name'] == db_data['name']


@allure.feature('Checkout API')
@allure.story('Checkout without login')
def test_checkout_without_login(session):
	checkout_api = CheckoutApi(session)
	checkout_api.get_prime()

	with allure.step('create order'):
		response = checkout_api.checkout()

	with allure.step('assert response and order number digits'):
		assert response.status_code == 401
		assert response.json()['errorMsg'] == 'Unauthorized'


@allure.feature('Checkout API')
@allure.story('Checkout without prime key')
def test_checkout_without_prime_key(session, login):
	checkout_api = CheckoutApi(session)

	with allure.step('Proceed to checkout'):
		response = checkout_api.checkout()

	with allure.step('assert response and order number digits'):
		assert response.status_code == 400
		assert response.json()['errorMsg'] == 'Prime value is required.'


@allure.feature('Checkout API')
@allure.story('Checkout with invalid prime key')
def test_checkout_with_invalid_prime_key(session, login):
	checkout_api = CheckoutApi(session)
	checkout_api.set_prime("this is a fake prime")

	with allure.step('Proceed to checkout'):
		response = checkout_api.checkout()

	with allure.step('assert response and order number digits'):
		assert response.status_code == 400
		assert response.json()['errorMsg'] == 'Invalid prime'


invalid_test_data = get_api_data('API Checkout with Invalid Value')
@allure.feature('Checkout API')
@allure.story('Checkout with invalid value')
@pytest.mark.parametrize('data', invalid_test_data)
def test_checkout_with_invalid_value(session, login, data): 
	checkout_api = CheckoutApi(session)
	checkout_api.get_prime()

	with allure.step('Proceed to checkout'):
		response = checkout_api.checkout(receiver=data)

	with allure.step('assert response and order number digits'):
		assert response.status_code == 400
		assert response.json()['errorMsg'] == data['errorMsg']


@allure.feature('Get order detail API')
@allure.story('Get order detail')
def test_get_order_detail(session, login, connect_db,): 
	checkout_api = CheckoutApi(session)
	get_order_api = GetOrderApi(session)
	checkout_api.get_prime()

	response = checkout_api.checkout()
	order_id = response.json()['data']['number']

	with allure.step('Get order detail'):
		get_order_response = get_order_api.get_order_info(order_id)
		data = get_order_response.json()['data']
		db_data = get_db_data(connect_db, order_id)
		checkout_info = checkout_api.get_payload_info()

	assert get_order_response.status_code == 200
	assert data['details']['recipient']['name'] == db_data['receiver']
	assert data['details']['recipient']['email'] == db_data['email']
	assert data['details']['recipient']['phone'] == db_data['mobile']
	assert data['details']['recipient']['address'] == db_data['address']
	assert checkout_info['order']['subtotal'] == db_data['subtotal']
	assert checkout_info['order']['total'] == db_data['total']
	assert checkout_info['order']['list'][0]['image'] == db_data['image']
	assert checkout_info['order']['list'][0]['name'] == db_data['name']
	


@allure.feature('Get order detail API')
@allure.story('Get order with invalid order id')
def test_get_order_detail_with_invalid_order_id(session, login):
	get_order_api = GetOrderApi(session)

	with allure.step('Get order detail'):
		get_order_response = get_order_api.get_order_info('123456789')
	
	assert get_order_response.status_code == 400
	assert get_order_response.json()['errorMsg'] == 'Order Not Found.'


@allure.feature('Get order detail API')
@allure.story('Get order detail without login')
def test_get_order_without_login(session, login):
	checkout_api = CheckoutApi(session)
	get_order_api = GetOrderApi(session)
	logout_api = LogOutApi(session)
	checkout_api.get_prime()

	response = checkout_api.checkout()
	order_id = response.json()['data']['number']


	logout_api.user_logout()

	with allure.step('Get order detail'):
		get_order_response = get_order_api.get_order_info(order_id)

	assert get_order_response.status_code == 403
	assert get_order_response.json()['errorMsg'] == 'Invalid Access Token'


@allure.feature('Get order detail API')
@allure.story('Get order detail without order id')
def test_get_order_detail_without_order_id(session, login):
	get_order_api = GetOrderApi(session)

	with allure.step('Get order detail'):
		get_order_response = get_order_api.get_order_info('')

	assert get_order_response.status_code == 404
	assert get_order_response.text.split('\n')[0] == '404 Not Found'