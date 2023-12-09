import mesa
from model import ChargingStationModel, CarAgent, ChargingStationAgent


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


grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)

model_params = {
    "N_cars": 15,
    "N_charging_stations": 3,
    "width": 10,
    "height": 10
}

server = mesa.visualization.ModularServer(ChargingStationModel,
                                          [grid],
                                          "Charging Station Model",
                                          model_params)
server.port = 8521  # The default
