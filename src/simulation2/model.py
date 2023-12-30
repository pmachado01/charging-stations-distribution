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

        centroid_agents = {}

        # Create centroid agents based on the centroids data
        for index, row in centroids_data.iterrows():
            geometry = wkt.loads(row["WKT"])
            centroid = ac.create_agent(geometry=geometry, unique_id=row["OBJECTID"])
            self.space.add_agents(centroid)
            self.schedule.add(centroid)
            centroid_agents[row["OBJECTID"]] = centroid
        
        # Create charging station agents based on the stations data
        for index, row in stations_data.iterrows():
            # Create geometry circle with small radius
            geometry = shapely.geometry.Point(row["longitude"], row["latitude"]).buffer(0.0003)
            number_of_charging_ports = row["chargers"]
            charging_station = ChargingStationAgent(row["name"], self, geometry, "epsg:4326", number_of_charging_ports)
            centroid_agents[row["nearest_centroid"]].add_station(charging_station)
            self.space.add_agents(charging_station)
            self.schedule.add(charging_station)

        # TODO: Create car agents based on the centroids data


    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
