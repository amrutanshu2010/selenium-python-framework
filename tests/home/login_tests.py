from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.home.login_page import LoginPage
from utilities.teststatus import TestStatus
import unittest
from base.webdriverfactory import WebDriverFactory


class LoginTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        wdf = WebDriverFactory(browser='chrome')
        cls.driver = wdf.getWebDriverInstance()

    def setUp(self):
        self.lp = LoginPage(self.driver)
        self.ts = TestStatus(self.driver)

    def test_invalidLogin(self):
        self.lp.login("test@email.com", "abca123")
        result = self.lp.verifyLoginFailed()
        assert result == True

    def test_validLogin(self):
        self.lp.login("test@email.com", "abcabc")
        result1 = self.lp.verifyTitle()
        self.ts.mark(result1, "Title is incorrect")
        result2 = self.lp.verifyLoginSuccess()
        self.ts.makrFinal("test_validLogin", result2, "Login Failed")
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)