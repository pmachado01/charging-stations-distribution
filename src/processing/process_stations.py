from ..utils.constants import Constants
import src.utils.files as Files
import pandas as pd
import sys
from geopy import distance
import argparse
import os


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points in kilometers
    """
    return distance.distance((lat1, lon1), (lat2, lon2)).km


def find_nearest_centroid(lat, lon, centroids):
    """
    Find the nearest centroid
    """
    # Initialize the minimum distance
    min_distance = sys.maxsize

    # Initialize the nearest centroid
    nearest_centroid = None

    # Iterate through each centroid
    for centroid in centroids.values():
        # Calculate the distance between the station and the centroid
        distance = calculate_distance(lat, lon, centroid["lat"], centroid["lon"])  # TODO: Verify in csv file the header names

        # Check if the distance is less than the minimum distance
        if distance < min_distance:
            # Update the minimum distance
            min_distance = distance

            # Update the nearest centroid
            nearest_centroid = centroid

    return nearest_centroid["OBJECTID"]


def associate_stations_with_centroids(data, centroids):
    """
    Associate each station with the nearest centroid
    """
    # Iterate through each station
    for station in data["stations"]:
        # Find the nearest centroid
        nearest_centroid = find_nearest_centroid(station["latitude"], station["longitude"], centroids)

        # Add the nearest centroid to the station
        station["nearest_centroid"] = nearest_centroid


def filter_stations_data(data):
    """
    Process the data
    """

    # Remove duplicate stations using the "nameAndStreetSlug" attribute
    df = pd.DataFrame(data["stations"])
    df = df.drop_duplicates(subset="nameAndStreetSlug")
    data["stations"] = df.to_dict(orient="records")

    # Process each station
    for station in data["stations"]:
        # Remove specified attributes
        station.pop("typeId", None)
        station.pop("nameAndStreetSlug", None)
        station.pop("address", None)
        station.pop("typeName", None)

        # Calculate total number of connectors
        total_connectors = sum(connector["total"] for connector in station["connectors"])

        # Remove 'connectors' attribute
        station.pop("connectors", None)

        # Add new attribute 'chargers'
        station["chargers"] = total_connectors

        # Remove commas from the 'name' attribute
        station["name"] = station["name"].replace(",", "")


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("stations_file", help="Stations file name")
    args = arg_parser.parse_args()

    # Read the stations file location from the command line
    stations_file_path = Files.get_raw_file_path(args.stations_file)

    # Read the centroids file location from the command line
    centroids_filename = Constants.Data.PROCESSED_CENTROIDS_FILE_NAME
    centroids_file_path = Files.get_processed_file_path(centroids_filename)

    # Read stations file
    stations_data = Files.read_json_file(stations_file_path)

    # Read centroids file
    centroids_data = Files.read_csv_file(centroids_file_path)
    centroids_data = centroids_data.to_dict(orient="index")

    # Filter stations data
    filter_stations_data(stations_data)

    # Associate each station with the nearest centroid
    associate_stations_with_centroids(stations_data, centroids_data)

    # Save the modified data
    save_location = Constants.Data.PROCESSED_DATA_PATH
    save_filename = Constants.Data.PROCESSED_STATIONS_FILE_NAME
    save_path = os.path.join(save_location, save_filename)
    Files.write_csv_file(save_path, stations_data["stations"])


if __name__ == "__main__":
    main()
