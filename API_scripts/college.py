from nba_api.stats.endpoints import CommonAllPlayers, CommonPlayerInfo
import pandas as pd
import time

# Step 1: Get all active players in the 2023-24 season
common_all = CommonAllPlayers(is_only_current_season=1, league_id='00', season='2023-24')
df_players = common_all.get_data_frames()[0]

# Step 2: For each player, fetch their college via CommonPlayerInfo
player_college = []

for idx, row in df_players.iterrows():
    pid = row['PERSON_ID']
    name = row['DISPLAY_FIRST_LAST']
    
    try:
        info = CommonPlayerInfo(player_id=pid).get_data_frames()[0]
        college = info.loc[0, 'SCHOOL']
    except Exception as e:
        college = 'Unavailable'
        print(f"Error fetching info for {name} (ID: {pid}): {e}")
    
    player_college.append({
        'Player ID': pid,
        'Player Name': name,
        'College': college
    })
    
    time.sleep(0.6)  # Respect rate limits

# Step 3: Convert to DataFrame
df_colleges = pd.DataFrame(player_college)

# Step 4: Dump to CSV
csv_file = 'nba_players_colleges_2023_24.csv'
df_colleges.to_csv(csv_file, index=False)

print(f"\nData dumped successfully to {csv_file}")
from nba_api.stats.endpoints import CommonAllPlayers, CommonPlayerInfo
import pandas as pd
import time

# Step 1: Get all active players in 2023-24
common_all = CommonAllPlayers(is_only_current_season=1, league_id='00', season='2023-24')
df_players = common_all.get_data_frames()[0]  # Contains PLAYER_ID and DISPLAY_FIRST_LAST

# Step 2: For each player, fetch their college via CommonPlayerInfo
player_college = []

for idx, row in df_players.iterrows():
    pid = row['PERSON_ID']
    name = row['DISPLAY_FIRST_LAST']
    info = CommonPlayerInfo(player_id=pid).get_data_frames()[0]
    college = info.loc[0, 'SCHOOL']  # College field
    player_college.append({'player_id': pid, 'player_name': name, 'college': college})
    time.sleep(0.6)  # be a good citizen and respect rate limits

# Step 3: Convert to DataFrame
df_colleges = pd.DataFrame(player_college)

print(df_colleges.head())
