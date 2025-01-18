from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import *
from bot import *
from time import sleep
from random import randint
from errors import *
from warnings import *
from submodules.Bot_Lifetime_Manager import *
class Kahoot_Bot():
    
    def __init__(self, *, gamepin: str, bots: int, nickname: str = None, headless: bool = False) -> None:
        self.__numofbots = bots
        self.__nickname = nickname
        self.__gamepin = gamepin
        self.__nickname_count = 0
        self.__time = 2
        self.__drivers: WebDriverWait = []
        self.__options = None
        self.__num_q = 0
        if not headless:     
            self.__options = Options()
            self.__options.add_argument("--headless")
    

    @property
    def __new_Nickname(self):
        self.__nickname_count += 1
        return (self.__nickname or "bot") + str(self.__nickname_count)

    def get_Quiz_Type(self):
        pass

    # and funcunality 
    def gameEnded(self) -> bool:
        return False
    


    def join_Game(self) -> None:
        for i in range(self.__numofbots):
            print("getting webdriver")
            wait: WebDriverWait = self.__create_New_Bot()
            try:
                game_input = wait.until(EC.presence_of_element_located((By.ID, 'game-input')))
                game_input.send_keys(self.__gamepin)
                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'cOYBIH'))).click()

                nickname_input = wait.until(EC.presence_of_element_located((By.ID, 'nickname')))                    
                nickname_input.send_keys(self.__new_Nickname) 
                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'cOYBIH'))).click()


            except TimeoutException:
                if self.__debug:
                        self.__close_All_Bots()
                        raise KahootFatel(f"driver could not find kahoot elements in provided time ({self.__time}) this could either be that your internet is slow or kahoot somehow changed some classes. if you think its becuse of the classes make a issue on GH")
                
    
    def pressButton(self, button_number: int) -> bool:
        """ tell your bots to press a spesific button. returns true if the button was pressed or if at lease one bot pressed one of the buttons returns false if the bots could not find a button"""
        if button_number > 3 or button_number < 0:
            raise ValueError("int has to be in between 0 and 3")
        for driver_index in range(len(self.__drivers)):
            try:
                self.__bots.press_button(f'[data-functional-selector="answer-{button_number}"]', ["icon__Icon-sc-5okv5j-0", "iryIbt"])
                self.__drivers[driver_index].until(EC.invisibility_of_element_located((By.CLASS_NAME, "icon__Icon-sc-5okv5j-0"))) 
                self.__drivers[driver_index].until(EC.invisibility_of_element_located((By.CLASS_NAME, "iryIbt")))
                A = self.__drivers[driver_index].until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-functional-selector="answer-{button_number}"]')))
                A.click()
                print("button pressed so sigma")
            except (TimeoutException, StaleElementReferenceException):
                 # return true if a single bot or more clicked the button in this case the program was simply not fast enpp he to run though all the bots
                if driver_index > 0:
                    warn(f"all kahoot bots did not have time to click button {button_number} the round ended to quick", KahootWarning)
                    self.__num_q += 1
                    return True
                # if on the first bot return false as no bots had the chance to click sense the button doesent exsist
                return False
            
        self.__num_q += 1
        return True
try:
    kahoot = Kahoot_Bot(gamepin=input("enter the pin: "), headless=True, bots=1, nickname="cheezybaslls")
    kahoot.login()
    # exsample anser key (of course static)
    a = [0, 3, 1, 3, 2]
    index = 0
    while not kahoot.gameEnded():
         # here you could either implement your own way of getting the anser or you can call class methods for getting the algirithems
        print(index)
        if kahoot.pressButton(a[index]):
            index += 1

except KeyboardInterrupt:
    print("\ngoodbye!")
    exit()
