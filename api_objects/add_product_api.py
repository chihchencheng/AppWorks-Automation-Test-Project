import json
import os
import logging
from utils.api_base import ApiBase


class AddProductAPI(ApiBase):
    product_info = {
        "category": "men",
        "title": "p",
        "description": "p",
        "price": 0,
        "texture": "p",
        "wash": "p",
        "place": "p",
        "note": "p",
        "color_ids": ["2", "3"],
        "sizes": ["L", "XL"],
        "story": "p",
        "main_image": "",
        "other_images": [""]
    }


    def __init__(self, session): 
        super().__init__(session)
        self.session = session
        self.url = f"{os.getenv('HOME_PAGE_URL')}/api/1.0/admin/product"
        self.body = self.product_info

        self.files = []
        

    def send(self, **kwargs):
        if kwargs:
            self.set_product_info(kwargs['product'])

        self.api_request('post', url = self.url, data = self.body, files = self.files)
        return self.response
    
    def set_product_info(self, data):
        self.body['category'] = data['category']
        self.body['title'] = data['title']
        self.body['description'] = data['description']
        self.body['price'] = data['price']
        self.body['texture'] = data['texture']
        self.body['wash'] = data['wash']
        self.body['place'] = data['place_of_product']
        self.body['note'] = data['note']
        self.body['color_ids'] = list(data['color_id'].split(','))
        self.body['sizes'] = list(data['sizes'].split(','))
        self.body['story'] = data['story']
        self.set_product_image(data)


    def set_product_image(self, data):
        if data['main_image'] != "":
            main_image = f"test_data/{data['main_image']}"
            self.files.append(('main_image', open(main_image, 'rb')))
        else:
            logging.info("no main image")

        if data['other_image_1'] != "":
            image_path = f"test_data/{data['other_image_1']}"
            self.files.append(('other_images', open(image_path, 'rb')))
        else:
            logging.info("no other image 1")

        if data['other_image_2'] != "":
            image_path = f"test_data/{data['other_image_2']}"
            self.files.append(('other_images', open(image_path, 'rb')))
        else:
            logging.info("no other image 2")





        

