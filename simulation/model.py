import mesa
from simulation.agents.charging_station import ChargingStationAgent
from simulation.agents.car import CarAgent


class ChargingStationModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, N_cars, N_charging_stations, width, height):
        self.num_car_agents = N_cars
        self.num_charging_station_agents = N_charging_stations
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivationByType(self)
        self.running = True
        # Create car agents
        for i in range(self.num_car_agents):

            initial_battery_level = self.random.uniform(0.5, 1)
            full_battery_range = self.random.uniform(300, 600)
            target_battery_level = self.random.uniform(0.8, 1)
            alert_battery_level = self.random.uniform(0.15, 0.3)

            a = CarAgent(i, self, initial_battery_level, full_battery_range, target_battery_level, alert_battery_level)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        # Create charging station agents
        for i in range(self.num_charging_station_agents):
            number_of_charging_ports = 1

            a = ChargingStationAgent(i+N_cars, self, number_of_charging_ports)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
