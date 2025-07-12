from nba_api.stats.endpoints import LeagueLeaders
import pandas as pd
import time

# Configuration
season = '2023-24'
top_n = 10  # Number of top players to include per stat
categories = {
    'PTS': 'Points Per Game',
    'AST': 'Assists Per Game',
    'REB': 'Rebounds Per Game',
    'STL': 'Steals Per Game',
    'BLK': 'Blocks Per Game',
    'FG_PCT': 'Field Goal %',
    'FG3_PCT': '3-Point %',
    'FT_PCT': 'Free Throw %',
}

# Storage for leaderboard data
top_players = []

print("📊 Fetching top performers from NBA API...")

for abbr, stat_name in categories.items():
    try:
        print(f"⏳ Getting leaders for: {stat_name}")
        leaders = LeagueLeaders(season=season, stat_category_abbreviation=abbr).get_data_frames()[0]
        top = leaders.head(top_n)
        for _, row in top.iterrows():
            top_players.append({
                'player_id': row['PLAYER_ID'],
                'player_name': row['PLAYER'],
                'team': row['TEAM'],
                'season': season,
                'stat_category': stat_name,
                'value': row[abbr]
            })
        time.sleep(0.6)  # Gentle delay to avoid throttling
    except Exception as e:
        print(f"❌ Error loading {stat_name}: {e}")

# Convert to DataFrame
df_top = pd.DataFrame(top_players)

# Save to CSV
filename = f"nba_top_performers_{season.replace('-', '_')}.csv"
df_top.to_csv(filename, index=False)
print(f"✅ Top performers saved to {filename}")
