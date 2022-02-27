"""
@package utilities

CheckPoint class implementation
It provides functionality to assert the result

Example:
    self.check_point.markFinal("Test Name", result, "Message")
"""

import utilities.customLogger as cl
import logging
from base.selenium_driver import SeleniumDriver

class TestStatus(SeleniumDriver):

    log = cl.customLogger(logging.INFO)

    def __init__(self, driver):
        super(TestStatus, self).__init__(driver)
        self.resultList = []

    def setResult(self, result, resultMessage):
        try:
            if result is not None:
                if result:
                    self.resultList.append("PASS")
                    self.log.info("### VERIFICATION SUCCESSFULL :: +" + resultMessage)
                else:
                    self.resultList.append("FAILED")
                    self.log.info("### VERIFICATION FAILED :: +" + resultMessage)
                    self.screenShot(resultMessage)
            else:
                self.resultList.append("FAILED")
                self.log.info("### VERIFICATION FAILED :: +" + resultMessage)
                self.screenShot(resultMessage)
        except:
            self.resultList.append("FAILED")
            self.log.info("### EXCEPTION OCCURRED !!!")
            self.screenShot(resultMessage)

    def mark(self, result, resultMessage):
        self.setResult(result, resultMessage)

    def markFinal(self, testName, result, resultMessage):
        self.setResult(result, resultMessage)

        if "FAILED" in self.resultList:
            self.log.error(testName + "### TEST FAILED")
            self.resultList.clear()
            assert True == False
        else:
            self.log.info(testName + "### TEST SUCCESSFULL")
            self.resultList.clear()
            assert True == True
