from random import randint
from uuid import uuid4

def get_login(request):
	return request.config.getoption('--login')

def get_password(request):
	return request.config.getoption('--password')

def get_url(request):
	return request.config.getoption('--url')

def get_chrome_driver_path(request):
	return request.config.getoption('--chrome_driver_path')

def get_fio():
	return str(uuid4())

def get_phone():
	return str(randint(10 ** 11, 10 ** 12 - 1))
