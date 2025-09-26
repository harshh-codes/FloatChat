# -*- coding: utf-8 -*-
import pandas as pd
import glob

# Print Parquet file info
print("Parquet files:")
parquet_files = glob.glob("data_processed/parquet/*.parquet")
print(f"\nTotal files: {len(parquet_files)}")
print("\nSample file contents:")
if parquet_files:
    df = pd.read_parquet(parquet_files[0])
    print(f"\nColumns: {df.columns.tolist()}")
    print("\nFirst row:")
    print(df.iloc[0].to_dict())