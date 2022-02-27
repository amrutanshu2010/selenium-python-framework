import logging
import time

import utilities.customLogger as cl
from base.selenium_driver import SeleniumDriver

class RegisterCoursesPage(SeleniumDriver):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _all_courses = "ALL COURSES" # By Link Text
    _search_box = "//input[@id='search']" # By Xpath
    _search_query = "Javascript" # simple string
    _search = "//button[@type='submit']" # By Xpath
    _course_name = "//div[@id='course-list']//div/div/a/div/div[2]/div/span[2]" # By Xpath
    _enroll_button = "//div[@id='zen_cs_desc_with_promo_dynamic']//button[contains(text(), 'Enroll in Course')]" # By Xpath
    _order_summary_page = "checkout-order-summary" # By ID
    _iframe_cc_num = 0 # IFrame reference
    _cc_num = "//input[@placeholder='Card Number']" # By Xpath
    _card_number = "5217291897266824" # A number for input
    _iframe_cc_exp = 1 # IFrame name
    _cc_exp = "//input[@placeholder='MM / YY']" # By Xpath
    _card_expiry = "0326" # A number for input
    _iframe_cc_cvv = 2 # IFrame name
    _cc_cvv = "//input[@placeholder='Security Code']" # By Xpath
    _card_cvv = "023" # A number for input
    _cc_country = "//select[@name='country-list']" # By Xpath & this element should be used in select class
    _country = "Australia"
    _submit_button = "//div[@class='stripe-outer ']/div[2]/div/button[1]/i" # By Xpath
    _card_declined_msg = "//div[@id='page']/div[3]/div/div/div/div/p" # By xpath

    # Login method could be used in the main test file from login_page
    # To click on All courses button
    def clickAllCourses(self):
        # self.waitForElement(self._all_courses, locatorType="link")
        self.elementClick(self._all_courses, locatorType="link")

    # To send keys to search box
    def enterSearchCriteria(self):
        # self.waitForElement(self._search_box, locatorType="xpath")
        self.sendKeys(self._search_query, self._search_box, locatorType="xpath")

    # To click on search button
    def clickSearchButton(self):
        self.elementClick(self._search, locatorType="xpath")

    # click on the searched course
    def clickCourse(self):
        try:
            element_present = self.elementPresenceCheck(self._course_name, byType="xpath")
            self.log.info(
                "Element present with locator: {} and locatorType: {}".format(self._course_name, "xpath"))
            if element_present:
                self.elementClick(self._course_name, locatorType="xpath")
                self.log.info("Clicked on the element with locator: {} and locatorType: {}".format(self._course_name, "xpath"))
            else:
                self.log.info("Unable to click on the element with locator: {} and locatorType: {}".format(self._course_name, "xpath"))
        except:
            self.log.error("Unable to find the element with locator: {} and locatorType: {}".format(self._course_name, "xpath"))




    # Ensure that we are on the correct page
    def orderSummaryPage(self):
        try:
            element_present = self.isElementDisplayed(self._order_summary_page, locatorType='id')
            if element_present:
                self.log.info(
                    "We are on a correct page with locator: {} and locatorType: {}".format(self._order_summary_page, "ID"))
            else:
                self.log.info(
                    "We are on an incorrect page with locator: {} and locatorType: {}".format(self._order_summary_page, "ID"))
        except:
            self.log.error("Unable to locate element with locator: {} and locatorType: {}".format(self._order_summary_page, "ID"))

    # click on enroll button
    def clickEnrollButton(self):
        try:
            element_present = self.elementPresenceCheck(self._enroll_button, byType="xpath")
            if element_present:
                self.elementClick(self._enroll_button, locatorType="xpath")
                self.log.info("Clicked on enroll button with locator : {} and locatorType: {}".format(self._enroll_button, "xpath"))
            else:
                self.log.info(
                    "Enroll button is not present with locator : {} and locatorType: {}".format(self._enroll_button,
                                                                                            "xpath"))
        except:
            self.log.error("Unable to find the Enroll button with locator : {} and locatorType: {}".format(self._enroll_button, "xpath"))


    # To scroll into view
    def scrollToCardNumber(self):
        self.driver.switch_to_frame(self._iframe_cc_num)
        self.webScrollToElement(self._cc_num, locatorType="xpath")

    # Enter card number
    def enterCardNumber(self, num=_cc_num):
        self.sendKeys(self._card_number, num, locatorType="xpath")
        self.moveOutOfIFrame()

    # Enter card expiry date
    def enterCardExpiry(self, exp=_cc_exp):
        self.moveToIFrame(self._iframe_cc_exp)
        self.sendKeys(self._card_expiry, exp, locatorType="xpath")
        self.moveOutOfIFrame()

    # Enter CVV
    def enterCardCVV(self, cvv=_cc_cvv):
        self.moveToIFrame(self._iframe_cc_cvv)
        self.sendKeys(self._card_cvv, cvv, locatorType="xpath")
        self.moveOutOfIFrame()

    # Enter country
    def enterCountry(self, country_name):
        self.chooseFromSelectClass(visible_Text=country_name, locator=self._cc_country, locatorType="xpath")

    def enterCrediCardInfo(self, num=_cc_num, exp=_cc_exp, cvv=_cc_cvv, country_name=_country):
        self.scrollToCardNumber()
        # self.clearFields(num, locatorType="xpath")
        self.enterCardNumber(num)
        # self.clearFields(exp, locatorType="xpath")
        self.enterCardExpiry(exp)
        # self.clearFields(cvv, locatorType="xpath")
        self.enterCardCVV(cvv)
        self.enterCountry(country_name)

    def clickSubmitButton(self):
        self.elementClick(self._submit_button, locatorType="xpath")


    def enrollCourse(self, num=_cc_num, exp=_cc_exp, cvv=_cc_cvv):
        time.sleep(3)
        self.clickAllCourses()
        self.enterSearchCriteria()
        self.clickSearchButton()
        time.sleep(10)
        self.clickCourse()
        self.orderSummaryPage()
        self.clickEnrollButton()
        time.sleep(10)
        self.enterCrediCardInfo()
        self.clickSubmitButton()

    def verifyEnrollFailed(self):
        result = self.isElementPresent(self._card_declined_msg, locatorType="xpath")
        return result


