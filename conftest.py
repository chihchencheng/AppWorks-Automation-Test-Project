import pytest
import os
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
import logging

if 'ENV_FILE' in os.environ:
	env_file = os.environ['ENV_FILE']
	load_dotenv(env_file)
else:
	load_dotenv()


@pytest.fixture
def connect_db():
	db = pymysql.connect(
	host = os.getenv('DB_HOST'),
	port = int(os.getenv('PORT')),
	database = os.getenv('DATABASE'),
	user = os.getenv('USER_NAME'),
	password= os.getenv('PASSWORD'),
	cursorclass=DictCursor
	)

	try:
		if db.open:
			yield db 
	except pymysql.Error as e:
		print("Error while connecting to MySQL", e)
	finally:
		db.close()

