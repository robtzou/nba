from nba_api.stats.endpoints import CommonAllPlayers, CommonPlayerInfo
import pandas as pd
import time

# Step 1: Get active players for 2023-24 season
season = '2023-24'
all_players_df = CommonAllPlayers(is_only_current_season=1, season=season).get_data_frames()[0]
all_players_df = all_players_df[all_players_df['ROSTERSTATUS'] == 1][['PERSON_ID', 'DISPLAY_FIRST_LAST']]

draft_info_records = []
entry_methods_set = set()

def infer_entry_method(draft_year, draft_round, draft_number):
    if draft_year == 'Undrafted':
        return 'Undrafted'
    elif not draft_year or draft_year in ['0', '']:
        return 'International'
    elif draft_round == '1':
        return '1st Round Pick'
    elif draft_round == '2':
        return '2nd Round Pick'
    else:
        return 'Other Draft'

# Step 2: Loop through 2023-24 players and fetch draft info
for idx, row in all_players_df.iterrows():
    pid, name = row['PERSON_ID'], row['DISPLAY_FIRST_LAST']
    try:
        info = CommonPlayerInfo(player_id=pid).get_data_frames()[0].iloc[0]
    except Exception as e:
        print(f"❌ {name} ({pid}) error: {e}")
        continue

    draft_year = info.get('DRAFT_YEAR')
    draft_round = info.get('DRAFT_ROUND')
    draft_number = info.get('DRAFT_NUMBER')
    entry_method = infer_entry_method(draft_year, draft_round, draft_number)
    entry_methods_set.add(entry_method)

    draft_info_records.append({
        'player_id': pid,
        'player_name': name,
        'draft_year': draft_year,
        'draft_round': draft_round,
        'draft_number': draft_number,
        'entry_method': entry_method
    })

    if idx % 50 == 0:
        print(f"✅ Processed {idx} players")
    time.sleep(0.5)

# Step 3: Save draft method lookup
draft_methods = [{'draft_method_id': i+1, 'entry_method': em} for i, em in enumerate(sorted(entry_methods_set))]
df_draft_methods = pd.DataFrame(draft_methods)
df_draft_methods.to_csv("draft_methods.csv", index=False)
print("📄 Saved draft_methods.csv")

# Step 4: Save player draft info with method ID
method_map = {row['entry_method']: row['draft_method_id'] for _, row in df_draft_methods.iterrows()}
df_player_draft_info = pd.DataFrame(draft_info_records)
df_player_draft_info['draft_method_id'] = df_player_draft_info['entry_method'].map(method_map)
df_player_draft_info = df_player_draft_info[['player_id', 'player_name', 'draft_year', 'draft_round', 'draft_number', 'draft_method_id']]
df_player_draft_info.to_csv("player_draft_info.csv", index=False)
print("✅ Saved player_draft_info.csv")
