# check_cleaned_data.py
import pandas as pd
import numpy as np

# Read the cleaned data
df = pd.read_parquet("data_processed/clean/cleaned_data.parquet")

# Print basic info
print("\nDataset Info:")
print(f"Number of records: {len(df)}")
print(f"\nColumns: {df.columns.tolist()}")

# Print sample record
print("\nSample Record:")
sample = df.iloc[0]

# Print metadata
print("\nMetadata:")
metadata = sample['metadata']
for key, value in metadata.items():
    print(f"{key}: {value}")

# Print first few profiles
print("\nFirst 3 profiles:")
profiles = sample['profiles']
for i, profile in enumerate(profiles[:3], 1):
    print(f"\nProfile {i}:")
    for key, value in profile.items():
        print(f"{key}: {value}")