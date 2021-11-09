from selenium.webdriver.common.by import By


class UnauthorizedPageLocators:
    LOG_IN_BUTTON_LOCATOR = (By.XPATH, '//div[contains(@class, "responseHead-module-button")]')
    LOGIN_INPUT_LOCATOR = (By.NAME, 'email')
    PASSWORD_INPUT_LOCATOR = (By.NAME, 'password')
    LOG_IN_SUBMIT_LOCATOR = (By.XPATH, '//div[contains(@class, "authForm-module-button")]')
    FORGOT_PASSWORD_LINK_LOCATOR = (By.XPATH, '//a[@href="https://account.my.com/password_reset/"]')


class AuthorizedPageLocators:
    LOG_OUT_POPUP_LOCATOR = (By.XPATH, '//div[contains(@class, "right-module-rightButton")]')
    LOG_OUT_BUTTON_LOCATOR = (By.XPATH, '//a[@href="/logout"]')


class CampaignPageLocators:
    TRAFFIC_BUTTON_LOCATOR = (By.CLASS_NAME, '_traffic')
    LINK_INPUT_LOCATOR = (By.XPATH, '//input[contains(@class, "mainUrl-module-searchInput")]')
    CAMPAIGN_NAME_INPUT_LOCATOR = (By.XPATH, '//div[contains(@class, "input_campaign-name")]//input')
    TEASER_BUTTON_LOCATOR = (By.ID, 'patterns_teaser_57_58')
    LOAD_IMAGE_90x75_LOCATOR = (By.XPATH, '//input[@type="file" and @data-test="image_90x75"]')
    CAMPAIGN_AD_TITLE_INPUT_LOCATOR = (By.XPATH, '//input[contains(@data-name, "title")]')
    CAMPAIGN_AD_DESCRIPTION_INPUT_LOCATOR = (By.XPATH, '//textarea[contains(@data-name, "text")]')
    CREATE_CAMPAIGN_SUBMIT_LOCATOR = (By.XPATH, '//div[contains(@class, "footer__buttons-wrap")]'
                                                '//button[contains(@class, "button_submit")]')

    def CAMPAIGN_NAME_CELL_LOCATOR(name):
        return (By.XPATH, f'//div[contains(@class, "nameCell-module-campaignNameCell")]'
                          f'//a[text()="{name}"]')


class SegmentPageLocators:
    HTML_ROOT_LOCATOR = (By.TAG_NAME, "html")
    ADD_SEGMENT_CHECKBOX_LOCATOR = (By.CLASS_NAME, 'adding-segments-source__checkbox')
    ADD_SEGMENT_POPUP_SUBMIT_LOCATOR = (By.CSS_SELECTOR, '.adding-segments-modal__btn-wrap .button_submit')
    SEGMENT_NAME_INPUT_LOCATOR = (By.CSS_SELECTOR, '.input_create-segment-form input')
    ADD_SEGMENT_SUBMIT_LOCATOR = (By.CSS_SELECTOR, '.create-segment-form__btn-wrap button')
    ALL_SEGMENTS_NAME_LOCATOR = (By.XPATH, '//div[contains(@class, "main-module-Table")]'
                                           '//a[contains(@href, "/segments/segments_list")]')
    REMOVE_SEGMENT_SUBMIT_LOCATOR = (By.CLASS_NAME, 'button_confirm-remove')

    def APPS_AND_GAMES_SEGMENT_LOCATOR(text):
        return (By.XPATH, f'//div[contains(@class, "adding-segments-item") and text()="{text}"]')

    def SEGMENT_NAME_CELL_LOCATOR(name):
        return (By.XPATH, f'//a[contains(@href, "/segments/segments_list") and text()="{name}"]'
                f'/ancestor::div[@data-row-id]')

    def DELETE_SEGMENT_BUTTON_LOCATOR(data_row_id):
        return (By.XPATH, f'//div[@data-row-id="{data_row_id}"]//span[contains(@class, "cells-module-removeCell")]')
