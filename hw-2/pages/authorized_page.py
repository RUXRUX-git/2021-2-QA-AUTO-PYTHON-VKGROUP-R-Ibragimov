import allure

from pages.base_page import BasePage
from ui.locators import AuthorizedPageLocators


class AuthorizedPage(BasePage):
    @allure.step('Logging out')
    def log_out(self):
        from pages.unauthorized_page import UnauthorizedPage

        self.click(AuthorizedPageLocators.LOG_OUT_POPUP_LOCATOR)
        self.click(AuthorizedPageLocators.LOG_OUT_BUTTON_LOCATOR)
        return UnauthorizedPage(self.driver)

    @allure.step('Going to segments page')
    def to_segments(self):
        from pages.segment_page import SegmentPage

        self.driver.get('https://target.my.com/segments/')
        return SegmentPage(self.driver)

    @allure.step('Going to campaigns page')
    def to_campaigns(self):
        from pages.campaign_page import CampaignPage

        self.driver.get('https://target.my.com/dashboard/')
        return CampaignPage(self.driver)
