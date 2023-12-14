import mesa
from simulation.agents.charging_station import ChargingStationAgent


class CarAgent(mesa.Agent):
    """A car agent."""

    def __init__(self, unique_id, model, initial_battery_level, full_battery_range, target_battery_level, alert_battery_level):
        super().__init__(unique_id, model)
        
        self.target_battery_level = target_battery_level  # In percentage [0, 1]
        self.alert_battery_level = alert_battery_level  # in percentage [0, 1]
        self.current_battery_level = initial_battery_level  # In percentage [0, 1]
        self.full_battery_range = full_battery_range  # In kilometers

        self.can_travel = True
        self.is_on_charging_station = False
        
    def calculate_current_range(self):
        """Calculate the current range of the car."""
        return self.current_battery_level / 100 * self.full_battery_range        
    
    def calculate_required_charging_time(self, charging_station):
        """Calculate the required charging time (in minutes) for the car at the given charging station."""
        charging_power = charging_station.charging_power / 60  # In km/min

        return self.calculate_required_charging_energy() / charging_power  # In minutes
    
    def calculate_required_charging_energy(self):
        """Calculate the required charging energy for the car at the given charging station."""
        return self.full_battery_range - self.calculate_current_range()  # In kilometers

    def charge(self, distance):
        """Charge the car for the given distance."""
        self.current_battery_level += distance / self.full_battery_range

    def can_travel(self, distance):
        """Check if the car can travel the given distance."""
        return self.calculate_current_range() >= distance

    def travel(self, distance):
        """Travel the given distance."""        
        self.current_battery_level -= distance / self.full_battery_range
        
        if self.current_battery_level < 0:
            self.current_battery_level = 0

    def move(self):
        """Move the car to a random adjacent cell."""
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

        self.travel(10)  # Travel 10 km

    def find_charging_station(self):
        """Find a charging station."""
        charging_stations = self.model.schedule.agents_by_type[ChargingStationAgent]
        charging_stations = list(charging_stations.values())
        print(type(charging_stations))
        print("Number of charging stations: {}".format(len(charging_stations)))
        # Find random charging station
        charging_station = self.random.choice(charging_stations)

        print(charging_station)

        charging_station.new_car_arrived(self)

    def can_travel(self):
        """Check if the car can travel."""
        return not self.is_on_charging_station and self.current_battery_level > 0

    def step(self):
        """Advance the agent by one step."""
        if not self.can_travel():
            return
        
        self.move()

        if self.current_battery_level < self.alert_battery_level:
            print("Car {} needs to be charged.".format(self.unique_id))
            print("Current battery level: {}".format(self.current_battery_level))
            self.find_charging_station()    
