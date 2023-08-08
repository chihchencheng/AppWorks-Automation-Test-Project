import json
import logging
import os
import allure
import pytest
from api_objects.delete_product_api import DeleteProductAPI
from api_objects.login_api import LoginApi
from api_objects.logout_api import LogOutApi
from api_objects.add_product_api import AddProductAPI
from test_data.get_data_from_excel import get_api_data


def get_db_data(connect_db, keyword):
	with connect_db.cursor() as cursor:
		sql = f"""
			SELECT * FROM(   
			SELECT p.*, m1.images, m2.variant, m3.color_ids, m4.sizes FROM stylish_backend.product AS p
			LEFT JOIN (			
			SELECT pi.product_id as id, GROUP_CONCAT(pi.image) AS images
			FROM stylish_backend.product AS p
			LEFT JOIN stylish_backend.product_images AS pi ON p.id = pi.product_id
			GROUP BY pi.product_id
			) m1 on p.id = m1.id
			LEFT JOIN (
			SELECT v.product_id as id, JSON_ARRAYAGG(JSON_OBJECT('color_code', c.code, 'size', v.size, 'stock', v.stock)) AS variant 
			FROM stylish_backend.product AS p
			LEFT JOIN  stylish_backend.variant AS v ON p.id = v.product_id
			LEFT JOIN stylish_backend.color AS c ON v.color_id = c.id
			GROUP BY v.product_id 
			) m2 on  p.id = m2.id
			LEFT JOIN (
			SELECT v.product_id as id,GROUP_CONCAT( DISTINCT v.color_id) AS color_ids
			FROM stylish_backend.product AS p
			LEFT JOIN stylish_backend.variant AS v ON p.id = v.product_id
			GROUP BY v.product_id
			) m3 on p.id = m3.id
			LEFT JOIN (
			SELECT v.product_id as id,GROUP_CONCAT( DISTINCT v.size) AS sizes
			FROM stylish_backend.product AS p
			LEFT JOIN stylish_backend.variant AS v ON p.id = v.product_id
			GROUP BY v.product_id
			) m4 on p.id = m4.id
			) main 
			WHERE main.id = '{keyword}';
		"""
		cursor.execute(sql)
		data = cursor.fetchall()

		product = {
			'id': data[0]['id'],
			'category': data[0]['category'],
			'title': data[0]['title'],
			'description': data[0]['description'],
			'price': data[0]['price'],
			'texture': data[0]['texture'],
			'wash': data[0]['wash'],
			'place': data[0]['place'],
			'note': data[0]['note'],
			'story': data[0]['story'],
			'color_ids': data[0]['color_ids']
		}

		return product


valid_product = get_api_data('API Create Product Success')
@allure.feature('Add product API')
@allure.story('Add product and delete product successfully')
@pytest.mark.parametrize('data', valid_product)
def test_create_product_successfully(session, connect_db, login, data):
	add_product_api =  AddProductAPI(session)
	delete_product_api = DeleteProductAPI(session)
	product_id = ''

	try:
		with allure.step('POST add product request'):
			response = add_product_api.send(product = data)
			assert response.status_code == 200
			product_id = response.json()['data']['product_id']
			db_data = get_db_data(connect_db, product_id)

			assert data['title'] == db_data['title']
			assert data['category'] == db_data['category']
			assert data['description'] == db_data['description']
			assert int(data['price']) == db_data['price']
			assert data['texture'] == db_data['texture']
			assert data['wash'] == db_data['wash']
			assert data['place_of_product'] == db_data['place']
			assert data['note'] == db_data['note']
			assert data['story'] == db_data['story']
			assert data['color_id'] == db_data['color_ids']

	except Exception as e:
		logging.error(f'Unable to create product {data["title"]}: {str(e)}')
		raise e
	finally:
		with allure.step('DELETE success newly added product'):
			delete_product_api.send(product_id)


invalid_product = get_api_data('API Create Product Failed')
@allure.feature('Add product API')
@allure.story('Add product unsuccessfully')
@pytest.mark.parametrize('data', invalid_product)
def test_unable_to_create_product(session, login, data):
	add_product_api =  AddProductAPI(session)
	response = ''
	try:
		with allure.step(f'POST add product request, {data["title"]}'):
			response = add_product_api.send(product = data)
			assert response.status_code == 400
			assert response.json()['errorMsg'] == data['errorMsg']
	except Exception as e:
		logging.error(f'Unable to create product {data["title"]}: {str(e)}')
		raise e
	finally:
		with allure.step('DELETE product if created'):
			if response.status_code == 200:
				product_id = response.json()['data']['product_id']
				delete_product_api = DeleteProductAPI(session)	
				delete_product_api.send(product_id)


one_valid_product = [valid_product[0]]
@allure.feature('Add product API')
@allure.story('Add product without login')
@pytest.mark.parametrize('data', one_valid_product)
def test_add_product_without_login(session, data):  
	add_product_api =  AddProductAPI(session)
	delete_product_api = DeleteProductAPI(session)
	product_id = ''

	try:
		with allure.step('POST add product request'):
			response = add_product_api.send(product = data)
			assert response.status_code == 401
			assert response.json()['errorMsg'] == 'Unauthorized'

	except Exception as e:
		if response.status_code == 200:
			product_id = response.json()['data']['product_id']
		logging.error(f'Add product without login error: {str(e)}')
		raise e
	finally:
		with allure.step('DELETE if product added'):
			if product_id != "":
				delete_product_api.send(product_id)


@allure.feature('Delete product API')
@allure.story('Delete product with invalid product id')
def test_delete_product_with_invalid_product_id(session, login):
	delete_product_api = DeleteProductAPI(session)
	product_id = '1234'

	with allure.step('DELETE product request'):
		response = delete_product_api.send(product_id)
		assert response.status_code == 400
		assert response.json()['errorMsg'] == 'Product ID not found.'


@allure.feature('Delete product API')
@allure.story('Delete product without login')
@pytest.mark.parametrize('data', one_valid_product)
def test_delete_product_without_login(session, login, data):
	add_product_api =  AddProductAPI(session)
	delete_product_api = DeleteProductAPI(session)
	login_api = LoginApi(session)
	logout_api = LogOutApi(session)
	product_id = ''

	with allure.step('POST add product request'):
			response = add_product_api.send(product = data)
			assert response.status_code == 200
			product_id = response.json()['data']['product_id']

	with allure.step('POST logout'):
		logout_api.user_logout()

	with allure.step('POST delete product'):	
		try:
			del_response = delete_product_api.send(product_id)
			assert del_response.status_code == 403
			assert del_response.json()['errorMsg'] == 'Invalid Access Token'
		finally:
			with allure.step('DELETE added product'):
				login_api.user_login('native', os.getenv('USER2_EMAIL'), os.getenv('USER_PWD'))
				delete_product_api.send(product_id)