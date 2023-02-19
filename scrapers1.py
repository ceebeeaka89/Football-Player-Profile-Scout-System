import requests
import pprint
import pandas

class PlayerScraper:
    def __init__(self):
        self.endpoint = "https://v3.football.api-sports.io/players/topscorers"
        self.key = "38f912894585a68ef5819ed617600292"
        self._data = None

    def scrape(self):
      
        return requests.get(
            self.endpoint,  # endpoint
            headers={"x-apisports-key": self.key},
            params={"season": 2021,
                    "league":39}
        ).json()

    @property
    def data(self):
        if self._data is None:
            self._data = self.scrape()

        return self._data

    def get_goals_assists_by_player(self):
        resp = self.data["response"]
        df_data = { "name": [], "goals": [], "assists": [], "shots": [], "on": [],
                    "games":[], "duels":[], "won":[], "dribble_percent": [],
                    "fouls drawn per game":[], "penalty win per game": [], "penalty scored per game": []}

        for player_dict in resp:  # for dictionary in list
            player_info = player_dict["player"]
            name = player_info["name"]

            player_stats_list = player_dict["statistics"]
            player_stats = player_stats_list[0]  

            goal_data = player_stats["goals"]
            goals = goal_data["total"]
            assists = goal_data["assists"]

            games_data = player_stats["games"]
            apps = games_data["appearences"]

            shot_data = player_stats["shots"]
            total = shot_data["total"]
            on = shot_data["on"]

            dribble_data = player_stats["dribbles"]
            dribbles_percent = dribble_data["success"]/dribble_data["attempts"] * 100

            targMan_data = player_stats["duels"]
            Tdeuls = targMan_data["total"]
            wonDeuls = targMan_data["won"]

            penaulty_data = player_stats["penalty"]
            won = penaulty_data["won"]
            if won is None: won = 0
            won = won / apps
            scored = penaulty_data["scored"]
            if scored is None: scored = 0
            scored = scored / apps

            foul_data = player_stats["fouls"]
            drawn = foul_data["drawn"]
            if drawn is None: drawn = 0
            drawn = drawn / apps

            if total is None:
                total = 0

            if on is None:
                on = 0

            if assists is None:
                assists = 0

            if apps is None:
                apps = 0

            if Tdeuls is None:
                Tdeuls = 0

            if wonDeuls is None:
                wonDeuls = 0

            df_data["games"].append(apps)
            df_data["shots"].append(total)
            df_data["on"].append(on)
            df_data["name"].append(name)
            df_data["goals"].append(goals)
            df_data["assists"].append(assists)
            df_data["duels"].append(Tdeuls)
            df_data["won"].append(wonDeuls)
            df_data["dribble_percent"].append(dribbles_percent)
            df_data["fouls drawn per game"].append(drawn)
            df_data["penalty win per game"].append(won)
            df_data["penalty scored per game"].append(scored)

        return pandas.DataFrame(df_data)


