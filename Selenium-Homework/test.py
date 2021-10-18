import pytest

from ui.locators import basic_locators
from base import BaseCase

class TestOne(BaseCase):
	@pytest.mark.UI
	def test_login(self, config):
		self.log_in(config)

		profile_button = self.find(basic_locators.PROFILE_BUTTON_LOCATOR) # Когда нашлась кнопка, мы выждали нужное время для загрузки страницы
		assert "Профиль" in self.driver.page_source

	@pytest.mark.UI
	def test_logout(self, config):
		self.log_in(config)
		self.log_out()

		popup_login_button = self.find(basic_locators.POPUP_LOGIN_BUTTON_LOCATOR) # Когда нашлась кнопка, мы выждали нужное время для загрузки страницы

		assert "Войти" in self.driver.page_source
	
	@pytest.mark.UI
	def test_change_contact_info(self, config):
		fio = config['fio']
		phone = config['phone']

		self.log_in(config)

		self.click(basic_locators.PROFILE_BUTTON_LOCATOR)
		self.change_contact_info(fio, phone)
		self.click(basic_locators.SAVE_CONTACT_INFO_BUTTON_LOCATOR)

		self.driver.refresh()

		fio_input = self.find(basic_locators.FIO_INPUT_LOCATOR)
		phone_input = self.find(basic_locators.PHONE_INPUT_LOCATOR)

		assert fio_input.get_attribute('value') == fio
		assert phone_input.get_attribute('value') == phone

	@pytest.mark.parametrize('url, locator', [
		("https://target.my.com/billing", basic_locators.BILLING_BUTTON_LOCATOR),
		("https://target.my.com/statistics/summary", basic_locators.STATISTICS_BUTTON_LOCATOR),
	])
	@pytest.mark.UI
	def test_subpages_transition(self, url, locator, config):
		self.log_in(config)

		self.click(locator)

		assert(self.driver.current_url == url)		



