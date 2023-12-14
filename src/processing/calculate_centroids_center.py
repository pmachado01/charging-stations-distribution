from src.utils.constants import Constants
import src.utils.files as Files
from shapely.ops import cascaded_union
from shapely.wkt import loads
import argparse


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
    centroids_file_path = Files.get_processed_file_path(args.centroids_file)

    # Read centroids file
    centroids_data = Files.read_csv_file(centroids_file_path)

    # Iterate through each centroid
    for centroid in centroids_data:
        # Extract the geometric center
        center_x, center_y = extract_geometric_center(centroid["WKT"])

        # Add the geometric center to the centroid
        centroid["lon"] = center_x
        centroid["lat"] = center_y

    # Write centroids file
    Files.write_csv_file(centroids_file_path, centroids_data)

    print(f"Geometric centers have been added to {centroids_file_path}.")