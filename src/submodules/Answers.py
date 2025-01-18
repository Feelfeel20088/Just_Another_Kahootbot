from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
__all__ = ["e"]

class e:
    def __init__(self):
        self.__soup: BeautifulSoup

    def get_page(self, game_name: str):
        driver = Firefox(options=self.__options)
        driver.get(f"https://create.kahoot.it/search-results/all?query={game_name.replace(" ", "+")}&orderBy=relevance&inventoryItemId=ANY")
        driver = WebDriverWait(driver, self.__kahoot.__time)
        driver.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="kahoot titled Videojuegos. View more details about this kahoot"]')))