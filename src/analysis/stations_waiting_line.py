from src.utils.constants import Constants
import src.utils.files as Files
import matplotlib.pyplot as plt
import os

def extract_data(stations_data):
    # Extract data into a dictionary
    stations_waiting_cars_dict = {} # {station_id: {timestamp: waiting_cars}}
    for index, row in stations_data.iterrows():
        station_id = row["charging_station_name"]
        timestamp = row["timestamp"]
        waiting_cars = row["waiting_cars"]

        if station_id not in stations_waiting_cars_dict:
            stations_waiting_cars_dict[station_id] = {}
        stations_waiting_cars_dict[station_id][timestamp] = waiting_cars

    return stations_waiting_cars_dict


def plot_per_station(average_waiting_cars):
    # Draw a bar chart of the average waiting cars for each station
    plt.bar(average_waiting_cars.keys(), average_waiting_cars.values())        
    plt.xlabel("Timestamp")
    plt.ylabel("Waiting cars")
    plt.title("Average waiting cars for each station")
    plt.legend()
    plt.savefig(Constants.Graphs.STATIONS_WAITING_CARS_GRAPH_FILE_PATH)


def plot_total(total_waiting_cars):
    # Draw a bar chart of the average waiting cars between all stations
    plt.bar(["Average waiting cars"], [total_waiting_cars])
    plt.xlabel("Average waiting cars")
    plt.title("Average waiting cars between all stations")
    plt.savefig(Constants.Graphs.TOTAL_STATIONS_WAITING_CARS_GRAPH_FILE_PATH)


def save_per_station(average_waiting_cars):
    # Delete the file if it already exists
    if os.path.exists(Constants.Logs.PROCESSED_OUPUT_STATIONS_WAITING_CARS_FILE_PATH):
        os.remove(Constants.Logs.PROCESSED_OUPUT_STATIONS_WAITING_CARS_FILE_PATH)

    # Save the records to the file
    with open(Constants.Logs.PROCESSED_OUPUT_STATIONS_WAITING_CARS_FILE_PATH, "w", encoding="utf-8") as file:
        file.write("station_id,average_waiting_cars\n")
        for station_id in average_waiting_cars: # {station_id: average_waiting_cars}
            file.write("{},{}\n".format(station_id, average_waiting_cars[station_id]))



def save_total(total_waiting_cars):
    # Delete the file if it already exists
    if os.path.exists(Constants.Logs.PROCESSED_OUPUT_TOTAL_STATIONS_WAITING_CARS_FILE_PATH):
        os.remove(Constants.Logs.PROCESSED_OUPUT_TOTAL_STATIONS_WAITING_CARS_FILE_PATH)
        
    # Save the records to the file
    with open(Constants.Logs.PROCESSED_OUPUT_TOTAL_STATIONS_WAITING_CARS_FILE_PATH, "w", encoding="utf-8") as file:
        file.write("average_waiting_cars\n")
        file.write("{}\n".format(total_waiting_cars))


def main():
    stations_waiting_cars_file_path = Constants.Logs.RAW_OUPUT_STATIONS_WAITING_CARS_FILE_PATH

    # Read stations file
    stations_data = Files.read_csv_file(stations_waiting_cars_file_path)

    # Extract data into a dictionary
    stations_waiting_cars_dict = extract_data(stations_data)

    # Calculate average waiting cars for each station
    average_waiting_cars = {} # {station_id: average_waiting_cars}
    for station_id in stations_waiting_cars_dict:
        total_waiting_cars = 0
        for timestamp in stations_waiting_cars_dict[station_id]:
            total_waiting_cars += stations_waiting_cars_dict[station_id][timestamp]
        average_waiting_cars[station_id] = total_waiting_cars / len(stations_waiting_cars_dict[station_id])
    
    # Calculate average waiting cars between all stations
    total_waiting_cars = 0
    for station_id in average_waiting_cars:
        total_waiting_cars += average_waiting_cars[station_id]
    total_waiting_cars /= len(average_waiting_cars)

    # Draw a bar chart of the average waiting cars for each station
    plot_per_station(average_waiting_cars)

    # Draw a bar chart of the average waiting cars between all stations
    plot_total(total_waiting_cars)

    # Save the records to the file
    save_per_station(average_waiting_cars)
    save_total(total_waiting_cars)


if __name__ == "__main__":
    main()
