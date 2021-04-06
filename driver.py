from selenium import webdriver
import time
import game

url = 'https://sportsbook.fanduel.com/sports'

CURRENT_HANDICAP_CSS = "div[class='currenthandicap']"
SELECTION_PRICE_CSS = "div[class='selectionprice']"

class API:

    def __init__(self, driver_location):
        self.driver = webdriver.Chrome(driver_location)
        self.driver.get(url)

    def close_overlay(self):
        time.sleep(5)
        try:
            overlay = self.driver.find_element_by_xpath("//div[@class='q-close-dynamic-overlay']")
            overlay.click()
        except:
            print("No overlay. Continuing")
        

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
                nba_game.set_away_spread(spread_div.find_elements_by_css_selector(CURRENT_HANDICAP_CSS)[0].text, #
                 spread_div.find_elements_by_css_selector(SELECTION_PRICE_CSS)[0].text)
                print(nba_game.get_away_spread())
                nba_game.set_home_spread(spread_div.find_elements_by_css_selector(CURRENT_HANDICAP_CSS)[1].text, #
                 spread_div.find_elements_by_css_selector(SELECTION_PRICE_CSS)[1].text)
                print(nba_game.get_home_spread())

            
            # Get/Set moneylines
            for moneyline_div in div.find_elements_by_css_selector("div[class='market money']"):
                nba_game.set_away_moneyline(moneyline_div.find_elements_by_css_selector(SELECTION_PRICE_CSS)[0].text)
                print(nba_game.get_away_moneyline())
                nba_game.set_home_moneyline(moneyline_div.find_elements_by_css_selector(SELECTION_PRICE_CSS)[1].text)
                print(nba_game.get_home_moneyline())

            # Get/Set market totals
            for total_div in div.find_elements_by_css_selector("div[class='market total']"):
                try:
                    nba_game.set_over(total_div.find_elements_by_css_selector(CURRENT_HANDICAP_CSS)[0].text[2:], #
                     total_div.find_elements_by_css_selector(SELECTION_PRICE_CSS)[0].text)
                    print(nba_game.get_over_total())
                    nba_game.set_under(total_div.find_elements_by_css_selector(CURRENT_HANDICAP_CSS)[1].text[2:], #
                     total_div.find_elements_by_css_selector(SELECTION_PRICE_CSS)[1].text)
                    print(nba_game.get_under_total())
                except:
                    print("ERROR: No O/U for this game")

            games.append(nba_game)
        return games