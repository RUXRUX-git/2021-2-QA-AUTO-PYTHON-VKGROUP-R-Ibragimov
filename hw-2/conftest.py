import pytest

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from pages.unauthorized_page import UnauthorizedPage
from constants import *


@pytest.fixture(scope='function')
def unauthorized_page(driver):
    return UnauthorizedPage(driver)


@pytest.fixture(scope='function')
def authorized_page(unauthorized_page, login=LOGIN, password=PASSWORD):
    return unauthorized_page.log_in(login, password)


@pytest.fixture(scope='function')
def campaign_page(authorized_page):
    return authorized_page.to_campaigns()


@pytest.fixture(scope='function')
def segment_page(authorized_page):
    return authorized_page.to_segments()


@pytest.fixture(scope='function')
def driver():
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(URL)
    browser.maximize_window()

    yield browser

    browser.quit()
