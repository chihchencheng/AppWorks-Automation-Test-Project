
import json
import logging
import os
from utils.api_base import ApiBase
from api_objects.get_prime_api import GetPrimeApi


class CheckoutApi(ApiBase):
    endpoint = f"{os.getenv('HOME_PAGE_URL')}/api/1.0/order"     
    prime = ""
    payload = {}


    def checkout(self, **kwargs):
        self.payload = {
            "prime": self.prime,
            "order": {
                "shipping": "delivery",
                "payment": "credit_card",
                "subtotal": 1299,
                "freight": 30,
                "total": 1329,
                "recipient": {
                    "name": "Chen",
                    "phone": "0912345678",
                    "email": "chihchencheng31@gmail.com",
                    "address": "Taipei City",
                    "time": "morning"
                },
                "list": [
                    {
                    "color": {
                        "code": "DDF0FF",
                        "name": "淺藍"
                    },
                    "id": 201807202157,
                    "image": "http://54.201.140.239/assets/201807202157/main.jpg",
                    "name": "活力花紋長筒牛仔褲",
                    "price": 1299,
                    "qty": 1,
                    "size": "L",
                    "stock": 9
                    }
                ]
            }
        }
        if kwargs:
            self.payload['order']['recipient'] = self.set_receiver_info(kwargs['receiver'])

        self.payload['prime'] = self.prime
        self.api_request('post', self.endpoint, json = self.payload)
        return self.response
    

    def get_prime(self):
        get_prime_api = GetPrimeApi(self.session)
        response = get_prime_api.send()
        self.prime = response.json()['card']['prime']


    def set_prime(self, new_prime):
        self.prime = new_prime


    def set_receiver_info(self, data):
        return {
			"name": data['receiver'],
			"phone": data['mobile'],
			"email": data['email'],
			"address": data['address'],
			"time": data['deliver_time']
		}
    
    def get_payload_info(self):
        return self.payload