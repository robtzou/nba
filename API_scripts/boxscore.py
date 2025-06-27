from nba_api.stats.endpoints import leaguegamefinder, boxscoretraditionalv2
import pandas as pd
import time

def get_game_ids_for_season(season='2023-24', season_type='Regular Season'):
    gamefinder = leaguegamefinder.LeagueGameFinder(
        season_nullable=season,
        season_type_nullable=season_type
    )
    games_df = gamefinder.get_data_frames()[0]
    return games_df['GAME_ID'].unique()

def get_boxscores(game_ids, delay=1.0):
    all_boxscores = []

    for i, game_id in enumerate(game_ids):
        try:
            boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
            df = boxscore.player_stats.get_data_frame()
            df['GAME_ID'] = game_id
            all_boxscores.append(df)
        except Exception as e:
            print(f"Failed to get boxscore for {game_id}: {e}")
        time.sleep(delay)  # Avoid rate limiting

        if (i + 1) % 50 == 0:
            print(f"{i + 1} games processed...")

    return pd.concat(all_boxscores, ignore_index=True)

if __name__ == "__main__":
    season = '2023-24'
    print("Fetching game IDs...")
    game_ids = get_game_ids_for_season(season)

    print(f"Found {len(game_ids)} games. Fetching box scores...")
    all_data = get_boxscores(game_ids)

    output_file = f'nba_boxscores_{season.replace("-", "")}.csv'
    all_data.to_csv(output_file, index=False)
    print(f"Saved all box scores to {output_file}")
