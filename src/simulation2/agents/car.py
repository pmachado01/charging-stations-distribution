import mesa
from src.utils.constants import Constants
from .charging_station import ChargingStationAgent
import os

class CarAgent(mesa.Agent):
    """A car agent."""

    def __init__(self, unique_id, model, centroid, initial_battery_level, full_battery_range, target_battery_level, alert_battery_level):
        super().__init__(unique_id, model)
        self.centroid = centroid
        
        self.target_battery_level = target_battery_level  # In percentage [0, 1]
        self.alert_battery_level = alert_battery_level  # in percentage [0, 1]
        self.current_battery_level = initial_battery_level  # In percentage [0, 1]
        self.full_battery_range = full_battery_range  # In kilometers

        self.is_on_charging_station = False
        self.dead = False

        self.destination_charging_station = None
        self.travelled_distance_to_charging_station = 0
        self.start_time_searching_charging_station = None
        
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

    def travel(self, distance):
        """Travel the given distance."""        
        self.current_battery_level -= distance / self.full_battery_range
        
        if self.current_battery_level < 0:
            self.current_battery_level = 0

    def move(self):
        """Move the car to a random adjacent cell or to the charging station."""
        self.travel(5)  # Travel 5 km

    def find_charging_station(self):
        """Find a charging station."""
        #TODO: New way to find the charging station
        
        charging_stations = self.model.schedule.agents_by_type[ChargingStationAgent]
        charging_stations = list(charging_stations.values())
        
        # Find random charging station TODO: Find the nearest charging station
        charging_station = self.random.choice(charging_stations)

        # TODO: Set the distance to the charging station
        distance_to_charging_station = 0.3
        if distance_to_charging_station > self.calculate_current_range():
            #print("Car {} cannot reach the charging station.".format(self.unique_id))
            self.kill()
            return
        
        self.destination_charging_station = charging_station
        self.start_time_searching_charging_station = self.model.schedule.time


    def kill(self): 
        self.dead = True
        self.log_dead()


    def can_travel(self):
        """Check if the car can travel."""
        return not self.is_on_charging_station and self.current_battery_level > 0 and not self.dead
    

    def step(self):
        """Advance the agent by one step."""
        if not self.can_travel():
            return
        
        #TODO: Find some way to avoid the car from being always on travel
        self.move()

        if self.current_battery_level < self.alert_battery_level and self.destination_charging_station is None:
            #print("Car {} needs to be charged.".format(self.unique_id))
            #print("Current battery level: {}".format(self.current_battery_level))
            self.find_charging_station()

    def log_dead(self):
        """Log the car as dead."""
        with open(Constants.Logs.OUPUT_DEAD_CARS_FILE_PATH, "a") as file:
            file.write("{},{},{}\n".format(self.unique_id, self.model.schedule.time, self.current_battery_level))
