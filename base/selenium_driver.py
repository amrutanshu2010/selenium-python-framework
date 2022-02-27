from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import utilities.customLogger as cl
import logging
import time
import os

class SeleniumDriver():

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def screenShot(self, resultMessage):

        filename = resultMessage + "_" + str(round(time.time() * 1000)) + ".png"
        screenshotDirectory = "../../screenshots/"
        relativeFileName = screenshotDirectory + filename
        currentDirectory = os.path.dirname(__name__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, screenshotDirectory)

        try:
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            self.driver.save_screenshot(destinationFile)
            self.log.info("Screenshot saved to directory - " + destinationFile)
        except:
            self.log.info("### EXCEPTION OCCURRED !!!")
            print_stack()

    def getTitle(self):
        return self.driver.title

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type " + locatorType + " not correct/supported")
        return False

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info("Element Found with locator: " + locator + " and locatorType: " + locatorType)
        except:
            self.log.info("Element not found")
        return element

    def getElementList(self, locator, locatorType="id"):
        '''
        :param locator: any locator
        :param locatorType: specify the locator type
        :return: The list of elements
        '''
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_elements(byType, locator)
            self.log.info("Element list found with locator {} and locatorType {}".format(locator, locatorType))
        except:
            self.log.info("Element not found with locator {} and locatorType {}".format(locator, locatorType))
        return element


    def getElements(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_elements(byType, locator)
            self.log.info("Element Found with locator: " + locator + " and locatorType: " + locatorType)
        except:
            self.log.info("Element not found")
        return element

    def elementClick(self, locator='', locatorType="id", element=None):
        try:
            if locator: # This means locator is not empty
                element = self.getElement(locator, locatorType)
            element.click()
            self.log.info("Clicked on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Cannot click on the element with locator: " + locator + " locatorType: " + locatorType)
            print_stack()

    def sendKeys(self, data, locator, locatorType="id", element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.send_keys(data)
            self.log.info("Sent data to element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Cannot send data to the element with locator: " + locator + " locatorType: " + locatorType)
            print_stack()

    def getText(self, locator, locatorType='id', element=None, info=""):
        '''
        Get text on an element, either provide the element of combination of locator & locatorType
        :param locator: any locator
        :param locatorType:  spefify the locator type
        :param element: provide the element directly
        :return: the text contained in the element
        :info: info related to the element
        '''
        try:
            if locator:
                self.log.debug("In locator condition.")
                element = self.getElement(locator, locatorType)
            self.log.debug("Before finding the text.")
            text = element.text
            self.log.debug("After finding the element, size is - {}".format(len(text)))
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                self.log.info("Getting text on the element :: {}".format(info))
                self.log.info("The text is :: '{}'".format(text))
                text = text.strip()
        except:
            self.log.error("Failed to get the text on the element :: {}".format(info))
            print_stack()
            text = None
        return text


    def isElementPresent(self, locator, locatorType="id", element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info("Element present with locator: {} and locatorType: {}".format(locator, locatorType))
                return True
            else:
                self.log.info("Element is not present with locator: {} and locatorType: {}".format(locator, locatorType))
                return False
        except:
            self.log.info("Element not found")
            return False

    def isElementDisplayed(self, locator, locatorType='id', element=None):
        isDisplayed = False
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                isDisplayed = element.is_displayed()
                self.log.info("Element is displayed with locator: {} and locatorType: {}".format(locator, locatorType))
            else:
                self.log.info("Element is not displayed with locator: {} and locatorType: {}".format(locator, locatorType))
            return isDisplayed
        except:
            self.log.error("### ELEMENT NOT FOUND !!!")
            return False

    def elementPresenceCheck(self, locator, byType):
        try:
            elementList = self.driver.find_elements(byType, locator)
            if len(elementList) > 0:
                self.log.info("Element Found")
                return True
            else:
                self.log.info("Element not found")
                return False
        except:
            self.log.info("Element not found")
            return False

    def waitForElement(self, locator, locatorType="id",
                               timeout=10, pollFrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                  " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, 10, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((byType,
                                                             "stopFilter_stops-0")))
            self.log.info("Element appeared on the web page")
        except:
            self.log.info("Element not appeared on the web page")
            print_stack()
        return element

    def webScroll(self, direction = 'up'):
        if direction.lower() == "up":
            self.driver.execute_script("window.scrollBy(0, -1000);")
        elif direction.lower() == 'down':
            self.driver.execute_script("window.scrollBy(0, 1000);")
        else:
            self.log.info("Invalid argument provided for scrolling, please provide 'up' or 'down'.")

    def webScrollToElement(self, locator, locatorType="id", element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            ac = ActionChains(self.driver)
            ac.move_to_element(element).perform()
            self.log.info("Moved to the element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Could not move to the element with locator: " + locator + " locatorType: " + locatorType)
            print_stack()

    def chooseFromSelectClass(self,visible_Text, locator, locatorType="id", element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            sel = Select(element)
            sel.select_by_visible_text(visible_Text)
            self.log.info("Selected the specified dropdown with visible text as: " + visible_Text)
        except:
            self.log.info("Could not select the specified dropdown with visible text as: " + visible_Text)
            print_stack()

    def clearFields(self, locator, locatorType="id", element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.clear()
            self.log.info("Input fields are cleared for element having locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Input fields are cleared for element having locator: " + locator + " locatorType: " + locatorType)
            print_stack()


    def moveToIFrame(self, nameORID):
        try:
            if nameORID:
                self.driver.switch_to_frame(nameORID)
                self.log.info("Switched to IFrame")
            else:
                self.log.info("Iframe name or ID is not provided")
        except:
            self.log.error("Not able to switch to IFrame")

    def moveOutOfIFrame(self):
        try:
            self.driver.switch_to_default_content()
            self.log.info("Switched to default content")
        except:
            self.log.error("Not able to switch to default content")






