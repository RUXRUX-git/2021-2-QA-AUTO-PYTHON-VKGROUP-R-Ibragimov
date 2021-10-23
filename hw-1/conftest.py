import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import constants
import utils


def pytest_addoption(parser):
	parser.addoption('--login', default=constants.LOGIN)
	parser.addoption('--password', default=constants.PASSWORD)
	parser.addoption('--url', default=constants.URL)
	parser.addoption('--chrome_driver_path', default=constants.CHROME_DRIVER_PATH)


@pytest.fixture()
def config(request):
	return {'login': utils.get_login(request), 
			'password': utils.get_password(request),
			'url': utils.get_url(request), 
			'chrome_driver_path': utils.get_chrome_driver_path(request),
			'fio': utils.get_fio(), 
			'phone': utils.get_phone()}


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
