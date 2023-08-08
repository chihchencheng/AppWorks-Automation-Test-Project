import logging
import pytest
import os

from utils.api_base import ApiBase



class LoginApi(ApiBase):
	login_endpoint = f"{os.getenv('HOME_PAGE_URL')}/api/1.0/user/login"
	

	def user_login(self, provider, email, password):
		payload = {
		"provider": provider,
		"email": email,
		"password": password
		}
		self.api_request('post', self.login_endpoint, json = payload)
		if self.response.status_code == 200:
			self.session.headers.update({'Authorization': self.response.json()['data']['access_token']})
		
		return {'response':self.response, 
	  			'session': self.session}

	