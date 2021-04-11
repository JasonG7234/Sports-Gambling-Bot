from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import game

CURRENT_HANDICAP_CSS = "div[class='currenthandicap']"
SELECTION_PRICE_CSS = "div[class='selectionprice']"

class API:

    def __init__(self, driver_location, url):
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
                    nba_game.set_under(handicaps[1].text[2:], selectionprices[1].text)
                except:
                    print("ERROR: No O/U for this game")
            games.append(nba_game)
        return games

    def close_numberfire_overlay(self):
        time.sleep(10)
        overlay = self.driver.find_element_by_xpath("//div[@class='signup-interstitial open']")
        login_text = overlay.find_element_by_xpath("//a[@data-login-modal-open=true()]")
        ActionChains(self.driver).move_to_element(login_text).click(login_text).perform()
        time.sleep(2)
        overlay = self.driver.find_element_by_xpath("//div[@class='modal numberFire-login open']")
        close_overlay = overlay.find_element_by_xpath("//span[@class='nf-icon icon-close']")
        ActionChains(self.driver).move_to_element(close_overlay).click(close_overlay).perform()

    def get_numberfire_projections(self):
        for lineup_dropdown in self.driver.find_elements_by_xpath("//div[@class='dfs-main__options__sections__indiv']"):
            if ("Slate" in lineup_dropdown.text):
                for dropdown in lineup_dropdown.find_elements_by_xpath("//div[@class='custom-drop']"):
                    if ("Main" in dropdown.text):
                        dropdown.click()
                        time.sleep(1)
                        for slate_option in dropdown.find_elements_by_tag_name('li'):
                            print(slate_option.text)
                            if ("All Day" in slate_option.text):
                                slate_option.click()
                                time.sleep(5)
                                return self.driver.find_element_by_css_selector('tbody.stat-table__body')
        