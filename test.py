from bs4 import BeautifulSoup
import driver
import re
import requests

DRIVER_LOCATION = '../chromedriver'

FANTASYPROS_URL = "https://www.fantasypros.com/mlb/projections/daily-pitchers.php"
NUMBERFIRE_URL = "https://www.numberfire.com/mlb/daily-fantasy/daily-baseball-projections#"

DAILY_PITCHER_PROJECTIONS = []

def find_site(url):
    response = requests.get(url)
    try: 
        html = response.content.decode("utf-8")
    except UnicodeDecodeError:
        html = response.content.decode("latin-1")
    return BeautifulSoup(re.sub("<!--|-->","", html), "html.parser")


def main():
    webdriver = driver.API(DRIVER_LOCATION, NUMBERFIRE_URL)
    webdriver.close_numberfire_overlay()
    numberfire_table = webdriver.get_numberfire_projections()
    
    for row in numberfire_table.find_elements_by_tag_name('tr'):
        player = []
        player.append(row.find_element_by_css_selector("a.full").text)
        player.append(row.find_element_by_css_selector("td.k").text)
        print(player)
        DAILY_PITCHER_PROJECTIONS.append(player)
    
    webdriver.quit_driver()

if __name__ == "__main__":
    main()
