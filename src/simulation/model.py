import mesa
import mesa_geo as mg
import shapely
import shapely.wkt as wkt
from .agents.centroid import CentroidAgent
from .agents.charging_station import ChargingStationAgent
from .agents.car import CarAgent
from ..utils.constants import Constants



class ChargingStationModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, stations_data, centroids_data, N_charging_stations, distance_matrix_data):
        self.num_charging_station_agents = N_charging_stations
        self.distance_matrix_data = distance_matrix_data
        self.space = mg.GeoSpace()
        self.schedule = mesa.time.RandomActivationByType(self)
        self.running = True

        ac = mg.AgentCreator(CentroidAgent, self, crs="epsg:4326")

        self.centroid_agents = {}

        # Create centroid agents based on the centroids data
        for index, row in centroids_data.iterrows():
            geometry = wkt.loads(row["WKT"])
            centroid = ac.create_agent(geometry=geometry, unique_id=row["OBJECTID"])
            #self.space.add_agents(centroid)
            self.schedule.add(centroid)
            self.centroid_agents[row["OBJECTID"]] = centroid
        
        # Create charging station agents based on the stations data
        for index, row in stations_data.iterrows():
            # Create geometry circle with small radius
            geometry = shapely.geometry.Point(row["longitude"], row["latitude"]).buffer(0.0003)
            centroid = self.centroid_agents[row["nearest_centroid"]]
            number_of_charging_ports = 3
            charging_station = ChargingStationAgent(row["name"], self, geometry, "epsg:4326", centroid, number_of_charging_ports)
            
            centroid.add_station(charging_station)
            #self.space.add_agents(charging_station)
            self.schedule.add(charging_station)
        
        # Create car agents based on the centroids data
        for index, row in centroids_data.iterrows():
            for i in range(int(row["number_of_ev_cars"])):
                centroid = self.centroid_agents[row["OBJECTID"]]

                initial_battery_level = self.random.uniform(Constants.Simulation.INITIAL_BATTERY_LEVEL_MIN, Constants.Simulation.INITIAL_BATTERY_LEVEL_MAX)
                full_battery_range = self.random.uniform(Constants.Simulation.FULL_BATTERY_RANGE_MIN, Constants.Simulation.FULL_BATTERY_RANGE_MAX)
                target_battery_level = self.random.uniform(Constants.Simulation.TARGET_BATTERY_LEVEL_MIN, Constants.Simulation.TARGET_BATTERY_LEVEL_MAX)
                alert_battery_level = self.random.uniform(Constants.Simulation.ALERT_BATTERY_LEVEL_MIN, Constants.Simulation.ALERT_BATTERY_LEVEL_MAX)
                desireable_distance = self.random.uniform(Constants.Simulation.DESIRABLE_DISTANCE_MIN, Constants.Simulation.DESIRABLE_DISTANCE_MAX)

                car = CarAgent(f'car_{row["OBJECTID"]}_{i}', self, centroid, initial_battery_level, full_battery_range, target_battery_level, alert_battery_level, desireable_distance)
                self.schedule.add(car)

        #TODO: Remove this
        print("Number of centroid agents: {}".format(len(self.centroid_agents)))
        print("Number of charging station agents: {}".format(len(self.schedule.agents_by_type[ChargingStationAgent])))
        print("Number of car agents: {}".format(len(self.schedule.agents_by_type[CarAgent])))
        total_population = 234438
        print("Number of stations/100k people: {}".format(len(self.schedule.agents_by_type[ChargingStationAgent]) / (total_population / 100000)))
              

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()


    def find_optimal_charging_station(self, current_centroid_unique_id, max_distance, desireable_distance):
        # Get the head of the distance matrix into a list
        distance_matrix_head = self.distance_matrix_data.columns.tolist()

        # Get the index of the current centroid in the distance matrix
        current_centroid_index = distance_matrix_head.index(str(current_centroid_unique_id))
        
        # Get the distances from the current centroid to all the other centroids
        distances = self.distance_matrix_data.iloc[current_centroid_index]

        # Remove distances greater than max_distance
        distances = distances[distances < max_distance]
        if len(distances) == 0:
            return None

        # Sort distances
        distances.sort_values(inplace=True)

        # Get nearest station that is free
        for centroid, distance in distances.items():
            # If the distance is greater than the desireable distance, break and return the nearest station
            if distance > desireable_distance:
                break

            centroid_agent = self.centroid_agents[int(centroid)]
            charging_station = centroid_agent.get_available_charging_station()

            # If it found a free charging station with a distance less than the desireable distance, return it
            if charging_station is not None:
                return charging_station, distance
        
        
        # If it didn't find a free charging station with a distance less than the desireable distance, return the nearest station
        for centroid, distance in distances.items():
            centroid_agent = self.centroid_agents[int(centroid)]
            charging_station = centroid_agent.get_charging_station()

            if charging_station is not None:
                return charging_station, distance
        
        return None
        