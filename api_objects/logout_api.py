import logging
import pytest
import os

from utils.api_base import ApiBase

class LogOutApi(ApiBase):
	endpoint  = f"{os.getenv('HOME_PAGE_URL')}/api/1.0/user/logout"


	def user_logout(self):
		self.api_request('post', self.endpoint)
		return self.response