from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import utilities.custom_logger as cl
import logging
import time
import os

class SeleniumDriver():

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def screenShot(self, resultMessage):
        fileName = resultMessage + "." + str(round(time.time() * 1000)) + ".png"
        screenshotDirectory = "../screenshots/"
        relativeFileName = screenshotDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, screenshotDirectory)

        try:
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            self.driver.save_screenshot(destinationFile)
            self.log.info("Screenshot save to directory: " + destinationFile)
        except:
            self.log.error("### Exception Occurred")
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
            self.log.info("Locator type" + locatorType + "not correct/supported")

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info("Element Found with locator: " + locator + " and locatorType: " + locatorType)
        except:
            self.log.info("Element not found with locator: " + locator + " and locatorType: " + locatorType)
        return element

    def getElementList(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_elements(byType, locator)
            self.log.info("Element list found with locator: " + locator + " and locatorType: " + locatorType)
        except:
            self.log.info("Element list not found with loctor: " + locator + " and locatorType: " + locatorType)
        return element



    def isElementPresent(self, locator="", locatorType="id", element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                print("Element Found")
                return True
            else:
                print("Element not found")
                return False
        except:
            print("Element not found")
            return False

    def elementClick(self, locator="", locatorType="id", element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.click()
            self.log.info("Clicked on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Cannot click on the element with locator: " + locator + " locatorType: " + locatorType)
            print_stack()

    def sendKeys(self, data, locator="", locatorType="id", element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.sendd_keys(data)
            self.log.info("Sent data on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Cannot send data on the element with locator: " + locator +
                  " locatorType: " + locatorType)
            print_stack()

    def getText(self, locator="", locatorType="id", element=None, info=""):
        try:
            if locator:
                self.log.debug("In locator condition")
                element = self.getElement(locator, locatorType)
            self.log.debug("Before finding text")
            text = element.text
            self.log.debug("After finding element, size is: " + str(len(text)))
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                self.log.info("Getting text on element :: " + info)
                self.log.info("The text is :: " + text + "'")
                text = text.strip()
        except:
            self.log.error("Failed to get text on element " + info)
            print_stack()
            text = None
        return text

    def isElementDisplayed(self, locator="", locatorType="id", element=None):
        isDisplayed = False
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                isDisplayed = element.is_displayed()
                self.log.info("Element is displayed with locator: " + locator + " locatorType: " + locatorType)
            else:
                self.log.info("Element not displayed with locator: " + locator + " locatorType: " + locatorType)
            return isDisplayed
        except:
            print("Element not found")
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


    def waitForElement(self, locator, locatorType="id", timeout=10, pollFrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximu :: " + str(timeout) + " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, 10,poll_frequency=1,ignored_exceptions=[NoSuchElementException,
                                                                                 ElementNotVisibleException,
                                                                                 ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable(byType,""))
            self.log.info("Element appeared on the web page")
        except:
            self.log.info("Element not appeared on the web page")
            print_stack()
        return element

    def webScroll(self, direction="up"):
        if direction == "up":
            self.driver.execute_script("window.scrollBy(0, -1000);")
        if direction == "down":
            self.driver.execute_script("window.scrollBy(0, 1000);")

    def SwitchFrameByIndex(self, locator, locatorType="xpath"):

        result = False
        try:
            iframe_list = self.getElementList("//iframe", locatorType="xpath")
            self.log.info("Length of iframe list: ")
            self.log.info(str(len(iframe_list)))
            for i in range(len(iframe_list)):
                self.switchToFrame(index=iframe_list[i])
                result = self.isElementPresent(locator, locatorType)
                if result:
                    self.log.info("iframe index is:")
                    self.log.info(str(i))
                    break
                self.switchToDefaultContent()
            return result
        except:
            print("iFrame index not found")
            return result

    def switchToFrame(self, id="", name="", index=None):

        if id:
            self.driver.switch_to.frame(id)
        elif name:
            self.driver.switch_to.frame(name)
        else:
            self.driver.switch_to.frame(index)

    def switchToDefaultContent(self):

        self.driver.switch_to.default_content()

    def getElementAttributeValue(self, attribute, element=None, locator="", locatorType="id"):

        if locator:
            element = self.getElement(locator=locator, locatorType=locatorType)
        value = element.get_attribute(attribute)
        return value

    def isEnabled(self, locator, locatorType="id", info=""):

        element = self.getElement(locator, locatorType=locatorType)
        enabled = False
        try:
            attributeValue = self.getElementAttributeValue(element=element, attribute="disabled")
            if attributeValue is not None:
                enabled = element.is_enabled()
            else:
                value = self.getElementAttributeValue(element=element, attribute="class")
                self.log.info("Attribute value From Application Web Ui --> :: " + value)
                enabled = not ("disabled" in value)
            if enabled:
                self.log.info("'Element :: '" + info + "' is enabled'")
            else:
                self.log.info("'Element :: '" + info + "' is not enabled'" )
        except:
            self.log.error("'Element :: '" + info + "' state could not be found'")
        return enabled