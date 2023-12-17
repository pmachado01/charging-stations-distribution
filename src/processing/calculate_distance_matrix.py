from src.utils.constants import Constants
import src.utils.files as Files
import pandas as pd
import geopy.distance
import os

id_column_name = 'BGRI2021'
lon_column_name = 'lon'
lat_column_name = 'lat'


def main():
    # Get the centroids file path
    centroids_file_path = Files.get_processed_file_path(Constants.Data.PROCESSED_CENTROIDS_FILE_NAME)

    # Read centroids file
    centroids_data = Files.read_csv_file(centroids_file_path)

    # Get the coordinates
    coordinates = centroids_data[[lon_column_name, lat_column_name]]

    # Calculate the Haversine distance matrix
    num_points = len(coordinates)
    distance_matrix = [[geopy.distance.geodesic((coordinates.iloc[i][lat_column_name],
                                                 coordinates.iloc[i][lon_column_name]),
                                                (coordinates.iloc[j][lat_column_name],
                                                 coordinates.iloc[j][lon_column_name])).km
                        for j in range(num_points)] for i in range(num_points)]
    
    # Create a list of IDs
    index = list(centroids_data[id_column_name])[:num_points]
    
    # Create a DataFrame from the distance matrix
    distance_df = pd.DataFrame(distance_matrix, index=index, columns=index)

    # Save the distance matrix DataFrame to a CSV file
    save_location = Constants.Data.PROCESSED_DATA_PATH
    save_filename = Constants.Data.DISTANCE_MATRIX_FILE_NAME
    save_path = os.path.join(save_location, save_filename)
    Files.write_csv_file(save_path, distance_df)


if __name__ == "__main__":
    main()
