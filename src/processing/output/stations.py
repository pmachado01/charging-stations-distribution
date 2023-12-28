from src.utils.constants import Constants
import src.utils.files as Files
import matplotlib.pyplot as plt
import os

def extract_data(stations_data):
    # Extract data into a dictionary
    stations_usage_dict = {} # {station_id: {timestamp: usage}}
    for index, row in stations_data.iterrows():
        station_id = row["charging_station_name"]
        timestamp = row["timestamp"]
        usage = row["usage"]

        if station_id not in stations_usage_dict:
            stations_usage_dict[station_id] = {timestamp: usage}
        else:
            stations_usage_dict[station_id][timestamp] = usage

    return stations_usage_dict


def calculate_usage(stations_usage_dict):
    # Calculate average usage for each station
    stations_usage = {} # {station_id: usage}
    for station_id in stations_usage_dict:
        usage_sum = 0
        for timestamp in stations_usage_dict[station_id]:
            usage_sum += float(stations_usage_dict[station_id][timestamp])
        stations_usage[station_id] = usage_sum / len(stations_usage_dict[station_id])

    return stations_usage


def calculate_total_average_usage(stations_usage_dict):
    # Calculate average usage across all stations
    total_usage = {} # {timestamp: usage}
    for station_id, usage_data in stations_usage_dict.items():
        for timestamp, usage in usage_data.items():
            if timestamp not in total_usage:
                total_usage[timestamp] = float(usage)
            else:
                total_usage[timestamp] += float(usage)
    for timestamp in total_usage:
        total_usage[timestamp] /= len(stations_usage_dict)
    
    return total_usage



def plot_usage_1(stations_usage_dict):
    # Plotting
    plt.figure(figsize=(12, 8))

    for station_id, usage_data in stations_usage_dict.items():
        timestamps, usage_values = zip(*sorted(usage_data.items()))
        plt.plot(timestamps, usage_values)

    plt.xlabel('Timestamp')
    plt.ylabel('Average Usage')
    plt.title('Usage of Charging Stations Over Time')
    plt.ylim(0, 1)
    #plt.legend(stations_usage_dict.keys(), loc='lower right')
    plt.tight_layout()
    plt.savefig(Constants.Graphs.STATIONS_USAGE_GRAPH1_FILE_PATH)


def plot_usage_2(stations_usage):
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(stations_usage.keys(), stations_usage.values())
    plt.xlabel('Charging Station Name')
    plt.ylabel('Average Usage')
    plt.title('Average Usage of Charging Stations')
    plt.ylim(0, 1)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(Constants.Graphs.STATIONS_USAGE_GRAPH2_FILE_PATH)


def plot_total_usage(total_usage):
    plt.figure(figsize=(12, 8))
    timestamps, usage_values = zip(*sorted(total_usage.items()))
    plt.plot(timestamps, usage_values)
    plt.xlabel('Timestamp')
    plt.ylabel('Average Usage')
    plt.title('Average Usage of Charging Stations')
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(Constants.Graphs.STATIONS_TOTAL_USAGE_GRAPH_FILE_PATH)


def save_per_station(stations_usage):
    """Save the records to the file."""
    # Write stations usage to file
    with open(Constants.Data.PROCESSED_OUPUT_STATIONS_FILE_PATH, "w") as file:
        file.write("charging_station_name,usage\n")

        for station_id in stations_usage:
            file.write("{},{}\n".format(station_id, stations_usage[station_id]))


def save_total(total_usage):
    """Save the records to the file."""
    # Delete the file if it exists
    if os.path.exists(Constants.Data.PROCESSED_OUPUT_TOTAL_STATIONS_FILE_PATH):
        os.remove(Constants.Data.PROCESSED_OUPUT_TOTAL_STATIONS_FILE_PATH)
    
    # Write stations usage to file
    with open(Constants.Data.PROCESSED_OUPUT_TOTAL_STATIONS_FILE_PATH, "w") as file:
        file.write("timestamp,usage\n")

        for timestamp in total_usage:
            file.write("{},{}\n".format(timestamp, total_usage[timestamp]))
        file.write("total,{}\n".format(sum(total_usage.values())/len(total_usage)))   


def main():
    stations_file_path = Constants.Data.RAW_OUPUT_STATIONS_FILE_PATH

    # Read stations file
    stations_data = Files.read_csv_file(stations_file_path)

    # Extract data into a dictionary
    stations_usage_dict = extract_data(stations_data)

    # Calculate usage
    stations_usage = calculate_usage(stations_usage_dict)

    # Calculate average usage across all stations
    total_usage = calculate_total_average_usage(stations_usage_dict)    
    
    # Draw a line chart of the usage of each station
    plot_usage_1(stations_usage_dict)
    plot_usage_2(stations_usage)

    # Draw a bar chart of the average usage across all stations
    plot_total_usage(total_usage)

    # Save the records to the file
    save_per_station(stations_usage)
    save_total(total_usage)


if __name__ == "__main__":
    main()
