import pandas as pd
import numpy as np

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('data_10000_tuples.csv', header=None, names=['Source IP', 'Destination IP', 'Source Port', 'Destination Port', 'Protocol'])

# Shuffle the DataFrame row indices
shuffled_indices = np.random.permutation(df.index)

# Define the group size (100 tuples per group)
group_size = 100

# Create a list to store shuffled groups
shuffled_groups = []

# Iterate through the shuffled indices in groups of group_size
for i in range(0, len(shuffled_indices), group_size):
    # Get a group of indices
    group_indices = shuffled_indices[i:i+group_size]
    # Get the corresponding rows from the DataFrame and shuffle them
    shuffled_group = df.iloc[group_indices].sample(frac=1)
    # Append the shuffled group to the list
    shuffled_groups.append(shuffled_group)

# Concatenate the shuffled groups back into a single DataFrame
shuffled_df = pd.concat(shuffled_groups)

# Write the shuffled DataFrame to a new CSV file
shuffled_df.to_csv('shuffled_data_10000.csv', index=False)
