from nba_api.stats.endpoints import playerindex
import pandas as pd

# Fetch player index data
pi = playerindex.PlayerIndex()
data = pi.get_data_frames()[0]

# Convert FROM_YEAR and TO_YEAR to numeric values
data["FROM_YEAR"] = pd.to_numeric(data["FROM_YEAR"], errors="coerce")
data["TO_YEAR"] = pd.to_numeric(data["TO_YEAR"], errors="coerce")

# Filter for players active in the 2023–24 season
active_2324 = data[(data["FROM_YEAR"] <= 2024) & (data["TO_YEAR"] >= 2023)]

# Create full name column
active_2324["FULL_NAME"] = active_2324["PLAYER_FIRST_NAME"] + " " + active_2324["PLAYER_LAST_NAME"]

# Select relevant columns
players_df = active_2324[["PERSON_ID", "FULL_NAME", "DRAFT_YEAR"]]

# Save to CSV
players_df.to_csv("nba_2023_24_players.csv", index=False)

print("🔥 Success! Saved as 'nba_2023_24_players.csv'")
