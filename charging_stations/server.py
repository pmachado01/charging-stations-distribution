import mesa
import solara
from model import MoneyModel
from matplotlib.figure import Figure

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}
    if agent.wealth > 0:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    return portrayal



grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)
chart = mesa.visualization.ChartModule(
[{"Label": "Gini", "Color": "Black"}], data_collector_name="datacollector"
)


server = mesa.visualization.ModularServer(MoneyModel,
                                          [grid, chart],
                                          "Charging Station Model",
                                          {'N': 100, 'width': 10, 'height': 10})
server.port = 8521  # The default
#server.launch()
