from nba_api.stats.endpoints import TeamGameLog, TeamEstimatedMetrics
import datetime
import driver
import pandas
import time

DRIVER_LOCATION = '../chromedriver'
URL = 'https://sportsbook.fanduel.com/sports'

RECENT_GAME_COUNT = 8

TEST_GAME_ID = "0022000747"

def print_full_dataframe(df):
    with pandas.option_context('display.max_columns', None):
        print(df)

def main():

    league_team_metrics = TeamEstimatedMetrics(league_id="00", season="2020-21", season_type="Regular Season").get_data_frame()[0]

    fanduel = driver.API(DRIVER_LOCATION, URL)
    fanduel.close_overlay()
    games = fanduel.get_basketball_games()
    fanduel.quit_driver()

    #EFG = (FG + 0.5 * 3P) / FGA

    B2B_With_Travel = pandas.DataFrame()
    B2B_With_No_Travel = pandas.DataFrame()
    #Three_In_Four = [] ????? 
    Home = pandas.DataFrame()
    Away = pandas.DataFrame()

    recent_game = -1

    for game in games:
        game.print_matchup()
        for team_id in game.get_team_ids():
            most_recent_game_date = datetime.date.today()
            was_most_recent_game_home = False

            game_log = TeamGameLog(league_id_nullable="00", season="2020-21", season_type_all_star="Regular Season", team_id=team_id).get_data_frames()[0].iloc[:RECENT_GAME_COUNT]
            print("Fetching team metrics ")
            time.sleep(30)
            team_metrics = league_team_metrics.loc[league_team_metrics['TEAM_ID'] == team_id]
            for i in range(0,RECENT_GAME_COUNT):

                # Append game row to home or away list 
                is_current_game_home = True if str(game_log.iloc[i]['MATCHUP'])[4] == 'v' else False
                if is_current_game_home:
                    Home = Home.append(game_log.iloc[i])
                else: 
                    Away = Away.append(game_log.iloc[i]) #???

                current_game_date = datetime.datetime.strptime(game_log.iloc[i]['GAME_DATE'], '%b %d, %Y').date()
                days_between_games = (most_recent_game_date - current_game_date).days
                if (days_between_games == 1):
                    if (is_current_game_home and was_most_recent_game_home):
                        B2B_With_No_Travel = B2B_With_No_Travel.append(game_log.iloc[i])
                    else:
                        B2B_With_Travel = B2B_With_Travel.append(game_log.iloc[i])
                
                was_most_recent_game_home = is_current_game_home
                most_recent_game_date = current_game_date
                        
    #print_full_dataframe(Home)

    home_win_pct = (Home['WL'] == 'W').sum() / len(Home.index)

    print("Home team won: " + str(home_win_pct) + "%")
    print("Away team won: " + str((Away['WL'] == 'W').sum()) + "/" + str(len(Away.index)))
    print("B2B with travel team won: " + str((B2B_With_Travel['WL'] == 'W').sum()) + "/" + str(len(B2B_With_Travel.index)))
    print("B2B no travel team won: " + str((B2B_With_No_Travel['WL'] == 'W').sum()) + "/" + str(len(B2B_With_No_Travel.index)))

if __name__ == "__main__":
    main()