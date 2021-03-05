# -*- coding: utf-8 -*-
import unittest

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var elements = document.querySelector('downloads-manager')
        .shadowRoot.querySelector('#downloadsList')
        .items
        if (elements.every(e => e.state === 'COMPLETE'))
        return elements.map(e => e.filePath || e.file_path || e.fileUrl || e.file_url);
        """)


# class Create(unittest.TestCase):
#     def setUp(self):
#         chrome_options = webdriver.ChromeOptions()
#         prefs = {'download.default_directory': '/Users/chenxinlu/Downloads/tron-wallet/'}
#         chrome_options.add_experimental_option('prefs', prefs)
#         self.driver = webdriver.Chrome(options=chrome_options, executable_path="/usr/local/bin/chromedriver")
#         self.driver.implicitly_wait(10)
#         self.verificationErrors = []
#         self.accept_next_alert = True
#
#     def test_create(self):
#         driver = self.driver
#         # Label: Test
#         driver.get("https://tronscan.org/#/walletwizard")
#         driver.find_element_by_name("password_input").click()
#         driver.find_element_by_name("password_input").clear()
#         driver.find_element_by_name("password_input").send_keys(
#             "innocentkitfaithpaperhorsearmysaydistancekingdomboardtouristmeat")
#         driver.find_element_by_css_selector("button.btn.btn-dark.btn-lg.ml-auto > span").click()
#         driver.find_element_by_css_selector("button.btn.btn-lg.btn-block > span").click()
#         # waits for all the files to be completed and returns the paths
#         paths = WebDriverWait(driver, 120, 1).until(every_downloads_chrome)
#         print(paths)
#
#     def is_element_present(self, how, what):
#         try:
#             self.driver.find_element(by=how, value=what)
#         except NoSuchElementException as e:
#             return False
#         return True
#
#     def is_alert_present(self):
#         try:
#             self.driver.switch_to_alert()
#         except NoAlertPresentException as e:
#             return False
#         return True
#
#     def close_alert_and_get_its_text(self):
#         try:
#             alert = self.driver.switch_to_alert()
#             alert_text = alert.text
#             if self.accept_next_alert:
#                 alert.accept()
#             else:
#                 alert.dismiss()
#             return alert_text
#         finally:
#             self.accept_next_alert = True
#
#     def tearDown(self):
#         # self.driver.quit()
#         # self.driver.close()
#         self.assertEqual([], self.verificationErrors)
class Create(object):
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': '/Users/chenxinlu/Downloads/tron-wallet/'}
        chrome_options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(options=chrome_options, executable_path="/usr/local/bin/chromedriver")
        self.driver.implicitly_wait(10)
        # self.accept_next_alert = True
        # self.verificationErrors = []

    def test_create(self):
        driver = self.driver
        # Label: Test
        driver.get("https://tronscan.org/#/walletwizard")
        driver.find_element_by_name("password_input").click()
        driver.find_element_by_name("password_input").clear()
        driver.find_element_by_name("password_input").send_keys(
            "innocentkitfaithpaperhorsearmysaydistancekingdomboardtouristmeat")
        driver.find_element_by_css_selector("button.btn.btn-dark.btn-lg.ml-auto > span").click()
        driver.find_element_by_css_selector("button.btn.btn-lg.btn-block > span").click()
        # waits for all the files to be completed and returns the paths
        paths = WebDriverWait(driver, 120, 1).until(every_downloads_chrome)
        print(paths[0])

    def close(self):
        self.driver.quit()

    # def is_element_present(self, how, what):
    #     try:
    #         self.driver.find_element(by=how, value=what)
    #     except NoSuchElementException as e:
    #         return False
    #     return True
    #
    # def is_alert_present(self):
    #     try:
    #         self.driver.switch_to_alert()
    #     except NoAlertPresentException as e:
    #         return False
    #     return True
    #
    # def close_alert_and_get_its_text(self):
    #     try:
    #         alert = self.driver.switch_to_alert()
    #         alert_text = alert.text
    #         if self.accept_next_alert:
    #             alert.accept()
    #         else:
    #             alert.dismiss()
    #         return alert_text
    #     finally:
    #         self.accept_next_alert = True
    #
    # def tearDown(self):
    #     # self.driver.quit()
    #     # self.driver.close()
    #     self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    create_wallet = Create()
    for i in range(0, 100):
        create_wallet.test_create()
    create_wallet.close()
