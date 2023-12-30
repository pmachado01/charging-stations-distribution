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
        portrayal = {"color": "Red"}
    elif isinstance(agent, CentroidAgent):
        portrayal = {"color": "Blue"}
    elif isinstance(agent, CarAgent):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "color": "red",
                     "r": 0.5}
        if agent.current_battery_level > agent.alert_battery_level:
            portrayal["color"] = "green"
        else:
            portrayal["color"] = "red"
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

total_ev_cars = 0
for index, row in centroids_data.iterrows():
        total_ev_cars += int(row["number_of_ev_cars"])

map_element = mg.visualization.MapModule(agent_portrayal, [41.17, -8.61], 12, 800, 500)

model_params = {
    "stations_data": stations_data,
    "centroids_data": centroids_data,
    "N_cars": total_ev_cars,
    "N_charging_stations": len(stations_data)
}

server = mesa.visualization.ModularServer(ChargingStationModel,
                                          [map_element],
                                          "Charging Station Model",
                                          model_params)
server.port = 8521  # The default
