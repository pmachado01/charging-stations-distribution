from ..utils.constants import Constants
import src.utils.files as Files
import mesa
from .model import ChargingStationModel, CarAgent, ChargingStationAgent
import os

def agent_portrayal(agent):
    if isinstance(agent, CarAgent):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "red",
                     "r": 0.5}
        if agent.current_battery_level > agent.alert_battery_level:
            portrayal["Color"] = "green"
        else:
            portrayal["Color"] = "red"

    elif isinstance(agent, ChargingStationAgent):
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "green",
                     "w": 1,
                     "h": 1}
        if len(agent.waiting_cars) > 0:
            portrayal["Color"] = "red"
        elif len(agent.charging_cars) > 0:
            portrayal["Color"] = "yellow"
        else:
            portrayal["Color"] = "blue"
    else:
        portrayal = None

    return portrayal

# Reset the output files
if os.path.exists(Constants.Data.RAW_OUPUT_CHARGING_RECORDS_FILE_PATH):
    os.remove(Constants.Data.RAW_OUPUT_CHARGING_RECORDS_FILE_PATH)
with open(Constants.Data.RAW_OUPUT_CHARGING_RECORDS_FILE_PATH, "w") as file:
    file.write("car_id,car_centroid,charging_station_name,charging_station_centroid,travelled_distance,time_spent_travelling,arrival_time,initial_battery_level,final_battery_level,start_time,end_time\n")

if os.path.exists(Constants.Data.RAW_OUPUT_STATIONS_FILE_PATH):
    os.remove(Constants.Data.RAW_OUPUT_STATIONS_FILE_PATH)
with open(Constants.Data.RAW_OUPUT_STATIONS_FILE_PATH, "w") as file:
    file.write("charging_station_name,timestamp,usage\n")

if os.path.exists(Constants.Data.RAW_OUPUT_DEAD_CARS_FILE_PATH):
    os.remove(Constants.Data.RAW_OUPUT_DEAD_CARS_FILE_PATH)
with open(Constants.Data.RAW_OUPUT_DEAD_CARS_FILE_PATH, "w") as file:
    file.write("car_id,timestamp,battery_level\n")


stations_file_path = Constants.Data.PROCESSED_STATIONS_FILE_PATH
stations_data = Files.read_csv_file(stations_file_path)

centroids_file_path = Constants.Data.PROCESSED_CENTROIDS_FILE_PATH
centroids_data = Files.read_csv_file(centroids_file_path)

total_ev_cars = 0
for index, row in centroids_data.iterrows():
        total_ev_cars += int(row["number_of_ev_cars"])

grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)

model_params = {
    "stations_data": stations_data,
    "centroids_data": centroids_data,
    "N_cars": total_ev_cars,
    "N_charging_stations": len(stations_data),
    "width": 10,
    "height": 10
}

server = mesa.visualization.ModularServer(ChargingStationModel,
                                          [grid],
                                          "Charging Station Model",
                                          model_params)
server.port = 8521  # The default
