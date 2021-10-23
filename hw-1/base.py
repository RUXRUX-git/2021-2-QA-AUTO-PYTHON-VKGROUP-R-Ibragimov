import pytest

from selenium.common.exceptions import (StaleElementReferenceException, 
                                       ElementClickInterceptedException, 
                                       ElementNotInteractableException) 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ui.locators import basic_locators
import constants


# Ничего лучше не придумал)) просто проверить кликабельность не получится,
# потому что кнопка выхода выезжает вместе с попапом
class click_or_false(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            element.click()
            return element
        except (StaleElementReferenceException, 
            ElementClickInterceptedException, ElementNotInteractableException):
            return False


class BaseCase:
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver


    def find(self, locator):
        return WebDriverWait(self.driver, constants.MAX_TIME_WAIT).until(
            EC.presence_of_element_located(locator)
        )


    def click(self, locator):
        for i in range(constants.MAX_CLICKS_COUNT):
            try:
                elem = self.find(locator)
                elem.click()
                return
            except StaleElementReferenceException:
                if i == constants.MAX_CLICKS_COUNT - 1:
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


    def log_out(self):
        popup_locator = basic_locators.LOGOUT_POPUP_BUTTON_LOCATOR
        button_locator = basic_locators.LOGOUT_BUTTON_LOCATOR

        self.click(popup_locator)

        WebDriverWait(self.driver, constants.MAX_TIME_WAIT).until(
            click_or_false(button_locator)
            )


    def change_contact_info(self, config):
        fio = config['fio']
        phone = config['phone']

        self.click(basic_locators.PROFILE_BUTTON_LOCATOR)

        fio_input = self.find(basic_locators.FIO_INPUT_LOCATOR)
        fio_input.clear()
        fio_input.send_keys(fio)

        phone_input = self.find(basic_locators.PHONE_INPUT_LOCATOR)
        phone_input.clear()
        phone_input.send_keys(phone)

        self.click(basic_locators.SAVE_CONTACT_INFO_BUTTON_LOCATOR)
