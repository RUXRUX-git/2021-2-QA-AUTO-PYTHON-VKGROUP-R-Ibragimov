import pytest
import time

from ui.locators import basic_locators
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


CLICK_RETRY = 3
MAX_TIME_WAIT = 30

class BaseCase:
    driver = None


    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver


    def find(self, locator):
        return WebDriverWait(self.driver, MAX_TIME_WAIT).until(
            EC.presence_of_element_located(locator)
        )


    def click(self, locator):
        for i in range(CLICK_RETRY):
            try:
                elem = self.find(locator)
                elem.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY-1:
                    raise


    def log_in(self, config):
        self.click(basic_locators.POPUP_LOGIN_BUTTON_LOCATOR)

        login = config['login']
        password = config['password']

        email_field = self.find(basic_locators.EMAIL_FIELD_LOCATOR)
        email_field.clear()
        email_field.send_keys(login)

        password_field = self.find(basic_locators.PASSWORD_FIELD_LOCATOR)
        password_field.clear()
        password_field.send_keys(password)

        self.click(basic_locators.SEND_LOGIN_FORM_BUTTON_LOCATOR)

        time.sleep(3) # Wait for page to load


    def log_out(self):
        self.click(basic_locators.LOGOUT_POPUP_BUTTON_LOCATOR)

        WebDriverWait(self.driver, MAX_TIME_WAIT).until(
            EC.element_to_be_clickable(basic_locators.LOGOUT_BUTTON_LOCATOR)
        )
        self.click(basic_locators.LOGOUT_BUTTON_LOCATOR)

        time.sleep(3) # Wait for page to load


    def change_contact_info(self, fio, phone):
        self.click(basic_locators.PROFILE_BUTTON_LOCATOR)

        fio_input = self.find(basic_locators.FIO_INPUT_LOCATOR)
        fio_input.clear()
        fio_input.send_keys(fio)

        phone_input = self.find(basic_locators.PHONE_INPUT_LOCATOR)
        phone_input.clear()
        phone_input.send_keys(phone)

        self.click(basic_locators.SAVE_CONTACT_INFO_BUTTON_LOCATOR)

        time.sleep(3) # Wait for page to load
