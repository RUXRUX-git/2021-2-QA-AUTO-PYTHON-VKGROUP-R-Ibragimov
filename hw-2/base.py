import pytest
import os
import allure


class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def ui_report(self, driver, request, tmpdir):
        failed_tests_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_tests_count:
            screenshot = os.path.join(tmpdir.strpath, 'failure.png')
            driver.get_screenshot_as_file(screenshot)
            allure.attach.file(screenshot, 'failure.png', attachment_type=allure.attachment_type.PNG)

            browser_log = os.path.join(tmpdir.strpath, 'browser.log')
            with open(browser_log, 'w') as f:
                for i in driver.get_log('browser'):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")

            with open(browser_log, 'r') as f:
                allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)
