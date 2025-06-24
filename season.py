from nba_api.stats.endpoints import leaguedashplayerstats
import pandas as pd
import time

"query pull for players database"

num = 9
years = ['2011-12','2012-13','2013-14','2014-15','2015-16','2016-17','2018-19','2019-20','2021-22','2022-23',]

def get_season_stats(season=years[0], season_type='Regular Season'):
    # Delay to avoid rate-limiting
    time.sleep(1)
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        season_type_all_star=season_type
    )
    df = stats.get_data_frames()[0]
    return df

if __name__ == "__main__":
    season = years[num]
    df = get_season_stats(season)
    print(df.head())  # Show top 5 rows
    df.to_csv(f'nba_player_stats_{season.replace("-", "")}.csv', index=False)
