from selenium.webdriver.common.by import By

POPUP_LOGIN_BUTTON_LOCATOR       = (By.CSS_SELECTOR, 'div[class^="responseHead-module-button"]')
SEND_LOGIN_FORM_BUTTON_LOCATOR   = (By.CSS_SELECTOR, 'div[class^="authForm-module-button"]')
EMAIL_FIELD_LOCATOR              = (By.NAME, 'email')
PASSWORD_FIELD_LOCATOR           = (By.NAME, 'password')

LOGOUT_POPUP_BUTTON_LOCATOR      = (By.CSS_SELECTOR, 'div[class^="right-module-rightButton"]')
LOGOUT_BUTTON_LOCATOR            = (By.XPATH, '//a[@href="/logout"]')

BILLING_BUTTON_LOCATOR           = (By.XPATH, '//a[@href="/billing"]')
STATISTICS_BUTTON_LOCATOR        = (By.XPATH, '//a[@href="/statistics"]')
PROFILE_BUTTON_LOCATOR           = (By.XPATH, '//a[@href="/profile"]') 

FIO_INPUT_LOCATOR                = (By.XPATH, '//div[contains(@class,"js-contacts-field-name")]/div/div/input')
PHONE_INPUT_LOCATOR              = (By.XPATH, '//div[contains(@class,"js-contacts-field-phone")]/div/div/input')
SAVE_CONTACT_INFO_BUTTON_LOCATOR = (By.XPATH, '//div[@class="profile-contact-info"]//div[@class="button__text"]')
