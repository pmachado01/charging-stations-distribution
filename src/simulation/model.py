import mesa
from .agents.charging_station import ChargingStationAgent
from .agents.car import CarAgent


class ChargingStationModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, stations_data, centroids_data, N_cars, N_charging_stations, width, height):
        self.num_car_agents = N_cars
        self.num_charging_station_agents = N_charging_stations
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivationByType(self)
        self.running = True

        # Create a temporary dictionary to hold the number of cars per centroid
        centroids_dict = {}
        for index, row in centroids_data.iterrows():
            centroids_dict[row["SECSSNUM21"]] = row["number_of_ev_cars"]
        
        # Create car agents based on the centroids data
        for i in range(self.num_car_agents):
            centroid = self.random.choice(list(centroids_dict.keys()))
            centroids_dict[centroid] -= 1
            if centroids_dict[centroid] == 0:
                del centroids_dict[centroid]

            initial_battery_level = self.random.uniform(0.5, 1)
            full_battery_range = self.random.uniform(300, 600)
            target_battery_level = self.random.uniform(0.8, 1)
            alert_battery_level = self.random.uniform(0.15, 0.3)

            a = CarAgent(i, self, centroid, initial_battery_level, full_battery_range, target_battery_level, alert_battery_level)

            self.schedule.add(a)

            # TODO: Add the car to its centroid's grid cell
            
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        # Create charging station agents based on the stations data
        for i in range(self.num_charging_station_agents):
            name = stations_data.iloc[i]["name"]
            latitude = stations_data.iloc[i]["latitude"]
            longitude = stations_data.iloc[i]["longitude"]
            number_of_charging_ports = stations_data.iloc[i]["chargers"]
            centroid = stations_data.iloc[i]["nearest_centroid"]

            a = ChargingStationAgent(i+N_cars, self, name, latitude, longitude, number_of_charging_ports, centroid)
            self.schedule.add(a)
            
            # TODO: Add the charging station to its centroid's grid cell

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
