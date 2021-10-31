import allure
from uuid import uuid4

from pages.authorized_page import AuthorizedPage
from ui.locators import SegmentPageLocators


class SegmentPage(AuthorizedPage):
    @allure.step('Getting segment row id by segment name "{segment_name}"')
    def get_segment_row_id(self, segment_name):
        value = self.find(SegmentPageLocators.SEGMENT_NAME_CELL_LOCATOR(segment_name)).get_attribute('data-row-id')
        self.logger.info('Segment row id is "{value}"')
        return value

    @allure.step('Creating random segment name')
    def create_random_segment_name(self):
        value = 'Segment' + str(uuid4())
        self.logger.info(f'Segment name is "{value}"')
        return value

    @allure.step('Going to segment creation page')
    def to_creation(self):
        self.driver.get('https://target.my.com/segments/segments_list/new/')

    @allure.step('Going to segments list page')
    def to_list(self):
        self.driver.get('https://target.my.com/segments/segments_list/')

    @allure.step('Creating segment')
    def create_segment(self):
        self.to_creation()
        self.click(SegmentPageLocators.APPS_AND_GAMES_SEGMENT_LOCATOR)
        self.click(SegmentPageLocators.ADD_SEGMENT_CHECKBOX_LOCATOR)
        self.click(SegmentPageLocators.ADD_SEGMENT_POPUP_SUBMIT_LOCATOR)
        segment_name = self.create_random_segment_name()
        self.send_keys(SegmentPageLocators.SEGMENT_NAME_INPUT_LOCATOR, segment_name)
        self.click(SegmentPageLocators.ADD_SEGMENT_SUBMIT_LOCATOR)
        return segment_name

    @allure.step('Deleting segment with name "{segment_name}"')
    def delete_segment(self, segment_name):
        self.to_list()
        row_id = self.get_segment_row_id(segment_name)
        print(row_id)
        self.click(SegmentPageLocators.DELETE_SEGMENT_BUTTON_LOCATOR(row_id))
        self.click(SegmentPageLocators.REMOVE_SEGMENT_SUBMIT_LOCATOR)
