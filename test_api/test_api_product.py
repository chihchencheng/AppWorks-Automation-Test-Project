from api_objects.product_category_api import ProductCategoryApi
from api_objects.product_details_api import ProductDetailsApi
from api_objects.product_search_api import ProductSearchApi
import pytest
import allure
import logging
from pytest_unordered import unordered

from utils.get_db_data import get_db_data_by_category, get_db_data_by_keyword, get_product_by_keyword_script, get_product_data_by_product_id

test_category = ['all','women', 'men' , 'accessories']  


@pytest.mark.flaky(reruns=1, reruns_delay=2)	
@allure.feature('Get product by category')
@allure.story('Get product by category successfully')
@pytest.mark.parametrize('data', test_category)
def test_get_product_category(connect_db, session, data, page=0):
	product_category_api = ProductCategoryApi()
	db_data = get_db_data_by_category(connect_db, data, page)
	response = product_category_api.get_product_by_category(session, data, page)
	res_json = response.json()["data"]
	assert response.status_code == 200
	logging.info(f'expect code: 200, actual status code: {response.status_code} ')
	for i in range(len(db_data)): 
		print(f"db data {i}: {db_data[i]}")
		print(f"response json {i}: {res_json[i]}")
		assert db_data[i]['id'] == res_json[i]['id']
		assert db_data[i]['category'] == res_json[i]['category']
		assert db_data[i]['title'] == res_json[i]['title']
		assert db_data[i]['description'] == res_json[i]['description']
		assert db_data[i]['price'] == res_json[i]['price']
		assert db_data[i]['texture'] == res_json[i]['texture']
		assert db_data[i]['wash'] == res_json[i]['wash']
		assert db_data[i]['place'] == res_json[i]['place']
		assert db_data[i]['note'] == res_json[i]['note']
		assert db_data[i]['story'] == res_json[i]['story']
		assert db_data[i]['main_image'] == res_json[i]['main_image']
		assert db_data[i]['images'] == unordered(res_json[i]['images'])
		for j in range(len(db_data[i]['variants'])):
			assert db_data[i]['variants'][j] == res_json[i]['variants'][j]
		assert db_data[i]['sizes'] == res_json[i]['sizes']


@allure.feature('Get product by category')
@allure.story('Get product with invalid category')
def test_get_product_with_invalid_category(session, category='fashion'):
	page=0
	product_category_api = ProductCategoryApi()
	response = product_category_api.get_product_by_category(session, category, page)
	assert response.status_code == 400
	assert response.json()['errorMsg'] == "Invalid Category"
	logging.info(f'expect status: 400, actual status code: {response.status_code}')
	logging.info(f'expect message: "Invalid Category", actual: {response.json()["errorMsg"]}')


@allure.feature('Search product by keyword')
@allure.story('Search product with valid keyword successfully')
def test_search_product_by_keyword_successfully(connect_db, session):
	keyword='防曬' 
	paging=0
	db_data = get_db_data_by_keyword(connect_db, keyword, paging) 
	product_search_api = ProductSearchApi()
	response = product_search_api.get_product_by_keyword(session, keyword, paging)
	res_json = response.json()["data"]
	assert response.status_code == 200
	logging.info(f'expect status code: 200, actual is: {response.status_code}')
	for i in range(len(res_json)): 
		print(f"db data {i}: {db_data[i]}")
		print(f"response json {i}: {res_json[i]}")
		assert db_data[i]['id'] == res_json[i]['id']
		assert db_data[i]['category'] == res_json[i]['category']
		assert db_data[i]['title'] == res_json[i]['title']
		assert db_data[i]['description'] == res_json[i]['description']
		assert db_data[i]['price'] == res_json[i]['price']
		assert db_data[i]['texture'] == res_json[i]['texture']
		assert db_data[i]['wash'] == res_json[i]['wash']
		assert db_data[i]['place'] == res_json[i]['place']
		assert db_data[i]['note'] == res_json[i]['note']
		assert db_data[i]['story'] == res_json[i]['story']
		assert db_data[i]['main_image'] == res_json[i]['main_image']
		assert db_data[i]['images'] == unordered(res_json[i]['images'])
		for j in range(len(db_data[i]['variants'])):
			assert db_data[i]['variants'][j] == res_json[i]['variants'][j]
		assert db_data[i]['sizes'] == res_json[i]['sizes']
	

@allure.feature('Search product by keyword')
@allure.story('Search product with invalid keyword')
def test_search_product_by_invalid_keyword(session):
	keyword=123
	paging=0
	product_search_api = ProductSearchApi()
	response = product_search_api.get_product_by_keyword(session, keyword, paging)
	res_json = response.json()["data"]

	assert response.status_code == 200
	assert res_json == []


@allure.feature('Get product details by product id')
@allure.story('Get product details by product id successfully')
def test_get_product_details_by_product_id(connect_db, session):
	id=201807201824
	db_data = get_product_data_by_product_id(connect_db, id)
	product_details_api = ProductDetailsApi()
	response = product_details_api.get_product_details_by_id(session, id)
	res_json = response.json()["data"]

	assert response.status_code == 200
	logging.info(f'expect status code: 200, actual is: {response.status_code}')

	assert db_data[0]['id'] == res_json['id']
	assert db_data[0]['category'] == res_json['category']
	assert db_data[0]['title'] == res_json['title']
	assert db_data[0]['description'] == res_json['description']
	assert db_data[0]['price'] == res_json['price']
	assert db_data[0]['texture'] == res_json['texture']
	assert db_data[0]['wash'] == res_json['wash']
	assert db_data[0]['place'] == res_json['place']
	assert db_data[0]['note'] == res_json['note']
	assert db_data[0]['story'] == res_json['story']
	assert db_data[0]['main_image'] == res_json['main_image']
	assert db_data[0]['images'] == unordered(res_json['images'])
	for j in range(len(db_data[0]['variants'])):
		assert db_data[0]['variants'][j] == res_json['variants'][j]
	assert db_data[0]['sizes'] == res_json['sizes']


@allure.feature('Get product details by product id')
@allure.story('Get product details by invalid product id')
def test_get_product_details_by_invalid_product_id(session):
	id=123
	product_details_api = ProductDetailsApi()
	response = product_details_api.get_product_details_by_id(session, id)

	assert response.status_code == 400
	logging.info(f'expect status code: 400, actual is: {response.status_code}')
	assert response.json()['errorMsg'] == 'Invalid Product ID'
	logging.info(f'expect error msg: Invalid Product ID, actual msg: {response.json()["errorMsg"]}')