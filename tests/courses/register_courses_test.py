from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.home.login_page import LoginPage
from utilities.teststatus import TestStatus
import unittest
from base.webdriverfactory import WebDriverFactory
from pages.courses.register_courses_page import RegisterCoursesPage

class RegisterCoursesTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        wdf = WebDriverFactory(browser='chrome')
        cls.driver = wdf.getWebDriverInstance()

    def setUp(self):
        self.lp = LoginPage(self.driver)
        self.ts = TestStatus(self.driver)

    def test1_validLogin(self):
        self.lp.login("test@email.com", "abcabc")

    def test2_register_courses(self):
        self.rcp = RegisterCoursesPage(self.driver)
        self.rcp.enrollCourse()
        result = self.rcp.verifyEnrollFailed()
        self.ts.markFinal("Register Courses", result, "Registering for  a course")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)
