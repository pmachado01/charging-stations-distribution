import mesa
import mesa_geo as mg
import shapely
import shapely.wkt as wkt
from .agents.centroid import CentroidAgent
from .agents.charging_station import ChargingStationAgent


class ChargingStationModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, stations_data, centroids_data, N_cars, N_charging_stations):
        self.num_car_agents = N_cars
        self.num_charging_station_agents = N_charging_stations
        self.space = mg.GeoSpace()
        self.schedule = mesa.time.RandomActivationByType(self)
        self.running = True

        ac = mg.AgentCreator(CentroidAgent, self, crs="epsg:4326")
        ac_station = mg.AgentCreator(ChargingStationAgent, self, crs="epsg:4326")

        # Create centroid agents based on the centroids data
        for index, row in centroids_data.iterrows():
            geometry = wkt.loads(row["WKT"])
            centroid = ac.create_agent(geometry=geometry, unique_id=index)
            self.space.add_agents(centroid)
            self.schedule.add(centroid)
        
        # Create charging station agents based on the stations data
        for index, row in stations_data.iterrows():
            # Create geometry circle with small radius
            geometry = shapely.geometry.Point(row["longitude"], row["latitude"]).buffer(0.0005)
            charging_station = ac_station.create_agent(geometry=geometry, unique_id=-index-1)
            self.space.add_agents(charging_station)
            self.schedule.add(charging_station)


    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
