import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from random import randint
from uuid import uuid4

import utils


def pytest_addoption(parser):
	parser.addoption('--login', default=utils.LOGIN)
	parser.addoption('--password', default=utils.PASSWORD)
	parser.addoption('--url', default=utils.URL)
	parser.addoption('--chrome_driver_path', default=utils.CHROME_DRIVER_PATH)


@pytest.fixture()
def config(request):
	login = request.config.getoption('--login')
	password = request.config.getoption('--password')
	url = request.config.getoption('--url')
	chrome_driver_path = request.config.getoption('--chrome_driver_path')

	fio = str(uuid4())
	phone = str(randint(10 ** 11, 10 ** 12 - 1))

	return {'login': login, 'password': password,'url': url, 'chrome_driver_path': chrome_driver_path,'fio': fio, 'phone': phone}


@pytest.fixture(scope='function')
def driver(config):
	url = config['url']

	# Убираем ненужные на данный момент сообщения
	options = Options()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--ignore-ssl-errors')
	options.add_experimental_option('excludeSwitches', ['enable-logging'])

	browser = webdriver.Chrome(executable_path=config['chrome_driver_path'], options=options)

	browser.maximize_window()
	browser.get(url)
	yield browser
	browser.close()
