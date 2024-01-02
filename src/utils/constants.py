import os

class Constants:
    class Data:  # Data constants
        RAW_DATA_PATH = os.path.join("data", "raw")
        PROCESSED_DATA_PATH = os.path.join("data", "processed")
        PROCESSED_CENTROIDS_FILE_NAME = "centroids.csv"
        PROCESSED_STATIONS_FILE_NAME = "stations.csv"
        DISTANCE_MATRIX_FILE_NAME = "distance_matrix.csv"
        PROCESSED_CENTROIDS_FILE_PATH = os.path.join(PROCESSED_DATA_PATH, PROCESSED_CENTROIDS_FILE_NAME)
        PROCESSED_STATIONS_FILE_PATH = os.path.join(PROCESSED_DATA_PATH, PROCESSED_STATIONS_FILE_NAME)
        DISTANCE_MATRIX_FILE_PATH = os.path.join(PROCESSED_DATA_PATH, DISTANCE_MATRIX_FILE_NAME)

    class Logs:
        RAW_OUPUT_STATIONS_FILE_PATH = "logs/stations.csv"
        PROCESSED_OUPUT_STATIONS_FILE_PATH = "logs/processed_stations.csv"
        PROCESSED_OUPUT_TOTAL_STATIONS_FILE_PATH = "logs/processed_total_stations.csv"
        RAW_OUPUT_CHARGING_RECORDS_FILE_PATH = "logs/charging_records.csv"
        PROCESSED_OUPUT_CHARGING_RECORDS_FILE_PATH = "logs/processed_charging_records.csv"
        RAW_OUPUT_DEAD_CARS_FILE_PATH = "logs/dead_cars.csv"
        PROCESSED_OUPUT_DEAD_CARS_FILE_PATH = "logs/processed_dead_cars.csv"

    class Graphs:
        GRAPHS_FOLDER_PATH = "logs/graphs"
        STATIONS_USAGE_GRAPH1_FILE_PATH = "logs/graphs/stations_usage1_graph.png"
        STATIONS_USAGE_GRAPH2_FILE_PATH = "logs/graphs/stations_usage2_graph.png"
        STATIONS_TOTAL_USAGE_GRAPH_FILE_PATH = "logs/graphs/stations_total_usage_graph.png"
        AVERAGE_TIME_SPENT_WAITING_GRAPH_FILE_PATH = "logs/graphs/average_time_spent_waiting_graph.png"
        AVERAGE_TRAVELLED_DISTANCE_GRAPH_FILE_PATH = "logs/graphs/average_travelled_distance_graph.png"
        AVERAGE_TIME_SPENT_TRAVELLING_GRAPH_FILE_PATH = "logs/graphs/average_time_spent_travelling_graph.png"
        TOTAL_AVERAGE_TRAVELLED_DISTANCE_GRAPH_FILE_PATH = "logs/graphs/total_average_travelled_distance_graph.png"
        TOTAL_AVERAGE_TIME_SPENT_TRAVELLING_GRAPH_FILE_PATH = "logs/graphs/total_average_time_spent_travelling_graph.png"
        TOTAL_AVERAGE_TIME_SPENT_WAITING_GRAPH_FILE_PATH = "logs/graphs/total_average_time_spent_waiting_graph.png"
        AVERAGE_BATTERY_LEVEL_GRAPH_FILE_PATH = "logs/graphs/average_battery_level_graph.png"
        AVERAGE_TIMESTAMP_TO_DIE_GRAPH_FILE_PATH = "logs/graphs/average_timestamp_to_die_graph.png"

    class Simulation:
        INITIAL_BATTERY_LEVEL_MIN   = 0.5  # In percentage
        INITIAL_BATTERY_LEVEL_MAX   = 1.0  # In percentage
        FULL_BATTERY_RANGE_MIN      = 300  # In km
        FULL_BATTERY_RANGE_MAX      = 700  # In km
        TARGET_BATTERY_LEVEL_MIN    = 0.8  # In percentage
        TARGET_BATTERY_LEVEL_MAX    = 1    # In percentage
        ALERT_BATTERY_LEVEL_MIN     = 0.15 # In percentage
        ALERT_BATTERY_LEVEL_MAX     = 0.3  # In percentage
        STATION_CHARGING_POWER      = 500  # In km/h
        CAR_MOVING_PROBABILITY      = 0.82 # Probability of the car moving in each step of the simulation
        CAR_MOVING_SPEED_MIN        = 30   # In km/h
        CAR_MOVING_SPEED_MAX        = 120  # In km/h
        DESIRABLE_DISTANCE_MIN      = 2    # In km
        DESIRABLE_DISTANCE_MAX      = 5    # In km