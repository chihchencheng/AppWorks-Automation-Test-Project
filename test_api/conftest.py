import requests
from api_objects.login_api import LoginApi
from dotenv import load_dotenv
import logging
import pytest
import os


if 'ENV_FILE' in os.environ:
	env_file = os.environ['ENV_FILE']
	load_dotenv(env_file)
else:
	load_dotenv()


@pytest.fixture
def session():
	session = requests.Session()
	yield session
	session.close()


@pytest.fixture
def login_api(session):
	return LoginApi(session)


@pytest.fixture
def login(login_api, worker_id):
	if worker_id == 'master':
		email = os.getenv('USER1_EMAIL')
	else:
		email = os.getenv(f'{worker_id}_USER_EMAIL')

	password = os.getenv(f'USER_PWD')
	return login_api.user_login('native', email, password)

