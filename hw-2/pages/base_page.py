import logging
import os
import allure
import numpy

from PIL import Image
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from constants import *


class BasePage:
    driver = None

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger('test')

    def wait(self, timeout=None):
        if timeout is None:
            timeout = BASE_TIMEOUT
        return WebDriverWait(self.driver, timeout=timeout)

    @allure.step('Finding element with locator {locator}')
    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @allure.step('Finding all elements with locator {locator}')
    def find_all(self, locator, timeout=None):
        self.wait(timeout).until(EC.presence_of_all_elements_located(locator))
        return self.driver.find_elements(*locator)

    @allure.step('Clicking on element with locator {locator}')
    def click(self, locator, timeout=BASE_TIMEOUT):
        for i in range(CLICK_RETRY):
            try:
                self.find(locator, timeout=timeout)
                elem = self.wait(timeout).until(
                    EC.element_to_be_clickable(locator))
                elem.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise

    @allure.step('Sending keys to element with locator {locator}')
    def send_keys(self, locator, keys, timeout=BASE_TIMEOUT):
        elem = self.wait(timeout).until(EC.visibility_of_element_located(locator))
        elem.clear()
        elem.send_keys(keys)

    @allure.step('Creating image with size {width}x{height}')
    def create_random_image(self, tmpdir, width, height):
        imarray = numpy.random.rand(height, width, 3) * 255  # First parameter should be height
        im = Image.fromarray(imarray.astype('uint8')).convert('RGBA')
        image_path = os.path.join(os.path.abspath(tmpdir.strpath), 'image.png')
        im.save(image_path, 'PNG')

        return image_path

    @allure.step('Sending file to element with locator {locator}. File path = "{file_path}"')
    def load_file(self, locator, file_path):
        field = self.find(locator)
        field.send_keys(file_path)
