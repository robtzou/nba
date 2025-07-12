from nba_api.stats.endpoints import CommonAllPlayers, PlayerAwards
import pandas as pd
import time

# Step 1: Get players active in the 2023-24 season
season = '2023-24'
players_df = CommonAllPlayers(is_only_current_season=1, season=season).get_data_frames()[0]
players_df = players_df[players_df['ROSTERSTATUS'] == 1][['PERSON_ID', 'DISPLAY_FIRST_LAST']]

# Step 2: Loop through each player and pull awards for 2023-24
award_rows = []

print("📦 Gathering awards for 2023–24 players...")

for idx, row in players_df.iterrows():
    player_id = row['PERSON_ID']
    name = row['DISPLAY_FIRST_LAST']

    try:
        awards_data = PlayerAwards(player_id=player_id).get_data_frames()[0]
        awards_2023 = awards_data[awards_data['SEASON'] == '2023-24']
    except Exception as e:
        print(f"❌ {name} ({player_id}) error: {e}")
        continue

    for _, a_row in awards_2023.iterrows():
        award_rows.append({
            'player_id': player_id,
            'player_name': name,
            'season': '2023-24',
            'description': a_row['DESCRIPTION']
        })

    if idx % 50 == 0:
        print(f"✅ Processed {idx} players")
    time.sleep(0.5)

# Step 3: Save to CSV
df_awards = pd.DataFrame(award_rows)
df_awards.to_csv("player_awards_2023_24.csv", index=False)
print("🏆 Saved player_awards_2023_24.csv")
