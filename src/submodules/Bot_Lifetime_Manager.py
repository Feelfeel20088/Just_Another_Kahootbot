from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from errors import *
from warnings import *
from bot import *
from types import overload

class Bot_Lifetime_Manager:
    """wrapper class for selenium suited for my needs"""
    
    @staticmethod
    def create_New_Bot(self, index, time, options) -> Kahoot_Bot:
        driver = Firefox(options=self.__options)
        driver.get("https://kahoot.it/")
        return Kahoot_Bot(driver, self.__time, index)
    
    @staticmethod
    def close_Bot(bot: Kahoot_Bot) -> None:
        bot.driver.quit()
        del bot

    @overload
    @staticmethod
    def close_Bot(bots: list[Kahoot_Bot]) -> None:
        for bot in bots:
            Bot_Lifetime_Manager.close_Bot(bot)
        del bot
        
    
    # please modify. if new support needs to be added for new button funcunality add it here
    @staticmethod
    def click_Button(bot: WebDriverWait, element: str, type: By, waiters: list[str] = [], waiter_types: list[By] = []): 
        i: str
        try: 
            for i in range(len(waiters)):
                bot.until(EC.invisibility_of_element_located((waiter_types[i], waiters[i])))
            
            bot.until(EC.element_to_be_clickable((type, element))).click()
        except (TimeoutException):
            warn(f"could not find element: {element}", KahootWarning)
    
    @overload
    @staticmethod
    def click_Button(bots: list[WebDriverWait], element: str, type: By, waiters: list[str] = [], waiter_types: list[By] = []):
        for bot in range(len(bots)):
            Bot_Lifetime_Manager.click_Button(bot, element, type, waiters, waiter_types)







__all__ = [Kahoot_Bot, Bot_Lifetime_Manager]

 