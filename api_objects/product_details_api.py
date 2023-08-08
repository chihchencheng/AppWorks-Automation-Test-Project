import os
import logging

class ProductDetailsApi():
	endpoint = f"{os.getenv('HOME_PAGE_URL')}/api/1.0/products/details"
    

	def get_product_details_by_id(self, session, product_id):
		endpoint = f"{self.endpoint}?id={product_id}"
		logging.info(f'Get product by endpoint: {endpoint}')
		response = session.get(endpoint)
		logging.info(f'ProductDetailsApi- Get product detail by product id: {product_id}: \
	       \n response json: {response.json()}')
		print('')
		return response