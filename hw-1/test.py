import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ui.locators import basic_locators
from base import BaseCase
import constants


class TestOne(BaseCase):
	@pytest.mark.UI
	def test_login(self, config):
		self.log_in(config)

		assert self.find(basic_locators.PROFILE_BUTTON_LOCATOR) # Когда нашлась кнопка, мы выждали нужное время для загрузки страницы


	@pytest.mark.UI
	def test_logout(self, config):
		self.log_in(config)
		self.log_out()

		assert self.find(basic_locators.POPUP_LOGIN_BUTTON_LOCATOR)
	

	@pytest.mark.UI
	def test_change_contact_info(self, config):
		self.log_in(config)

		self.click(basic_locators.PROFILE_BUTTON_LOCATOR)
		self.change_contact_info(config)
		self.click(basic_locators.SAVE_CONTACT_INFO_BUTTON_LOCATOR)

		self.driver.refresh()

		fio_input = self.find(basic_locators.FIO_INPUT_LOCATOR)
		phone_input = self.find(basic_locators.PHONE_INPUT_LOCATOR)

		assert fio_input.get_attribute('value') == config['fio']
		assert phone_input.get_attribute('value') == config['phone']


	@pytest.mark.parametrize('url, locator', [
		("https://target.my.com/billing", basic_locators.BILLING_BUTTON_LOCATOR),
		("https://target.my.com/statistics/summary", basic_locators.STATISTICS_BUTTON_LOCATOR),
	])
	@pytest.mark.UI
	def test_subpages_transition(self, url, locator, config):
		self.log_in(config)

		self.click(locator)

		# Тут ждем, пока пройдет переадресация на итоговую страничку
		assert WebDriverWait(self.driver, constants.MAX_TIME_WAIT).until( 
			EC.url_matches(url)
		)
