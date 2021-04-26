from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException
import error
import json
import time
import re
import sportsbook

class numberfire:

    def __init__(self, driver_location, url):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(driver_location)
        self.driver.get(url)

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
        self.close_numberfire_overlay()
        for lineup_dropdown in self.driver.find_elements_by_xpath("//div[@class='dfs-main__options__sections__indiv']"):
            if ("Slate" in lineup_dropdown.text):
                for dropdown in lineup_dropdown.find_elements_by_xpath("//div[@class='custom-drop']"):
                    if ("Main" in dropdown.text):
                        try:
                            dropdown.click()
                            time.sleep(1)
                            for slate_option in dropdown.find_elements_by_tag_name("li"):
                                if ("All Day" in slate_option.text):
                                    slate_option.click()
                                    time.sleep(5)
                                    return self.driver.find_element_by_css_selector("tbody.stat-table__body")
                        except ElementClickInterceptedException:
                            error.send_email("driver.py line 36 -> Numberfire can't select 'All Day' from the dropdown for some reason.")
                            return self.driver.find_element_by_css_selector("tbody.stat-table__body")
    def quit_driver(self):
        self.driver.quit()

class fantasypros:

    def __init__(self, driver_location, url):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(driver_location)
        self.driver.get(url)
    
    def get_fantasypros_projections(self):
        self.close_fantasypros_overlays()
        self.driver.find_element_by_css_selector("a#login-upgrade-btn").click()
        time.sleep(2)
        return self.login_to_fantasypros()

    def close_fantasypros_overlays(self):
        time.sleep(10)
        overlays = self.driver.find_elements_by_css_selector("iframe[id*='google_ads_iframe']")
        if (overlays): self.driver.switch_to.frame(overlays[len(overlays)-1])
        time.sleep(1)
        close_ad = self.driver.find_element_by_css_selector("div#closebutton")
        if (close_ad and close_ad.is_displayed()):
            close_ad.click()
            time.sleep(1)
        self.driver.switch_to.default_content()
        close_cookies_div = self.driver.find_element_by_css_selector("button.onetrust-close-btn-handler")
        if (not close_cookies_div): close_cookies_div = self.driver.find_element_by_css_selector("button.onetrust-accept-btn-handler")
        if (close_cookies_div and close_cookies_div.is_displayed()):
            close_cookies_div.click()

    def login_to_fantasypros(self):
        f = open('keys.json')
        data = json.load(f)
        self.driver.find_element_by_css_selector("input#id_username").send_keys(data['username'])
        self.driver.find_element_by_css_selector("input#id_password").send_keys(data['fantasypros_password'])
        f.close()
        self.driver.find_element_by_xpath("//button[contains(text(), 'LOG IN')]").click()
        time.sleep(2)
        return self.driver.find_element_by_css_selector("table#data")

    def quit_driver(self):
        self.driver.quit()

class oddsboom:

    def __init__(self, driver_location, url):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(driver_location)
        self.driver.get(url)

    def get_odds(self):
        self.login_to_oddsboom()
        count = 0
        strikeout_props = []
        while (True):
            time.sleep(5)
            try: 
                games = self.driver.find_element_by_css_selector("div.games")
                elem = games.find_elements_by_xpath("./*")[1+count]
            except NoSuchElementException:
                error.send_email("driver.py line 103 -> Oddsboom went back too many times, I think it forgot to find the strikeouts page.")
                return strikeout_props
            except IndexError:
                print("Have found all children elements on the page... moving on.")
                return strikeout_props
            if (elem.tag_name == 'a'):
                print("GAME #" + str(count) + ": " + elem.text)
                strikeout_props.extend(self.get_strikeout_props_per_game(elem))
                print(strikeout_props)
                count = count + 1
                print("==================================")
            else:
                print("DONE")
                return strikeout_props

    def login_to_oddsboom(self):
        f = open('keys.json')
        data = json.load(f)
        self.driver.find_element_by_css_selector("input#email").send_keys(data['username'])
        self.driver.find_element_by_css_selector("input#password").send_keys(data['oddsboom_password'])
        f.close()
        self.driver.find_element_by_css_selector("input#register").click()
        time.sleep(5)
        return self.driver.find_element_by_xpath("//a[contains(text(), 'MLB')]").click()

    def get_strikeout_props_per_game(self, elem):
        strikeout_props = []
        elem.click()
        time.sleep(8)
        try:
            self.driver.find_element_by_xpath("//button[contains(text(), 'Strikeouts')]").click()
        except NoSuchElementException:
            print("No strikeouts props button this game... moving on.")
            for i in range(0,1): 
                self.driver.back()
                time.sleep(1)
            return strikeout_props
        time.sleep(8)
        try:
            table_odds = self.driver.find_element_by_css_selector("table.odds")
            strikeout_props = self.loop_through_strikeout_table(table_odds)
        except NoSuchElementException:
            print("No strikeout props table this game... moving on.")
        
        # return back 
        for i in range(0,2): 
            self.driver.back()
            time.sleep(1)
        return strikeout_props
        
    def loop_through_strikeout_table(self, table_odds):
        strikeout_props = []
        for pitcher in table_odds.find_elements_by_tag_name("tr")[1:]:
            player = []
            sportsbooks = []
            cells = pitcher.find_elements_by_tag_name("td")
            player.append(re.sub("[^a-zA-Z\s]+", "", cells[0].text).replace("\n", " ").strip())
            for td in cells[1:]:
                try:
                    bookie = td.get_attribute("data-book")
                    over = td.text[2:6]
                    strikeouts = float(td.find_element_by_tag_name("strong").text)
                    under = td.text[-4:]
                    sportsbooks.append(sportsbook.odds(bookie, over, strikeouts, under))
                except NoSuchElementException:
                    print("There might not be a prop here... moving on.")
                except ValueError:
                    print("Couldn't find the strikeouts page I think... moving on.")
            player.append(sportsbooks)
            strikeout_props.append(player)
        return strikeout_props

    def quit_driver(self):
        self.driver.quit()