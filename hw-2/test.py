import pytest
import allure

from base import BaseCase
from ui.locators import UnauthorizedPageLocators
from ui.locators import CampaignPageLocators
from ui.locators import SegmentPageLocators
from constants import *


@allure.feature('UI tests')
@allure.story('Negative login tests')
class TestNegativeLogin(BaseCase):
    @pytest.mark.UI
    def test_not_matching_password(self, unauthorized_page):
        """Trying to authorize with invalid password"""

        assert unauthorized_page.log_in(
            LOGIN, PASSWORD + 'ABCD').find(UnauthorizedPageLocators.FORGOT_PASSWORD_LINK_LOCATOR)

    @pytest.mark.UI
    def test_invalid_login(self, unauthorized_page):
        """Trying to authorize with invalid login"""

        assert unauthorized_page.log_in(
            LOGIN + 'ABCD', PASSWORD).find(UnauthorizedPageLocators.FORGOT_PASSWORD_LINK_LOCATOR)


@allure.feature('UI tests')
@allure.story('Campaign creation tests')
class TestCampaignCreation(BaseCase):
    @pytest.mark.UI
    def test_campaign_creation(self, tmpdir, campaign_page):
        """Create campaign and check it in campaigns list"""

        name = campaign_page.create_campaign(tmpdir)
        campaign_page.find(CampaignPageLocators.CAMPAIGN_NAME_CELL_LOCATOR(name))


@allure.feature('UI tests')
@allure.story('Test segment creation and deletion')
class TestSegment(BaseCase):
    @pytest.mark.UI
    def test_segment_creation(self, segment_page):
        """Create segment, check in in segments list and then delete it"""

        name = segment_page.create_segment()
        segment_names = [elem.text for elem in segment_page.find_all(SegmentPageLocators.ALL_SEGMENTS_NAME_LOCATOR)]
        assert name in segment_names
        segment_page.delete_segment(name)

    @pytest.mark.UI
    def test_segment_deletion(self, segment_page):
        """Create segment, delete it and then check it is not in segments list"""

        name = segment_page.create_segment()
        segment_page.delete_segment(name)
        segment_page.driver.refresh()
        segment_names = [elem.text for elem in segment_page.find_all(SegmentPageLocators.ALL_SEGMENTS_NAME_LOCATOR)]
        assert name not in segment_names
