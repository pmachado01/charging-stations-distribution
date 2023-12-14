from src.utils.constants import Constants
import src.utils.files as Files
from shapely.ops import cascaded_union
from shapely.wkt import loads
import argparse
import os

WKT_GEOM_COLUMN_NAME = 'WKT'


def extract_geometric_center(wkt_str):
    """
    Extract the geometric center of a Multipolygon
    """
    multipolygon = loads(wkt_str)
    center_point = cascaded_union(multipolygon).centroid
    return center_point.x, center_point.y


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("centroids_file", help="Centroids file name")
    args = arg_parser.parse_args()

    # Get the centroids file path
    centroids_file_path = Files.get_raw_file_path(args.centroids_file)

    # Read centroids file
    centroids_data = Files.read_csv_file(centroids_file_path)

    # Iterate through each centroid of the DataFrame
    for index, row in centroids_data.iterrows():
        # Extract the geometric center of the Multipolygon
        x, y = extract_geometric_center(row[WKT_GEOM_COLUMN_NAME])

        # Add the new columns to the DataFrame
        centroids_data.at[index, "lon"] = x
        centroids_data.at[index, "lat"] = y

    # Write centroids file
    save_location = Constants.Data.PROCESSED_DATA_PATH
    save_filename = Constants.Data.PROCESSED_CENTROIDS_FILE_NAME
    save_path = os.path.join(save_location, save_filename)
    Files.write_csv_file(save_path, centroids_data)


if __name__ == "__main__":
    main()
