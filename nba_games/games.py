from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import Season, SeasonType
import pandas as pd

num = 11
years = ['2011-12','2012-13','2013-14','2014-15','2015-16','2016-17', '2017-18','2018-19','2019-20','2020-21','2021-22','2022-23',]

def get_all_season_games(season=years[num], season_type='Regular Season'):
    """
    Get all games for a specific NBA season
    
    Parameters:
    - season: String format like '2023-24', '2022-23', etc.
    - season_type: 'Regular Season', 'Playoffs', 'Pre Season', or 'All Star'
    
    Returns:
    - DataFrame with all games
    """
    
    gamefinder = leaguegamefinder.LeagueGameFinder(
        season_nullable=season,
        season_type_nullable=season_type
    )
    
    games_df = gamefinder.get_data_frames()[0]
    
    return games_df

if __name__ == "__main__":
    season = years[num]
    df = get_all_season_games(season)
    print(df.head())  # Show top 5 rows
    df.to_csv(f'nba_season_stats_{season.replace("-", "")}.csv', index=False)