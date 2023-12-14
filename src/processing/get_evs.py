import pandas as pd

# File paths
csv_file_path = '../../data/processed/centroids.csv'
sqm_file_path = '../../data/raw/sqm_price_per_place.csv'
output_file_path = 'evs.csv'

# Read the prices per place CSV file into a pandas DataFrame
sqm_df = pd.read_csv(sqm_file_path, encoding='utf-8')

# Read the centroids CSV file into a pandas DataFrame
centroids_df = pd.read_csv(csv_file_path, encoding='utf-8')

# Merge the two DataFrames on the common column 'DTMNFR21'
merged_df = pd.merge(centroids_df, sqm_df, on='DTMNFR21')

# Save the merged DataFrame to a new CSV file
merged_df.to_csv(output_file_path, index=False, encoding='utf-8')

print(f"The price per sqm has been added to {output_file_path}.")
