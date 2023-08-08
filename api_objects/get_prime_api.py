from ast import parse
import logging
import pytest
import os
import json
from urllib import parse


from utils.api_base import ApiBase


class GetPrimeApi(ApiBase):
	endpoint = 'https://js.tappaysdk.com/tpdirect/sandbox/getprime'


	def send(self):
		headers = {"Content-Type": "application/x-www-form-urlencoded", 
	     		   "x-api-key": os.getenv('X-API-KEY')}
		form_data = {
			'jsonString' : {
			"cardnumber":"4242424242424242",
			"cardduedate":"202904",
			"appid":"12348",
			"appkey":"app_pa1pQcKoY22IlnSXq5m5WP5jFKzoRG58VEXpT7wU62ud7mMbDOGzCYIlzzLF",
			"appname":"54.201.140.239",
			"url":"http://54.201.140.239",
			"port":"",
			"protocol":"http:",
			"tappay_sdk_version":"v5.8.0",
			"cardccv":"123"
			}
		}
		data = parse.urlencode(form_data)	
		self.api_request('post', self.endpoint, headers = headers, data = data)
		return self.response