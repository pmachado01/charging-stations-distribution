from src.utils.constants import Constants
import src.utils.files as Files
import matplotlib.pyplot as plt
import os


class ChargeRecord:
    """A charging record."""

    def __init__(self, car_id, car_centroid, charging_station_name, charging_station_centroid, travelled_distance, time_spent_travelling, arrival_time, initial_battery_level, final_battery_level, start_time, end_time):
        self.car_id = car_id
        self.car_centroid = car_centroid
        self.charging_station_name = charging_station_name
        self.charging_station_centroid = charging_station_centroid
        self.travelled_distance = travelled_distance
        self.time_spent_travelling = time_spent_travelling
        self.arrival_time = arrival_time
        self.initial_battery_level = initial_battery_level
        self.final_battery_level = final_battery_level
        self.start_time = start_time
        self.end_time = end_time


def extract_data_charging_records(charging_records_data):
    # Extract data into a dictionary
    charging_records_dict = {}  # {car_id: [ChargeRecord]
    for index, row in charging_records_data.iterrows():
        car_id = row["car_id"]
        car_centroid = row["car_centroid"]
        charging_station_name = row["charging_station_name"]
        charging_station_centroid = row["charging_station_centroid"]
        travelled_distance = row["travelled_distance"]
        arrival_time = row["arrival_time"]
        initial_battery_level = row["initial_battery_level"]
        final_battery_level = row["final_battery_level"]
        start_time = row["start_time"]
        end_time = row["end_time"]

        charging_record = ChargeRecord(car_id, car_centroid, charging_station_name, charging_station_centroid, travelled_distance, arrival_time, initial_battery_level, final_battery_level, start_time, end_time)

        if car_id not in charging_records_dict:
            charging_records_dict[car_id] = []
        charging_records_dict[car_id].append(charging_record)

    return charging_records_dict


def calculate_single_metrics(charging_records_dict):
    # Calculate travel distance to charging station, time spent travelling to charging station and time spent waiting for a charging port
    average_travelled_distance = {} # {car_id: average_travelled_distance}
    average_time_spent_waiting = {} # {car_id: average_time_spent_waiting}
    
    for car_id, charging_records in charging_records_dict.items():
        total_travelled_distance = 0
        total_time_spent_travelling = 0
        total_time_spent_waiting = 0

        for charging_record in charging_records:
            total_travelled_distance += charging_record.travelled_distance
            total_time_spent_travelling += charging_record.time_spent_travelling
            total_time_spent_waiting += charging_record.start_time - charging_record.arrival_time

        average_travelled_distance[car_id] = total_travelled_distance / len(charging_records)
        average_time_spent_waiting[car_id] = total_time_spent_waiting / len(charging_records)

    return average_travelled_distance, average_time_spent_waiting


def calculate_global_metrics(charging_records_dict):
    # Calculate total average travel distance to charging station and time spent waiting for a charging port for all cars
    total_average_travelled_distance = 0
    total_average_time_spent_waiting = 0

    for car_id, charging_records in charging_records_dict.items():
        for charging_record in charging_records:
            total_average_travelled_distance += charging_record.travelled_distance
            total_average_time_spent_waiting += charging_record.start_time - charging_record.arrival_time

    total_average_travelled_distance /= len(charging_records_dict)
    total_average_time_spent_waiting /= len(charging_records_dict)
    
    return total_average_travelled_distance, total_average_time_spent_waiting


def plot_average_travelled_distance(average_travelled_distance):
    # Plotting
    plt.figure(figsize=(10, 6))

    temp_average_travelled_distance = {}
    for car_id, distance in average_travelled_distance.items():
        if distance > 0:
            temp_average_travelled_distance[car_id] = distance
    
    
    # Extract car IDs and distances
    car_ids = list(temp_average_travelled_distance.keys())
    distances = list(temp_average_travelled_distance.values())
    
    # Use bar plot with car IDs on x-axis
    plt.bar(range(len(car_ids)), distances)
    
    plt.xlabel('Car ID')
    plt.ylabel('Average Travelled Distance (km)')
    plt.title('Average Travelled Distance to Charging Station')
    
    # Set x-axis ticks to be car IDs
    plt.xticks(range(len(car_ids)), car_ids, rotation=45)
    
    plt.tight_layout()
    plt.savefig(Constants.Graphs.AVERAGE_TRAVELLED_DISTANCE_GRAPH_FILE_PATH)


def plot_average_time_spent_waiting(average_time_spent_waiting):
    # Plotting
    plt.figure(figsize=(10, 6))

    temp_average_time_spent_waiting = {}
    for car_id, time_spent in average_time_spent_waiting.items():
        if time_spent > 0:
            temp_average_time_spent_waiting[car_id] = time_spent
    
    # Extract car IDs and time spent waiting
    car_ids = list(temp_average_time_spent_waiting.keys())
    time_spent_waiting = list(temp_average_time_spent_waiting.values())
    
    # Use bar plot with car IDs on x-axis
    plt.bar(range(len(car_ids)), time_spent_waiting)
    
    plt.xlabel('Car ID')
    plt.ylabel('Average Time Spent Waiting (minutes)')
    plt.title('Average Time Spent Waiting for a Charging Port')
    
    # Set x-axis ticks to be car IDs
    plt.xticks(range(len(car_ids)), car_ids, rotation=45)
    
    plt.tight_layout()
    plt.savefig(Constants.Graphs.AVERAGE_TIME_SPENT_WAITING_GRAPH_FILE_PATH)


def save_charging_records(charging_records_dict, average_travelled_distance, average_time_spent_waiting, total_average_travelled_distance, total_average_time_spent_waiting):
    # Delete the file if it already exists
    if os.path.exists(Constants.Logs.OUPUT_CHARGING_RECORDS_FILE_PATH):
        os.remove(Constants.Logs.OUPUT_CHARGING_RECORDS_FILE_PATH)

    # Save results to file
    with open(Constants.Logs.OUPUT_CHARGING_RECORDS_FILE_PATH, "w") as file:
        file.write("car_id,average_travelled_distance,average_time_spent_waiting\n")
        for car_id, charging_records in charging_records_dict.items():
            file.write("{},{},{},{}\n".format(car_id, average_travelled_distance[car_id], average_time_spent_waiting[car_id]))
        file.write("total,{},{},{}\n".format(total_average_travelled_distance, total_average_time_spent_waiting))


def extract_data_dead_cars(dead_cars_data):
    # Extract data into a dictionary
    dead_cars_dict = {} # {car_id: [(timestamp, battery_level)]}
    for index, row in dead_cars_data.iterrows():
        car_id = row["car_id"]
        timestamp = row["timestamp"]
        battery_level = row["battery_level"]

        if car_id not in dead_cars_dict:
            dead_cars_dict[car_id] = [(timestamp, battery_level)]
        else:
            dead_cars_dict[car_id].append((timestamp, battery_level))

    return dead_cars_dict


def calculate_average_battery_level(dead_cars_dict):
    # Calculate average battery level for each car
    average_battery_level = {} # {car_id: average_battery_level}
    for car_id, values in dead_cars_dict.items():
        battery_level_sum = 0
        for value in values:
            battery_level_sum += value[1]
        average_battery_level[car_id] = battery_level_sum / len(values)
    
    return average_battery_level


def plot_average_battery_level(average_battery_level):
    # Plotting
    plt.figure(figsize=(10, 6))
    
    # Extract car IDs and average battery level
    car_ids = list(average_battery_level.keys())
    battery_levels = list(average_battery_level.values())
    
    # Use bar plot with car IDs on x-axis
    plt.bar(range(len(car_ids)), battery_levels)
    
    plt.xlabel('Car ID')
    plt.ylabel('Average Battery Level (%)')
    plt.title('Average Battery Level of Dead Cars')
    
    # Set x-axis ticks to be car IDs
    plt.xticks(range(len(car_ids)), car_ids, rotation=45)
    
    plt.tight_layout()
    plt.savefig(Constants.Graphs.AVERAGE_BATTERY_LEVEL_GRAPH_FILE_PATH)


def plot_average_timestamp_to_die(dead_cars_dict):
    # Plotting
    plt.figure(figsize=(10, 6))
    
    # Extract car IDs and average timestamp to die
    car_ids = list(dead_cars_dict.keys())
    timestamps_to_die = [dead_cars_dict[car_id][0][0] for car_id in car_ids]
    
    # Use bar plot with car IDs on x-axis
    plt.bar(range(len(car_ids)), timestamps_to_die)
    
    plt.xlabel('Car ID')
    plt.ylabel('Average Timestamp to Die (ticks)')
    plt.title('Average Timestamp for Dead Cars')
    
    # Set x-axis ticks to be car IDs
    plt.xticks(range(len(car_ids)), car_ids, rotation=45)
    
    plt.tight_layout()
    plt.savefig(Constants.Graphs.AVERAGE_TIMESTAMP_TO_DIE_GRAPH_FILE_PATH)



def save_dead_cars(average_battery_level):
    # Delete the file if it already exists
    if os.path.exists(Constants.Logs.OUPUT_DEAD_CARS_FILE_PATH):
        os.remove(Constants.Logs.OUPUT_DEAD_CARS_FILE_PATH)

    # Save results to file
    with open(Constants.Logs.OUPUT_DEAD_CARS_FILE_PATH, "w") as file:
        file.write("car_id,average_battery_level\n")
        for car_id, battery_level in average_battery_level.items():
            file.write("{},{}\n".format(car_id, battery_level))


def main():
    ##########################################################
    # Analyse the data on charging records
    charging_records_file_path = Constants.Logs.OUPUT_CHARGING_RECORDS_FILE_PATH
    
    # Read charging records file
    charging_records_data = Files.read_csv_file(charging_records_file_path)

    # Extract data into a dictionary
    charging_records_dict = extract_data_charging_records(charging_records_data)

    # Calculate single metrics for each car
    average_travelled_distance, average_time_spent_waiting = calculate_single_metrics(charging_records_dict)

    # Calculate global metrics for all cars
    total_average_travelled_distance, total_average_time_spent_waiting = calculate_global_metrics(charging_records_dict)

    # Draw a line chart of the average travel distance to charging station, time spent travelling to charging station and time spent waiting for a charging port for each car
    # Draw a bar chart of the total average travel distance to charging station, time spent travelling to charging station and time spent waiting for a charging port for all cars
    plot_average_travelled_distance(average_travelled_distance)
    plot_average_time_spent_waiting(average_time_spent_waiting)

    # Save results to file
    save_charging_records(charging_records_dict, average_travelled_distance, average_time_spent_waiting, total_average_travelled_distance, total_average_time_spent_waiting)

    ##########################################################
    # Analyse the data on dead cars
    dead_cars_file_path = Constants.Logs.OUPUT_DEAD_CARS_FILE_PATH

    # Read dead cars file
    dead_cars_data = Files.read_csv_file(dead_cars_file_path)

    # Extract data into a dictionary
    dead_cars_dict = extract_data_dead_cars(dead_cars_data)

    # Calculate average battery level for each car
    average_battery_level = calculate_average_battery_level(dead_cars_dict)

    # Draw a bar chart of the average battery level for each car
    plot_average_battery_level(average_battery_level)

    # Draw a bar chart of the average timetamp for each car to die
    plot_average_timestamp_to_die(dead_cars_dict)

    # Save results to file
    save_dead_cars(average_battery_level)


if __name__ == "__main__":
    main()
