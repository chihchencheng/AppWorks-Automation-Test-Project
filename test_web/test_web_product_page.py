import logging
import random
import pytest
from page_objects.product_page import ProductPage



# Scenario: Color Selection
def test_color_selection(home_page,common_page, product_page):
	common_page.open_a_random_product_page()
	colors = product_page.find_all_color_option()
	color = random.choice(colors)
	product_page.select_color(color)
	selected_color = product_page.get_selected_color()

	assert selected_color == color, \
		f'expect: {color}, actual: {selected_color}'


# Scenario: Size Selection
def test_size_selection(home_page, common_page, product_page):
	common_page.open_a_random_product_page()

	size_options = product_page.find_all_size_option()

	size = random.choice(size_options)
	product_page.select_size(size)
	selected_size = product_page.get_selected_size()

	assert selected_size == size, f'expect: {size}, actual: {selected_size}'


# Scenario: Quantity Editor Disabled
def test_editor_disabled(home_page, common_page, product_page):
	qty_default_value = '1'
	common_page.open_a_random_product_page()

	product_page.increase_product_qty()
	product_qty = product_page.get_qty_value()

	assert product_qty == qty_default_value,\
		  f'expect: {qty_default_value}, actual: {product_qty}'


# Scenario: Quantity Editor - Increase Quantity
def test_increase_quantity(home_page, common_page, product_page):
	default_qty = 1
	first_time_add_qty = 8
	second_time_add_qty = 2
	common_page.open_a_random_product_page()

	size_options = product_page.find_all_size_option()
	product_page.select_size(random.choice(size_options))

	for i in range(first_time_add_qty):
		product_page.increase_product_qty()

	product_qty = product_page.get_qty_value()
	expect_qty = str(default_qty+first_time_add_qty)
	assert product_qty == expect_qty, \
		f'current product qty: {product_qty},	expect product qty: {expect_qty}'

	for i in range(second_time_add_qty):
		product_page.increase_product_qty()
	second_product_qty = product_page.get_qty_value()
	assert second_product_qty == expect_qty, \
		f'current product qty: {second_product_qty}, expect product qty: {expect_qty}'


# Scenario: Quantity Editor - Decrease Quantity
def test_decrease_quantity(home_page, common_page, product_page):
	default_qty = '1'
	add_qty = 8

	common_page.open_a_random_product_page()

	size_options = product_page.find_all_size_option()
	product_page.select_size(random.choice(size_options))

	for i in range(add_qty):
		product_page.increase_product_qty()

	for i in range(add_qty):
		product_page.decrease_product_qty()

	product_qty = product_page.get_qty_value()

	assert product_qty == default_qty,\
		  f'current product qty: {product_qty}, expect product qty: {default_qty}'


# Scenario: Add To Cart - Success
def test_add_to_cart(home_page, common_page, product_page):
	common_page.open_a_random_product_page()

	size_options = product_page.find_all_size_option()
	product_page.select_size(random.choice(size_options))
	
	logging.info('加入購物車')
	product_page.click_add_to_cart()
	alert_msg = product_page.get_alert_msg()
	assert alert_msg == '已加入購物車',\
		  f'expect: "已加入購物車", actual: {alert_msg}'
	assert product_page.get_in_cart_item_number() == '1'


# Scenario: Add To Cart - Failed
def test_add_to_cart_fail(home_page, common_page, product_page):
	common_page.open_a_random_product_page()

	product_page.click_add_to_cart()

	alert_msg = product_page.get_alert_msg()
	assert alert_msg == '請選擇尺寸',\
		  f'expect: "已加入購物車", actual: {alert_msg}'