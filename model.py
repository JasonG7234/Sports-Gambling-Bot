from nba_api.stats.endpoints import TeamGameLog, TeamEstimatedMetrics
import datetime
import driver
import pandas

DRIVER_LOCATION = '../chromedriver'

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

def print_full_dataframe(df):
    with pandas.option_context('display.max_columns', None):
        print(df)

def main():

    fanduel = driver.API(DRIVER_LOCATION)
    fanduel.close_overlay()
    games = fanduel.get_basketball_games()
    fanduel.quit_driver()

    for game in games:
        game.print_matchup()
        for team_id in game.get_team_ids():
            game_log = TeamGameLog(league_id_nullable="00", season="2020-21", season_type_all_star="Regular Season", team_id=team_id).get_data_frames()[0].iloc[:5]
    
    today = datetime.date.today()

    # recent_game_dates = list(game_log['GAME_DATE'])
    # for recent_game in recent_game_dates:
    #     game_date = datetime.datetime.strptime(recent_game, '%b %d, %Y').date()
    #     print((today - game_date).days)
    # recent_matchups = list(game_log['MATCHUP'])
    # for recent_matchup in recent_matchups:
    #     print('HOME' if recent_matchup[4] == 'v' else 'AWAY')

if __name__ == "__main__":
    main()