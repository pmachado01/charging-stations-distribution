import json
from geopy import distance
import sys
import pandas as pd


def read_stations_file_location():
    """
    Read the stations file location from the command line
    """
    # Read the file location from the command line
    stations_file_location = sys.argv[1]

    return stations_file_location


def read_centroids_file_location():
    """
    Read the centroids file location from the command line
    """
    # Read the file location from the command line
    centroids_file_location = sys.argv[2]

    return centroids_file_location


def check_file_exists(file_location):
    """
    Check if the file exists
    """
    try:
        # Open the file
        with open(file_location, 'r') as file:
            file.read()
    except FileNotFoundError:
        print("File not found")
        sys.exit(1)


def read_file(file_location):
    """
    Read data from the file
    """
    # Open the file
    with open(file_location, 'r') as file:
        data = file.read()

    return data


def read_csv_file(file_location):
    """
    Read data from the csv file
    """
    # Read the csv file
    data = pd.read_csv(file_location)

    # Convert the data to a dictionary
    data = data.to_dict(orient="index")

    return data


def process_data(data):
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


def save_data(data):
    """
    Save the modified data back to the file
    """
    with open('modified_stations.json', 'w') as file:
        json.dump(data, file, indent=2)


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
        distance = calculate_distance(lat, lon, centroid["lat"], centroid["lon"]) #TODO: Verify in csv file the header names

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
        print("Starting station: " + station["name"])
        # Find the nearest centroid
        nearest_centroid = find_nearest_centroid(station["latitude"], station["longitude"], centroids)

        # Add the nearest centroid to the station
        station["nearest_centroid"] = nearest_centroid

        print("Nearest centroid: " + str(nearest_centroid))
        print("Ending station: " + station["name"])

def main():
    """
    Main function
    """
    if len(sys.argv) != 3:
        print("Usage: python process.py <stations_file_location> <centroids_file_location>")
        sys.exit(1)

    # Read the stations file location from the command line
    stations_file_location = read_stations_file_location()

    # Read the centroids file location from the command line
    centroids_file_location = read_centroids_file_location()

    # Check if the stations file exists
    check_file_exists(stations_file_location)

    # Check if the centroids file exists
    check_file_exists(centroids_file_location)

    # Read data from the stations file
    stations_data = read_file(stations_file_location)

    # Load JSON data
    stations_data = json.loads(stations_data)

    # Process the data
    process_data(stations_data)

    # Read data from the centroids file
    centroids_data = read_csv_file(centroids_file_location)

    # Associate each station with the nearest centroid
    associate_stations_with_centroids(stations_data, centroids_data)

    # Save the modified data
    save_data(stations_data)


if __name__ == "__main__":
    main()