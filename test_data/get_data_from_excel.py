import logging
import os
import pandas as pd
import openpyxl


file_path = 'test_data/Stylish_TestCase.xlsx'

def get_test_data_from_file(sheet_name):
	logging.info('Read excel file')
	df = pd.read_excel(file_path, sheet_name, dtype=str)

	logging.info('data manipulate')
	df.fillna("", inplace=True)
	df.columns = df.columns.str.lower()
	df.columns = df.columns.str.replace(' ', '_')

	logging.info('Update cell which contains chars')
	df = df.applymap(lambda x: update_cell_contains_chars(x) if 'chars' in str(x) else x)
	
	logging.info('Update deliver time/ product color/ size base on sheet name')
	if 'Checkout' in sheet_name:
		df = df.applymap(lambda x: '不指定' if 'Anytime' in str(x) else x)
		df = df.applymap(lambda x: '08:00-12:00' if 'Morning' in str(x) else x)
		df = df.applymap(lambda x: '14:00-18:00' if 'Afternoon' in str(x) else x)
	elif 'Create Product' in sheet_name:
		df['colors'] = df['colors'].apply(lambda x: x.split(','))
		df['sizes'] = df['sizes'].apply(lambda x: x.split(','))
		df['title'] = df['title'].apply(lambda x: x + 'p' if x != '' and len(x) < 255 else x)
		df['main_image'] = df['main_image'].replace('sample image', os.path.abspath('test_data/mainImage.jpg'))
		df['other_image_1'] = df['other_image_1'].replace('sample image', os.path.abspath('test_data/otherImage0.jpg'))
		df['other_image_2'] = df['other_image_2'].replace('sample image', os.path.abspath('test_data/otherImage1.jpg'))

	data = df.to_dict(orient='records')

	return data
	
	
def update_cell_contains_chars(data):
	num_of_chars = int(data.split()[0])
	return num_of_chars * 'p'


def get_api_data(sheet_name):
	df = pd.read_excel(file_path, sheet_name, dtype=str)
	df.fillna("", inplace=True)
	df = df.applymap(lambda x: update_cell_contains_chars(x) if 'chars' in str(x) else x)
	if 'Create Product' in sheet_name:
		df['title'] = df['title'].apply(lambda x: x + 'p' if x != '' and len(x) < 255 and x != 'p' else x)
	data = df.to_dict(orient='records')
	return data