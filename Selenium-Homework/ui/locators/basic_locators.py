from selenium.webdriver.common.by import By

POPUP_LOGIN_BUTTON_LOCATOR       = (By.CSS_SELECTOR, 'div[class^="responseHead-module-button"]')
SEND_LOGIN_FORM_BUTTON_LOCATOR   = (By.CSS_SELECTOR, 'div[class^="authForm-module-button"]')
EMAIL_FIELD_LOCATOR              = (By.NAME, 'email')
PASSWORD_FIELD_LOCATOR           = (By.NAME, 'password')

LOGOUT_POPUP_BUTTON_LOCATOR      = (By.CSS_SELECTOR, 'div[class^="right-module-rightButton"]')
LOGOUT_BUTTON_LOCATOR            = (By.XPATH, '//a[text()="Выйти"]')

PROFILE_BUTTON_LOCATOR           = (By.XPATH, '//a[contains(text(), "Профиль") and contains(@class, "center-module-button")]') 
STATISTICS_BUTTON_LOCATOR        = (By.XPATH, '//a[contains(text(), "Статистика") and contains(@class, "center-module-button")]')
BILLING_BUTTON_LOCATOR           = (By.XPATH, '//a[contains(text(), "Баланс") and contains(@class, "center-module-button")]')

FIO_INPUT_LOCATOR                = (By.XPATH, '//div[contains(@class,"js-contacts-field-name")]/div/div/input')
PHONE_INPUT_LOCATOR              = (By.XPATH, '//div[contains(@class,"js-contacts-field-phone")]/div/div/input')
SAVE_CONTACT_INFO_BUTTON_LOCATOR = (By.XPATH, '//div[contains(text(), "Сохранить") and contains(@class, "button")]')
