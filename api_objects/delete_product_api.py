import os
from utils.api_base import ApiBase


class DeleteProductAPI(ApiBase):
    def __init__(self, session):
        super().__init__(session)
        self.url = f"{os.getenv('HOME_PAGE_URL')}/api/1.0/admin/product"

    def send(self, product_id):
        new_url = f"{self.url}/{product_id}"
        self.api_request('delete', new_url)
        return self.response
