from ..utils.constants import Constants
import src.utils.files as Files
import mesa
import mesa_geo as mg
from .agents.charging_station import ChargingStationAgent
from .agents.car import CarAgent
from .agents.centroid import CentroidAgent
from .model import ChargingStationModel
import os

#TODO: Improve agent colors
def agent_portrayal(agent):
    if isinstance(agent, ChargingStationAgent):
        portrayal = {"Filled": "true",
                     "Layer": 0,
                     "r": 0.5}
        usage = agent.get_usage()
        if usage > 0.8:
            portrayal["color"] = "red"
        elif usage > 0.5:
            portrayal["color"] = "orange"
        elif usage > 0.2:
            portrayal["color"] = "yellow"
        else:
            portrayal["color"] = "green"
    elif isinstance(agent, CentroidAgent):
        portrayal = {"color": "Blue"}
    else:
        portrayal = {"color": "gray"}

    return portrayal

# Reset the output files
if os.path.exists(Constants.Logs.OUPUT_CHARGING_RECORDS_FILE_PATH):
    os.remove(Constants.Logs.OUPUT_CHARGING_RECORDS_FILE_PATH)
with open(Constants.Logs.OUPUT_CHARGING_RECORDS_FILE_PATH, "w") as file:
    file.write("car_id,car_centroid,charging_station_name,charging_station_centroid,travelled_distance,time_spent_travelling,arrival_time,initial_battery_level,final_battery_level,start_time,end_time\n")

if os.path.exists(Constants.Logs.OUPUT_STATIONS_FILE_PATH):
    os.remove(Constants.Logs.OUPUT_STATIONS_FILE_PATH)
with open(Constants.Logs.OUPUT_STATIONS_FILE_PATH, "w") as file:
    file.write("charging_station_name,timestamp,usage\n")

if os.path.exists(Constants.Logs.OUPUT_DEAD_CARS_FILE_PATH):
    os.remove(Constants.Logs.OUPUT_DEAD_CARS_FILE_PATH)
with open(Constants.Logs.OUPUT_DEAD_CARS_FILE_PATH, "w") as file:
    file.write("car_id,timestamp,battery_level\n")


stations_file_path = Constants.Data.PROCESSED_STATIONS_FILE_PATH
stations_data = Files.read_csv_file(stations_file_path)

centroids_file_path = Constants.Data.PROCESSED_CENTROIDS_FILE_PATH
centroids_data = Files.read_csv_file(centroids_file_path)

#TODO: Add non retilinea path factor
distance_matrix_file_path = Constants.Data.DISTANCE_MATRIX_FILE_PATH
distance_matrix_data = Files.read_csv_file(distance_matrix_file_path)

map_element = mg.visualization.MapModule(agent_portrayal, [41.17, -8.61], 12, 800, 500)

model_params = {
    "stations_data": stations_data,
    "centroids_data": centroids_data,
    "N_charging_stations": len(stations_data),
    "distance_matrix_data" : distance_matrix_data
}

server = mesa.visualization.ModularServer(ChargingStationModel,
                                          [map_element],
                                          "Charging Station Model",
                                          model_params)
server.port = 8521  # The default
