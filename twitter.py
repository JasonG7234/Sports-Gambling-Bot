import tweepy 
import json
def send_tweet(pitchers):
    # MAKE SURE TO TEXT KEVIN FIRST
    f = open('keys.json')
    data = json.load(f)
    auth = tweepy.OAuthHandler(data["api_key"], data["api_secret"])
    auth.set_access_token(data["access_token"], data["access_secret"])

    f.close()
    best_bets = get_daily_best_bets(pitchers)
    tweepy.API(auth).update_status(status_text(best_bets))

def get_daily_best_bets(pitchers):
    #TODO: Treat as pandas
    return pitchers

def status_text(pitchers):
    tweet = "Today's top picks\U0000203C\n\n"
    for pitcher in pitchers:
        tweet = tweet + pitcher[0] + " " + pitcher[1] + " " + str(pitcher[2]) + " strikeouts. Best odds at " + pitcher[3] + " @ " + pitcher[4] + " (" + pitcher[5] + "units)\n"
    tweet = tweet + append_footer()
    return tweet

def append_footer():
    return "\n\U0001F4B0\U0001F4B0\U0001F4B0\n\n#fanduel #sportsbetting #mlb"