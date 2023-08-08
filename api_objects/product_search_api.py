import os
import logging

class ProductSearchApi():
	endpoint = f"{os.getenv('HOME_PAGE_URL')}/api/1.0/products"
    

	def get_product_by_keyword(self, session, keyword, paging):
		endpoint = f"{self.endpoint}/search?keyword={keyword}&paging={paging}"
		logging.info(f'Get product by endpoint: {endpoint}')
		response = session.get(endpoint)
		logging.info(f'Get product response by search {keyword}: {response.json()}')
		return response