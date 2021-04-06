from nba_api.stats.endpoints import ScoreboardV2, TeamEstimatedMetrics
from datetime import date
import driver
import pandas

DRIVER_LOCATION = '../chromedriver'

team_id_mapper = {'Atlanta Hawks': 1610612737, 'Boston Celtics': 1610612738, 'Cleveland Cavaliers': 1610612739, 'New Orleans Pelicans': 1610612740, 'Chicago Bulls': 1610612741,
                  'Dallas Mavericks': 1610612742, 'Denver Nuggets': 1610612743, 'Golden State Warriors': 1610612744, 'Houston Rockets': 1610612745, 'Los Angeles Clippers': 1610612746,
                  'Los Angeles Lakers': 1610612747, 'Miami Heat': 1610612748, 'Milwaukee Bucks': 1610612749, 'Minnesota Timberwolves': 1610612750, 'Brooklyn Nets': 1610612751,
                  'New York Knicks': 1610612752, 'Orlando Magic': 1610612753, 'Indiana Pacers': 1610612754, 'Philadelphia 76ers': 1610612755, 'Phoenix Suns': 1610612756,
                  'Portland Trail Blazers': 1610612757, 'Sacramento Kings': 1610612758, 'San Antonio Spurs': 1610612759, 'Oklahoma City Thunder': 1610612760, 'Toronto Raptors': 1610612761,
                  'Utah Jazz': 1610612762, 'Memphis Grizzlies': 1610612763, 'Washington Wizards': 1610612764, 'Detroit Pistons': 1610612765, 'Charlotte Hornets': 1610612766}

headers = {
        'Host': 'stats.nba.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://stats.nba.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'x-nba-stats-origin': 'stats',
        'x-nba-stats-token': 'true'
}

TEST_GAME_ID = "0022000747"

#test = TeamEstimatedMetrics(league_id="00", season="2020-21", season_type="Regular Season").get_data_frames()

#with pandas.option_context('display.max_columns', None):
#        print(test)

# set window size attribute to ensure consistency across devices

def main():
    fanduel = driver.API(DRIVER_LOCATION)
    fanduel.close_overlay()
    basketball_games = fanduel.get_basketball_games()


if __name__ == "__main__":
    main()