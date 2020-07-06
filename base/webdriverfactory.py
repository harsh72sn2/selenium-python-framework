from selenium import webdriver
import os

class WebDriverFactory():

    def __init__(self, browser):
        self.browser = browser

    def getWebDriverInstance(self):
        baseUrl = "https://letskodeit.teachable.com/"
        if self.browser == "iexplorer":
            driver = webdriver.Ie()
        elif self.browser == "firefox":
            driver = webdriver.Firefox()
        elif self.browser == "chrome":
            chromedriver = ""
            os.environ["webdriver.chrome.driver"] = chromedriver
            driver = webdriver.Chrome(chromedriver)
            driver.set_window_size(1440, 900)
        else:
            driver = webdriver.Firefox()

        driver.implicitly_wait(10)
        driver.maximize_window()
        driver.get(baseUrl)
        return driver