import logging
import os
import pymysql
from pymysql.cursors import DictCursor



def get_db_data_by_category(connect_db, category, page):
	items_per_page = 6  
	offset = page * items_per_page 
	with connect_db.cursor() as cursor:
		product_by_category_script = get_product_by_category_script(category, items_per_page, offset)
		cursor.execute(product_by_category_script)
		products = cursor.fetchall()
	
		product_img_script = get_image_by_category_script(category)
		cursor.execute(product_img_script)
		images = cursor.fetchall()

		variant_script = get_variant_by_category_script(category)
		cursor.execute(variant_script)
		variants = cursor.fetchall()
		
		color_script = f"""SELECT id, code, name FROM color;"""
		cursor.execute(color_script)
		db_colors = cursor.fetchall()

	for i in range(len(products)):
		asset_url = f'{os.getenv("HOME_PAGE_URL")}/assets/{products[i]["id"]}'
		product_images = []
		product_variant = []
		product_colors =[]
		product_sizes = []
		color_code_list = []
		for image in images:
			if products[i]['id'] == image['product_id']:
				product_images.append(f"{asset_url}/{image['image']}")
		products[i]['images'] = product_images

		for v in variants: 
			if 'product_id' in v.keys() and \
				products[i]['id'] == v['product_id']:
				for color in db_colors:
					if v['color_id'] == color['id']:
						v['color_id'] = color['code']
				v['color_code'] = v.pop('color_id')

				if v['color_code'] not in color_code_list:
					color_code_list.append(v['color_code'])
					for color in db_colors:
						if v['color_code'] == color['code']:
							product_colors.append({'code': color['code'], 'name': color['name'] })
							
				if v['size'] not in product_sizes:
					product_sizes.append(v['size'])
						
				del v['product_id']
				product_variant.append(v)
			
		
		products[i]['main_image'] = f'{asset_url}/{products[i]["main_image"]}'
		products[i]['variants'] = product_variant
		products[i]['colors'] = product_colors
		products[i]['sizes'] = product_sizes

	logging.info(f'Get test product data from db: {products}')

	return products


def get_product_by_category_script(category, items_per_page, offset):
	if category == 'all':
		return f"""
			SELECT p.id, p.category, p.title, p.description, p.price,
			p.texture, p.wash, p.place, p.note, p.story, p.main_image 
			FROM product p
			LIMIT {items_per_page} OFFSET {offset};
		"""
	else:
		return f"""
			SELECT p.id, p.category, p.title, p.description, p.price,
			p.texture, p.wash, p.place, p.note, p.story, p.main_image 
			FROM product p
			WHERE p.category ='{category}'
			LIMIT {items_per_page} OFFSET {offset};
		"""


def get_image_by_category_script(category):
	if category == 'all':
		return f"""
		SELECT pi.product_id, pi.image
		FROM product_images pi
		WHERE product_id in (
		SELECT DISTINCT id FROM product);
		"""
	else:
		return f"""
			SELECT pi.product_id, pi.image
			FROM product_images pi
			WHERE product_id in (
			SELECT DISTINCT id FROM product WHERE category ='{category}');
		"""


def get_variant_by_category_script(category):
	if category == 'all':
		return f"""
		SELECT v.product_id, v.color_id, v.size, v.stock
		FROM variant v 
		WHERE product_id in 
		(SELECT DISTINCT id FROM product p);
		"""
	else: 
		return f"""
			SELECT v.product_id, v.color_id, v.size, v.stock
			FROM variant v 
			WHERE product_id in 
			(SELECT DISTINCT id FROM product p WHERE p.category = '{category}');
		"""


def get_product_by_keyword_script(keyword, items_per_page, offset):
	return f"""
			SELECT p.id, p.category, p.title, p.description, p.price,
			p.texture, p.wash, p.place, p.note, p.story, p.main_image 
			FROM product p
			WHERE p.title like '%{keyword}%'
			LIMIT {items_per_page} OFFSET {offset};
		"""


def get_db_data_by_keyword(connect_db, keyword, page):
	items_per_page = 6  
	offset = page * items_per_page 
	with connect_db.cursor() as cursor:
		product_by_category_script = get_product_by_keyword_script(keyword, items_per_page, offset)
		cursor.execute(product_by_category_script)
		products = cursor.fetchall()

		get_img_script = f"""
			SELECT pi.product_id, pi.image
			FROM product_images pi
			WHERE pi.product_id in ({products[0]['id']});
		"""
		cursor.execute(get_img_script)
		images = cursor.fetchall()

		variant_script = f"""
			SELECT v.product_id, v.color_id, v.size, v.stock
			FROM variant v
			WHERE v.product_id in ({products[0]['id']});
		"""
		cursor.execute(variant_script)
		variants = cursor.fetchall()

		color_script = f"""SELECT id, code, name FROM color;"""
		cursor.execute(color_script)
		db_colors = cursor.fetchall()

	for i in range(len(products)):
		asset_url = f'{os.getenv("HOME_PAGE_URL")}/assets/{products[i]["id"]}'
		product_images = []
		product_variant = []
		product_colors =[]
		product_sizes = []
		color_code_list = []
		for image in images:
			if products[i]['id'] == image['product_id']:
				product_images.append(f"{asset_url}/{image['image']}")
		products[i]['images'] = product_images

		for v in variants: 
			if 'product_id' in v.keys() and \
				products[i]['id'] == v['product_id']:
				for color in db_colors:
					if v['color_id'] == color['id']:
						v['color_id'] = color['code']
				v['color_code'] = v.pop('color_id')

				if v['color_code'] not in color_code_list:
					color_code_list.append(v['color_code'])
					for color in db_colors:
						if v['color_code'] == color['code']:
							product_colors.append({'code': color['code'], 'name': color['name'] })
							
				if v['size'] not in product_sizes:
					product_sizes.append(v['size'])
						
				del v['product_id']
				product_variant.append(v)
			
		
		products[i]['main_image'] = f'{asset_url}/{products[i]["main_image"]}'
		products[i]['variants'] = product_variant
		products[i]['colors'] = product_colors
		products[i]['sizes'] = product_sizes

	logging.info(f'Get test product data from db: {products}')

	return products


def get_product_data_by_product_id(connect_db, id):

	with connect_db.cursor() as cursor:
		product_by_id_script = f"""
			SELECT p.id, p.category, p.title, p.description, p.price,
			p.texture, p.wash, p.place, p.note, p.story, p.main_image 
			FROM product p
			WHERE p.id = {id};
		"""
		cursor.execute(product_by_id_script)
		products = cursor.fetchall()

		get_img_script = f"""
			SELECT pi.product_id, pi.image
			FROM product_images pi
			WHERE pi.product_id = {id};
		"""
		cursor.execute(get_img_script)
		images = cursor.fetchall()

		variant_script = f"""
			SELECT v.product_id, v.color_id, v.size, v.stock
			FROM variant v
			WHERE v.product_id = {id};
		"""
		cursor.execute(variant_script)
		variants = cursor.fetchall()

		color_script = f"""SELECT id, code, name FROM color;"""
		cursor.execute(color_script)
		db_colors = cursor.fetchall()

	for i in range(len(products)):
		asset_url = f'{os.getenv("HOME_PAGE_URL")}/assets/{products[i]["id"]}'
		product_images = []
		product_variant = []
		product_colors =[]
		product_sizes = []
		color_code_list = []
		for image in images:
			if products[i]['id'] == image['product_id']:
				product_images.append(f"{asset_url}/{image['image']}")
		products[i]['images'] = product_images

		for v in variants: 
			if 'product_id' in v.keys() and \
				products[i]['id'] == v['product_id']:
				for color in db_colors:
					if v['color_id'] == color['id']:
						v['color_id'] = color['code']
				v['color_code'] = v.pop('color_id')

				if v['color_code'] not in color_code_list:
					color_code_list.append(v['color_code'])
					for color in db_colors:
						if v['color_code'] == color['code']:
							product_colors.append({'code': color['code'], 'name': color['name'] })
							
				if v['size'] not in product_sizes:
					product_sizes.append(v['size'])
						
				del v['product_id']
				product_variant.append(v)
			
		
		products[i]['main_image'] = f'{asset_url}/{products[i]["main_image"]}'
		products[i]['variants'] = product_variant
		products[i]['colors'] = product_colors
		products[i]['sizes'] = product_sizes

	logging.info(f'Get test product data from db: {products}')

	return products