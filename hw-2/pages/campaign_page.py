import random
import allure

from uuid import uuid4

from pages.authorized_page import AuthorizedPage
from ui.locators import CampaignPageLocators


class CampaignPage(AuthorizedPage):
    @allure.step('Creating random campaign name')
    def create_random_campaign_name(self):
        value = 'Campaign' + str(uuid4())
        self.logger.info(f'Campaign name is "{value}"')
        return value

    @allure.step('Creating random campaign ad title')
    def create_random_campaign_ad_title(self):
        value = str(random.randint(1, 10 ** 20))
        self.logger.info(f'Title is "{value}"')
        return value

    @allure.step('Creating random campaign ad description')
    def create_random_campaign_ad_description(self):
        value = str(random.randint(1, 10 ** 50))
        self.logger.info(f'Description is "{value}"')
        return value

    @allure.step('Going to campaign creation page')
    def to_creation(self):
        self.driver.get('https://target.my.com/campaign/new/')

    @allure.step('Creating campaign')
    def create_campaign(self, tmpdir):
        self.to_creation()
        self.click(CampaignPageLocators.TRAFFIC_BUTTON_LOCATOR)
        self.send_keys(CampaignPageLocators.LINK_INPUT_LOCATOR, 'http://example.com/')
        campaign_name = self.create_random_campaign_name()
        self.send_keys(CampaignPageLocators.CAMPAIGN_NAME_INPUT_LOCATOR, campaign_name)
        self.click(CampaignPageLocators.TEASER_BUTTON_LOCATOR)
        image_path = self.create_random_image(tmpdir, 90, 75)
        self.load_file(CampaignPageLocators.LOAD_IMAGE_90x75_LOCATOR, image_path)
        self.send_keys(CampaignPageLocators.CAMPAIGN_AD_TITLE_INPUT_LOCATOR, self.create_random_campaign_ad_title())
        self.send_keys(CampaignPageLocators.CAMPAIGN_AD_DESCRIPTION_INPUT_LOCATOR,
                       self.create_random_campaign_ad_description())
        self.click(CampaignPageLocators.CREATE_CAMPAIGN_SUBMIT_LOCATOR)
        return campaign_name
