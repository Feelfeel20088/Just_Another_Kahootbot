from selenium.webdriver.support.ui import WebDriverWait

# add more propertys here as needed
class Kahoot_Bot(WebDriverWait):
    index: int

    def __init__(self, driver, timeout, index, poll_frequency = ..., ignored_exceptions = None):
        super().__init__(driver, timeout, poll_frequency, ignored_exceptions)
        
        self.index = index
