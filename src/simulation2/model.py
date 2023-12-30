import mesa
import mesa_geo as mg
import shapely
import shapely.wkt as wkt
from .agents.centroid import CentroidAgent
from .agents.charging_station import ChargingStationAgent
from .agents.car import CarAgent


class ChargingStationModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, stations_data, centroids_data, N_charging_stations, distance_matrix_data):
        self.num_charging_station_agents = N_charging_stations
        self.distance_matrix_data = distance_matrix_data
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
        
        # Create car agents based on the centroids data
        for index, row in centroids_data.iterrows():
            for i in range(row["number_of_ev_cars"]):
                centroid = centroid_agents[row["OBJECTID"]]

                initial_battery_level = self.random.uniform(0.5, 1)
                full_battery_range = self.random.uniform(300, 600)
                target_battery_level = self.random.uniform(0.8, 1)
                alert_battery_level = self.random.uniform(0.15, 0.3)

                car = CarAgent(i, self, centroid, initial_battery_level, full_battery_range, target_battery_level, alert_battery_level)
                self.schedule.add(car)


    def step(self):
        """Advance the model by one step."""
        self.schedule.step()


    def find_optimal_charging_station(self, current_centroid_unique_id, max_distance, desireable_distance):
        # Since its a matrix we need to store the header
        header = self.distance_matrix_data.columns

        index = header.index(current_centroid_unique_id)
        
        distances = self.distance_matrix_data.iloc[index]

        # Remove distances greater than max_distance
        distances = distances[distances < max_distance]

        # Sort distances

        # Get nearest station that is free
        for centroid_id in distances.columns:
            # ... 

        
