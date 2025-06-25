import pandas as pd
import glob
import os

# Path to folder containing your CSVs
folder_path = './nba_games'
output_file = 'nba_merged.csv'

# Get list of CSV files
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

all_data = []

for file in csv_files:
    df = pd.read_csv(file)
    
    # Extract season name from filename, e.g. 'nba_stats_2023-24.csv'
    season_id = os.path.splitext(os.path.basename(file))[0].split('_')[-1]
    df['Season_ID'] = season_id
    all_data.append(df)

# Merge all CSVs
merged_df = pd.concat(all_data, ignore_index=True)

# Save to one CSV
merged_df.to_csv(output_file, index=False)
print(f"Merged CSV saved to {output_file}")
