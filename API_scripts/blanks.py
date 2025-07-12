import pandas as pd
import numpy as np

# Create a sample DataFrame with null values
df = pd.DataFrame({'A': [1, 2, np.nan, 4],
                   'B': [5, np.nan, 7, 8],
                   'C': [9, 10, 11, np.nan]})

# Replace all NaN values in the DataFrame with 0
df_filled = df.fillna(0)

print("Original DataFrame:")
print(df)
print("\nDataFrame after replacing NaN with 0:")
print(df_filled)