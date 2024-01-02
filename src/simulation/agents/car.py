import mesa
from src.utils.constants import Constants
from .charging_station import ChargingStationAgent
import os
import random

class CarAgent(mesa.Agent):
    """A car agent."""

    def __init__(self, unique_id, model, centroid, initial_battery_level, full_battery_range, target_battery_level, alert_battery_level, desireable_distance):
        super().__init__(unique_id, model)
        self.initial_centroid = centroid
        self.current_centroid = self.initial_centroid
        
        self.target_battery_level = target_battery_level  # In percentage [0, 1]
        self.alert_battery_level = alert_battery_level  # in percentage [0, 1]
        self.current_battery_level = initial_battery_level  # In percentage [0, 1]
        self.full_battery_range = full_battery_range  # In kilometers
        self.desireable_distance = desireable_distance  # In kilometers

        self.is_on_charging_station = False
        self.dead = False

        self.destination_charging_station = None
        self.remaining_distance_to_charging_station = 0
        
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
            self.kill()


    def move(self):
        """Move the car."""
        # Since each tick represents a minute, assuming a travel speed between 30km/h and 120km/h
        # each car should move between 0.5 and 2 km
        
        travel_distance = random.randrange(Constants.Simulation.CAR_MOVING_SPEED_MIN, Constants.Simulation.CAR_MOVING_SPEED_MAX) / 60  # In km/min
        self.travel(travel_distance)

        return travel_distance


    def find_charging_station(self):
        """Find a charging station."""
        result = self.model.find_optimal_charging_station(self.current_centroid.unique_id, self.calculate_current_range(), self.desireable_distance)
        
        if result is None:
            return

        charging_station, distance = result
        
        self.destination_charging_station = charging_station
        self.total_distance_to_charging_station = distance
        self.remaining_distance_to_charging_station = self.total_distance_to_charging_station
        self.current_centroid = None


    def kill(self):
        self.dead = True
        self.log_dead()


    def can_travel(self):
        """Check if the car can travel."""
        return not self.is_on_charging_station and self.current_battery_level > 0 and not self.dead
    

    def step(self):
        """Advance the agent by one step."""        
        pass
        if not self.can_travel():
            return
        
        # Check if the car is travelling towards a charging station
        if self.destination_charging_station is not None:
            travel_distance = self.move()
            self.remaining_distance_to_charging_station -= travel_distance

            # Check if the car has arrived at the charging station
            if self.remaining_distance_to_charging_station <= 0:
                self.current_centroid = self.destination_charging_station.centroid
                self.destination_charging_station.new_car_arrived(self, self.total_distance_to_charging_station)
                self.destination_charging_station = None
                self.total_distance_to_charging_station = 0

            return
                
        
        # Since cars are not always moving
        if random.random() < Constants.Simulation.CAR_MOVING_PROBABILITY:
            self.move()

        # Needs to find a charging station to charge
        if self.current_battery_level < self.alert_battery_level and self.destination_charging_station is None:
            print("Car {} needs to be charged.".format(self.unique_id))
            print("Current battery level: {}".format(self.current_battery_level))
            self.find_charging_station()

    def log_dead(self):
        """Log the car as dead."""
        with open(Constants.Logs.RAW_OUPUT_DEAD_CARS_FILE_PATH, "a") as file:
            file.write("{},{},{}\n".format(self.unique_id, self.model.schedule.time, self.current_battery_level))
