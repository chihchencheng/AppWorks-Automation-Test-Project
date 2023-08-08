import random

def add_product_to_cart(common_page, product_page):
	common_page.open_a_random_product_page()
	product_page.select_random_size()
	product_page.click_add_to_cart()
	product_page.get_alert_msg()


# Scenario: Shopping Cart Info Correct
def test_shopping_cart_info(home_page, common_page, product_page, cart_page):
	add_product_to_cart(common_page, product_page)

	product_added_to_cart = []
	product_added_to_cart.append(product_page.get_product_detail())
	product_page.click_to_view_cart_item()
	in_cart_item = cart_page.get_all_item_in_cart()

	assert product_added_to_cart == in_cart_item, \
		f'expect: {product_added_to_cart}, actual: {in_cart_item}'
	
	
# Scenario: Remove product from cart
def test_remove_product_from_cart(home_page, common_page, product_page, cart_page):
	for i in range(2):
		add_product_to_cart(common_page, product_page)
	
	product_page.click_to_view_cart_item()
	product_in_cart = cart_page.get_all_item_in_cart()
	random_choose_product = random.choice(product_in_cart)
	cart_page.delete_one_product_in_cart(random_choose_product['product'])

	alert_msg = cart_page.get_alert_msg()
	assert alert_msg == '已刪除商品',\
	f'expect: 已刪除商品, actual: {alert_msg}'

	updated_product_in_cart = cart_page.get_all_item_in_cart()
	updated_in_cart_item_number = cart_page.get_in_cart_item_number()

	assert random_choose_product not in  updated_product_in_cart, \
		f"""
		  updated cart item: {updated_product_in_cart}, \n
		  previous: {product_in_cart}, \n
		  deleted product: {random_choose_product}
		"""
	assert updated_in_cart_item_number == '1',\
		f'expect in cart item number: 1 , actual: {updated_in_cart_item_number}'


# Scenario: Edit quantity in cart
def test_edit_quantity_in_cart(home_page, common_page, product_page, cart_page):
	select_number = 4

	add_product_to_cart(common_page, product_page)
	product_page.click_to_view_cart_item()
	unit_price = int(cart_page.get_product_unit_price())

	cart_page.update_product_quantity(str(select_number))
	alert_msg = cart_page.get_alert_msg()
	alert_msg == '已修改數量',\
	f'expect: 已修改數量, actual: {alert_msg}'

	expect_subtotal = select_number * unit_price
	updated_qty = int(cart_page.get_product_quantity())
	updated_subtotal = unit_price * updated_qty
	assert updated_subtotal == expect_subtotal, \
	f'expect: {expect_subtotal}, actual: {updated_subtotal}'