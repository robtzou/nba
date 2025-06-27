from nba_api.stats.endpoints import leaguedashplayerstats, commonplayerinfo
import pandas as pd
import time

def get_season_averages(season='2023-24'):
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        season_type_all_star='Regular Season',
        per_mode_detailed='PerGame'
    )
    df = stats.get_data_frames()[0]
    return df

def enrich_with_player_info(player_ids):
    enriched_data = []
    for pid in player_ids:
        try:
            info = commonplayerinfo.CommonPlayerInfo(player_id=pid)
            df = info.get_data_frames()[0]
            enriched_data.append({
                'PLAYER_ID': pid,
                'COUNTRY': df.at[0, 'COUNTRY'],
                'POSITION': df.at[0, 'POSITION'],
                'TEAM_NAME': df.at[0, 'TEAM_NAME'],
                'NICKNAME': df.at[0, 'PLAYER_SLUG'],
            })
        except Exception as e:
            print(f"Failed for PLAYER_ID {pid}: {e}")
        time.sleep(0.6)  # Avoid rate limiting
    return pd.DataFrame(enriched_data)

def merge_stats_and_info(season='2023-24'):
    print("Pulling season averages...")
    stats_df = get_season_averages(season)
    player_ids = stats_df['PLAYER_ID'].unique()
    
    print("Enriching with metadata...")
    info_df = enrich_with_player_info(player_ids)

    print("Merging...")
    merged = pd.merge(stats_df, info_df, on='PLAYER_ID', how='left')
    return merged

if __name__ == "__main__":
    season = '2023-24'
    final_df = merge_stats_and_info(season)
    final_df.to_csv(f'nba_player_stats_with_meta_{season.replace("-", "")}.csv', index=False)
    print("Done. File saved.")
