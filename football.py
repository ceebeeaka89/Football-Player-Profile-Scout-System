import pandas
import matplotlib.pyplot as plt
import seaborn as sns
from scrapers import PlayerScraper
from soccerplots.radar_chart import Radar

playerstats = PlayerScraper()

df = playerstats.get_goals_assists_by_player()


# target man: high assists, high goals, high duels
# dribbler : high dribbling, concedes fowls
# ALL: played lots of games..!

def extra_columns(df):
    df["goals_per_game"] = df["goals"] / df["games"]
    df["assists_per_game"] = df["assists"] / df["games"]
    df["duels_win_percent"] = df["won"] / df["duels"] * 100

    df.loc[(df["dribble_percent"] > 40) &
           (df["fouls drawn per game"] > 1) &
           (df["penalty scored per game"] > 0.1),
           "player type"] = "dribbler"

    df.loc[(df["duels_win_percent"] > 0.3) &
           (df["goals"] > 10) &
           (df["assists_per_game"] > 0.3) &
           (df["penalty scored per game"] > 0.1),
           "player type"] = "target man"


extra_columns(df)


def plot_radars(df):
    ranks = df.copy()

    target_man_cols = ["duels_win_percent", "goals", "assists_per_game", "penalty scored per game"]
    dribbler_cols = ["dribble_percent", "fouls drawn per game", "penalty scored per game"]
    include = list(set(target_man_cols + dribbler_cols))
    print(include)

    # add up the rank for each of these columns
    ranks[include] = ranks[include].rank(method="dense", ascending=True)
    factor = len(df) / 10
    ranks[include] = ranks[include] / factor
    targetmen = ranks.loc[ranks["player type"] == "target man", include + ["name"]]
    targetmen["ranksum"] = targetmen[target_man_cols].sum(axis=1)
    dribblers = ranks.loc[ranks["player type"] == "dribbler", include + ["name"]]
    dribblers["ranksum"] = dribblers[dribbler_cols].sum(axis=1)

    targetmen = targetmen.sort_values("ranksum", ascending=False)
    dribblers = dribblers.sort_values("ranksum", ascending=False)

    top_target_man = targetmen.iloc[0]
    top_target_man_name = top_target_man["name"]
    top_target_man_values = top_target_man[include]
    top_dribbler = dribblers.iloc[0]
    top_dribbler_name = top_dribbler["name"]
    top_dribbler_values = top_dribbler[include]
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(targetmen)

    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    print(dribblers)
    print("################################")

    ranges = []
    targetman_value = []
    dribbler_value = []
    for p in include:
        a = min(df[p])
        a = a - (a * .25)

        b = max(df[p])
        b = b + (b * .25)

        # ranges.append((a, b))
        ranges.append((1, 10))

    print(ranges)

    T = dict(
        title_name=top_target_man_name,
        title_color='blue',
        subtitle_name='top target man',
        subtitle_color='blue',
        title_name_2=top_dribbler_name,
        title_color_2='red',
        subtitle_name_2='top dribbler',
        subtitle_color_2='red'
    )
    S1 = [top_target_man_values.to_list(), top_dribbler_values.to_list()]
    print(S1)

    plt.rcParams["font.family"] = "Arial"

    # Plotting the data
    radar = Radar(fontfamily="Arial", background_color="black", patch_color="#28252C", label_color="white",
                  range_color="#BFE9BF")
    fig, ax = radar.plot_radar(ranges=ranges, params=include, fontfamily="Arial",
                               values=S1, alphas=[0.76, 0.6],
                               title=T, endnote="hello there noe", radar_color=['#0f4c75', '#e94560'], compare=True)
    plt.show()



pandas.set_option('display.max_columns', None)
plot_radars(df)
1 / 0
params = ["goals_per_game", "assists_per_game", "duels_win_percent",
          "dribble_percent", "duels_win_percent", "penalty scored per game"]



pandas.set_option('display.max_columns', None)
print(df)
range()


# plot_radars(df)

def comparetogoals(df, y):
    ax = sns.scatterplot(df, x="goals", y=y, hue="name")
    plt.xlabel('Goals Scored')
    plt.ylabel(y)
    plt.title('Goals Scored vs Duels Won')

    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    plt.show()


def top_goals_assists(df):
    df.plot.bar(x="name", y=["goals", "assists"], figsize=(9, 8))
    plt.show()

