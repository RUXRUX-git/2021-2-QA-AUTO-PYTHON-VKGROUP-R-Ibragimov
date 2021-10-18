import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from random import randint
from uuid import uuid4

CHROME_DRIVER_PATH = "./sources/chromedriver"
LOGIN    = "ruxrux2002@yandex.ru"
PASSWORD = "44f3ee14-7ba6-4177-bec8-48136ab010f0"
URL = "https://target.my.com/"

def pytest_addoption(parser):
	parser.addoption('--login', default=LOGIN)
	parser.addoption('--password', default=PASSWORD)
	parser.addoption('--url', default=URL)
	parser.addoption('--chrome_driver_path', default=CHROME_DRIVER_PATH)

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

	options = Options()
	options.page_load_strategy = 'eager'

	browser = webdriver.Chrome(executable_path=config['chrome_driver_path'], options=options)

	browser.maximize_window()
	browser.get(url)
	yield browser
	browser.close()
