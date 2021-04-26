import csv
import driver
import time
import twitter
import sportsbook
from fuzzywuzzy import fuzz
from statistics import mean

DRIVER_LOCATION = '../chromedriver'

FANTASYPROS_URL = "https://www.fantasypros.com/mlb/projections/daily-pitchers.php"
NUMBERFIRE_URL = "https://www.numberfire.com/mlb/daily-fantasy/daily-baseball-projections#"
ODDSBOOM_URL = "https://www.oddsboom.com/login/"

DAILY_PITCHER_PROJECTIONS = []
DAILY_PITCHER_BETS = []

def populate_projections():
    webdriver = driver.numberfire(DRIVER_LOCATION, NUMBERFIRE_URL)
    numberfire_table = webdriver.get_numberfire_projections()
    for row in numberfire_table.find_elements_by_tag_name('tr'):
        player = []
        player.append(row.find_element_by_css_selector("a.full").text)
        player.append(float(row.find_element_by_css_selector("td.k").text))
        DAILY_PITCHER_PROJECTIONS.append(player)
    webdriver.quit_driver()

    webdriver = driver.fantasypros(DRIVER_LOCATION, FANTASYPROS_URL)
    fantasypros_table = webdriver.get_fantasypros_projections()
    for row in fantasypros_table.find_elements_by_tag_name('tr')[1:]:
        player = []
        cells = row.find_elements_by_tag_name('td')  
        add_matching_pitcher_entries(cells[1].find_element_by_css_selector("a.player-name").text, float(cells[3].text))
    print(DAILY_PITCHER_PROJECTIONS)
    webdriver.quit_driver()

def add_matching_pitcher_entries(name, strikeouts):
    for pitcher in DAILY_PITCHER_PROJECTIONS:
        if (fuzz.ratio(pitcher[0], name) > 92):
            pitcher.append(strikeouts)

def find_matching_pitcher_entries(name):
    for pitcher in DAILY_PITCHER_PROJECTIONS:
        if (fuzz.ratio(pitcher[0], name) > 92):
            return pitcher

def determine_confidence_interval(closest_proj, strikeouts, odds, projs):
    proj_number = abs(strikeouts - mean([mean([projs[1], projs[2]]), closest_proj]))
    if (odds[0] == '+'): #If you're getting plus money
        odds_number = round(float(odds[-3:]) / 100, 2)
    else:
        odds_number = round(100 / float(odds[-3:]), 2)
    return round(proj_number * odds_number, 1)

def main():

    populate_projections()
    
    webdriver = driver.oddsboom(DRIVER_LOCATION, ODDSBOOM_URL)
    for pitcher in webdriver.get_odds():
        pitcher_name = pitcher[0]
        pitcher_projections = find_matching_pitcher_entries(pitcher_name)
        if (not pitcher_projections or len(pitcher_projections) < 3):
            continue
        print("------------------------------------------")
        print(pitcher_projections)
        low_proj = min(pitcher_projections[1], pitcher_projections[2])
        high_proj = max(pitcher_projections[1], pitcher_projections[2])
        best_bet_for_pitcher = []
        for prop_bet in pitcher[1]:
            if (not prop_bet):
                print("No sportsbook")
                break
            print(prop_bet)
            if (float(prop_bet.get_strikeouts()) > high_proj):
                # Bet the under!
                confidence_interval = determine_confidence_interval(high_proj, prop_bet.get_strikeouts(), prop_bet.get_under(), pitcher_projections)
                if (not best_bet_for_pitcher or confidence_interval > best_bet_for_pitcher[5]):
                    best_bet_for_pitcher = [pitcher_name, "under", prop_bet.get_strikeouts(), prop_bet.get_sportsbook_name(), prop_bet.get_under(), confidence_interval]
            elif (float(prop_bet.get_strikeouts()) < low_proj):
                # Bet the over!
                confidence_interval = determine_confidence_interval(low_proj, prop_bet.get_strikeouts(), prop_bet.get_over(), pitcher_projections)
                if (not best_bet_for_pitcher or confidence_interval > best_bet_for_pitcher[5]):
                    best_bet_for_pitcher = [pitcher_name, "over", prop_bet.get_strikeouts(), prop_bet.get_sportsbook_name(), prop_bet.get_over(), confidence_interval]   
            else:
                print(prop_bet.get_sportsbook_name() + "/" + pitcher_name + " have solid projections.")
        if best_bet_for_pitcher: DAILY_PITCHER_BETS.append(best_bet_for_pitcher)
    webdriver.quit_driver()

    with open("output.csv", "a", newline="") as f:
        writer = csv.writer(f)
        #TODO: Add date to each row
        writer.writerows(DAILY_PITCHER_BETS)

    #TODO: Filter by top 3
    #twitter.send_tweet(DAILY_PITCHER_BETS)


if __name__ == "__main__":
    main()