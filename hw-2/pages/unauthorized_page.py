import allure

from pages.base_page import BasePage

from pages.authorized_page import AuthorizedPage
from ui.locators import UnauthorizedPageLocators


class UnauthorizedPage(BasePage):
    @allure.step('Loggin in. Login = "{login}", password = "{password}"')
    def log_in(self, login, password):
        self.click(UnauthorizedPageLocators.LOG_IN_BUTTON_LOCATOR)
        self.send_keys(UnauthorizedPageLocators.LOGIN_INPUT_LOCATOR, login)
        self.send_keys(UnauthorizedPageLocators.PASSWORD_INPUT_LOCATOR, password)
        self.click(UnauthorizedPageLocators.LOG_IN_SUBMIT_LOCATOR)
        return AuthorizedPage(self.driver)
