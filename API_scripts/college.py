from nba_api.stats.endpoints import commonallplayers, commonplayerinfo
import pandas as pd
import time

# Step 1: Get all players for 2023–24
players_response = commonallplayers.CommonAllPlayers(
    season='2023-24',
    league_id='00',
    
)
df_all = players_response.get_data_frames()[0]

# Step 2: Filter to active players only
active_players = df_all[df_all['ROSTERSTATUS'] == 1]

# Step 3: Loop through and get college info using CommonPlayerInfo
player_list = []
for idx, row in active_players.iterrows():
    player_id = row['PERSON_ID']
    name = row['DISPLAY_FIRST_LAST']

    try:
        info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        player_data = info.get_data_frames()[0]
        college = player_data.at[0, 'SCHOOL']
    except Exception as e:
        print(f"Error fetching data for {name} ({player_id}): {e}")
        college = None

    player_list.append({
        'Player_ID': player_id,
        'Name': name,
        'School': college
    })

    print(f"✔️ {name} | {college}")
    time.sleep(0.6)  # Delay to avoid rate-limiting

# Step 4: Save or use
df_final = pd.DataFrame(player_list)
df_final.to_csv("nba_2023_24_player_colleges.csv", index=False)
print(df_final.head())