import logging
import pytest
import os

from utils.api_base import ApiBase



class ProfileApi(ApiBase):
	profile_page_url = f"{os.getenv('HOME_PAGE_URL')}/api/1.0/user/profile"
	

	def get_user_profile(self):
		self.api_request('get', self.profile_page_url)
		return self.response

	
	def get_user_profile_with_token(self, bearer_token):
		headers = {'Authorization': bearer_token}
		self.api_request('get', self.profile_page_url, headers = headers)
		return self.response