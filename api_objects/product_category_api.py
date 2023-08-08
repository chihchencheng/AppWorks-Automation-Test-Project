import os
import logging

class ProductCategoryApi():
	product_category_endpoint = f"{os.getenv('HOME_PAGE_URL')}/api/1.0/products"

	def get_product_by_category(self, session, category, paging):
		endpoint = f"{self.product_category_endpoint}/{category}?paging={paging}"
		response = session.get(endpoint)

		return response