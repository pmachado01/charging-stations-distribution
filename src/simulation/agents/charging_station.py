import mesa
import mesa_geo as mg
from src.utils.constants import Constants
import os

class ChargeRecord:
    """A charging record."""

    def __init__(self, car, charging_station, travelled_distance, arrival_time):
        self.car = car
        self.initial_battery_level = car.current_battery_level
        self.final_battery_level = None
        self.charging_station = charging_station
        self.travelled_distance = travelled_distance
        self.arrival_time = arrival_time
        self.start_time = None
        self.end_time = None

    def start_charging(self, timestamp):
        """Start charging the car."""
        self.start_time = timestamp

    def end_charging(self, timestamp):
        """End charging the car."""
        self.end_time = timestamp
        self.final_battery_level = self.car.current_battery_level
        self.log_charging_record()

    def log_charging_record(self):
        """Log the charging record."""
        with open(Constants.Logs.RAW_OUPUT_CHARGING_RECORDS_FILE_PATH, "a", encoding="utf-8") as file:
            file.write("{},{},{},{},{},{},{},{},{},{}\n".format(self.car.unique_id,
                                                             self.car.current_centroid.unique_id,
                                                             self.charging_station.unique_id,
                                                             self.charging_station.centroid.unique_id,
                                                             self.travelled_distance,
                                                             self.arrival_time,
                                                             self.initial_battery_level,
                                                             self.final_battery_level,
                                                             self.start_time,
                                                             self.end_time))


class ChargingStationAgent(mg.GeoAgent):
    """A charging station agent."""

    def __init__(self, unique_id, model, geometry, crs, centroid, number_of_charging_ports):
        super().__init__(unique_id, model, geometry, crs)
        self.charging_power = Constants.Simulation.STATION_CHARGING_POWER  # In km/h
        self.centroid = centroid
        self.number_of_charging_ports = number_of_charging_ports
        
        self.charging_cars = []  # [ChargeRecord]
        self.waiting_cars = []  # [ChargeRecord]

    def new_car_arrived(self, car, travelled_distance):
        """A new car has arrived at the charging station."""
        car.is_on_charging_station = True
        chargeRecord = ChargeRecord(car, self, travelled_distance, self.model.schedule.time)

        if self.number_of_charging_ports > len(self.charging_cars):  # There is a free charging port
            self.add_car_to_charging(chargeRecord, self.model.schedule.time)

        else:  # There is no free charging port
            self.add_car_to_queue(chargeRecord)

    def add_car_to_charging(self, chargeRecord, start_time):
        """Add a car to the charging station."""
        chargeRecord.start_charging(start_time)
        self.charging_cars.append(chargeRecord)

    def add_car_to_queue(self, chargeRecord):
        """Add a car to the queue of waiting cars."""        
        self.waiting_cars.append(chargeRecord)

    def move_waiting_to_charging(self, number_of_free_charging_ports):
        """Move the n waiting cars to a charging port."""

        while number_of_free_charging_ports > 0 and len(self.waiting_cars) > 0:
            chargeRecord = self.waiting_cars.pop(0)
            #print("Car {} is now charging.".format(chargeRecord.car.unique_id))
            
            chargeRecord.start_charging(self.model.schedule.time)
            self.charging_cars.append(chargeRecord)

            number_of_free_charging_ports -= 1
        
    def remove_from_charging(self, chargeRecord):
        self.charging_cars.remove(chargeRecord)
        chargeRecord.car.is_on_charging_station = False
    
    def is_free(self):
        """Check if the charging station is free."""
        return len(self.charging_cars) < self.number_of_charging_ports
    
    def get_usage(self):
        """Get the usage of the charging station."""
        return len(self.charging_cars)/self.number_of_charging_ports
        
    def step(self):
        """Advance the agent by one step."""
        # Assuming each step is 1 minute

        number_of_free_charging_ports = self.number_of_charging_ports - len(self.charging_cars)

        for chargeRecord in self.charging_cars:
            # Check if the car is done charging    
            if chargeRecord.car.current_battery_level >= chargeRecord.car.target_battery_level:
                #print("Car {} is done charging.".format(chargeRecord.car.unique_id))

                chargeRecord.end_charging(self.model.schedule.time)
                self.remove_from_charging(chargeRecord)

                number_of_free_charging_ports += 1
                
            else:  # Charge the car
                chargeRecord.car.charge(self.charging_power / 60)  # In minutes
        
        self.move_waiting_to_charging(number_of_free_charging_ports)

        # Log the usage history
        self.log_usage_history(len(self.charging_cars)/self.number_of_charging_ports, self.model.schedule.time)
        self.log_waiting_cars()

    def log_usage_history(self, usage, timestamp):
        """Log the usage history of the charging station."""
        with open(Constants.Logs.RAW_OUPUT_STATIONS_USAGE_FILE_PATH, "a") as file:
            file.write("{},{},{}\n".format(self.unique_id, timestamp, usage))
    
    def log_waiting_cars(self):
        """Log the waiting cars of the charging station."""
        with open(Constants.Logs.RAW_OUPUT_STATIONS_WAITING_CARS_FILE_PATH, "a") as file:
            file.write("{},{},{}\n".format(self.unique_id, self.model.schedule.time, len(self.waiting_cars)))