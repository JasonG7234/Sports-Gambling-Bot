class odds:

    ODDSBOOM_SPORTSBOOK_CODES = {
        "bo": "BetMGM",
        "fd": "FanDuel",
        "ti": "Tipico",
        "bg": "Borgata",
        "pb": "PointsBet",
        "dk": "DraftKings",
        "fb": "FoxBet",
        "sh": "Sugarhouse",
        "ca": "Caesars",
        "wh": "William Hill",
        "ub": "Unibet",
        "88": "888sport",
        "b3": "bet365",
        "ba": "BetAmerica",
        "gn": "Golden Nugget"
    }

    def __init__(self, sportsbook, over, strikeouts, under):
        self.sportsbook_code = sportsbook
        self.sportsbook_name = self.ODDSBOOM_SPORTSBOOK_CODES.get(sportsbook)
        self.over = over
        self.strikeouts = strikeouts
        self.under = under

    def get_sportsbook_code(self):
        return self.sportsbook_code

    def get_sportsbook_name(self):
        return self.sportsbook_name

    def get_over(self):
        return self.over

    def get_strikeouts(self):
        return self.strikeouts

    def get_under(self):
        return self.under

    def __str__(self):
        return f"{self.sportsbook_name}: {str(self.strikeouts)}. o{self.over} & u{self.under}"