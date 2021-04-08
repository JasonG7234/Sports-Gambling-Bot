from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import game

url = 'https://sportsbook.fanduel.com/sports'

CURRENT_HANDICAP_CSS = "div[class='currenthandicap']"
SELECTION_PRICE_CSS = "div[class='selectionprice']"

class API:

    def __init__(self, driver_location):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(driver_location)
        self.driver.get(url)

    def close_overlay(self):
        time.sleep(5)
        try:
            overlay = self.driver.find_element_by_xpath("//div[@class='q-close-dynamic-overlay']")
            overlay.click()
        except:
            print("No overlay. Continuing")

    def quit_driver(self):
        self.driver.quit()
        

    def get_basketball_games(self):

        basketball_tab = self.driver.find_element_by_xpath("//a[contains(@href,'/sports/navigation/830.1')]")
        if (basketball_tab): 
            basketball_tab.click()
            time.sleep(5)
            main = self.driver.find_element_by_tag_name("main")
            return self.populate_game_elements(main.find_elements_by_class_name("event"))
        else: 
            print("ERROR: Could not find basketball tab.")
            self.driver.quit()
    
    def populate_game_elements(self, divs):
        games = []
        for div in divs:
            nba_game = game.NBAGame()

            # Get/Set team names
            nba_game.set_away_team(div.find_elements_by_css_selector("span[class='name']")[0].text)
            print(nba_game.get_away_team())
            nba_game.set_home_team(div.find_elements_by_css_selector("span[class='name']")[1].text)
            print(nba_game.get_home_team())
            
            # Get/Set spreads
            for spread_div in div.find_elements_by_css_selector("div[class='market points']"):
                try:
                    handicaps = spread_div.find_elements_by_css_selector(CURRENT_HANDICAP_CSS)
                    selectionprices = spread_div.find_elements_by_css_selector(SELECTION_PRICE_CSS)
                    nba_game.set_away_spread(handicaps[0].text, selectionprices[0].text)
                    nba_game.set_home_spread(handicaps[2].text, selectionprices[1].text)
                except:
                    print("ERROR: No spread for this game")

            
            # Get/Set moneylines
            for moneyline_div in div.find_elements_by_css_selector("div[class='market money']"):
                try: 
                    moneylines = moneyline_div.find_elements_by_css_selector(SELECTION_PRICE_CSS)
                    nba_game.set_away_moneyline(moneylines[0].text)
                    nba_game.set_home_moneyline(moneylines[1].text)
                except:
                    print("ERROR: No moneyline for this game")

            # Get/Set market totals
            for total_div in div.find_elements_by_css_selector("div[class='market total']"):
                try:
                    handicaps = total_div.find_elements_by_css_selector(CURRENT_HANDICAP_CSS)
                    selectionprices = total_div.find_elements_by_css_selector(SELECTION_PRICE_CSS)
                    nba_game.set_over(handicaps[0].text[2:], selectionprices[0].text)
                    nba_game.set_under(handicaps[2].text[2:], selectionprices[1].text)
                except:
                    print("ERROR: No O/U for this game")
            games.append(nba_game)
        return games