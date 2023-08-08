import os
from utils.api_base import ApiBase


class GetOrderApi(ApiBase):
    endpoint = f"{os.getenv('HOME_PAGE_URL')}/api/1.0/order"


    def get_order_info(self, order_id):
        self.endpoint = f"{self.endpoint}/{order_id}"
        self.api_request('get', self.endpoint)
        
        return self.response