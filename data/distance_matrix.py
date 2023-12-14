import pandas as pd
import geopy.distance
from scipy.spatial.distance import pdist, squareform

# Read the CSV file
csv_file_path = './processed/centroids.csv'  # Update with your CSV file path
output_file_path = 'distance_matrix.csv'


id_column_name = 'BGRI2021'
lon_column_name = 'lon'
lat_column_name = 'lat'

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path, encoding='utf-8')

coordinates = df[[lat_column_name, lon_column_name]]

# Calculate the Haversine distance matrix
num_points = len(coordinates)
distance_matrix = [[geopy.distance.geodesic((coordinates.iloc[i][lat_column_name], coordinates.iloc[i][lon_column_name]),
                              (coordinates.iloc[j][lat_column_name], coordinates.iloc[j][lon_column_name])).km
                    for j in range(num_points)] for i in range(num_points)]

# Create a list of IDs
index = list(df[id_column_name])[:num_points]
# Create a DataFrame from the distance matrix
distance_df = pd.DataFrame(distance_matrix, index=index, columns=index)

# Display the resulting distance matrix DataFrame
print(distance_df)

# Save the distance matrix DataFrame to a CSV file
distance_df.to_csv(output_file_path, index=False, encoding='utf-8')
