import mesa

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
        charging_power = charging_station.charging_power / 60 # In km/min

        return self.calculate_required_charging_energy() / charging_power # In minutes
    
    def calculate_required_charging_energy(self):
        """Calculate the required charging energy for the car at the given charging station."""
        return self.full_battery_range - self.calculate_current_range() # In kilometers

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

        self.travel(10) # Travel 10 km

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


class ChargeRecord:
    """A charging record."""

    def __init__(self, car, charging_station, arrival_time):
        self.car = car
        self.charging_station = charging_station  #TODO: Check if is necessary
        self.arrival_time = arrival_time
        self.start_time = None
        self.end_time = None

    def start_charging(self, timestamp):
        """Start charging the car."""
        self.start_time = timestamp

    def end_charging(self, timestamp):
        """End charging the car."""
        self.end_time = timestamp


class ChargingStationAgent(mesa.Agent):
    """A charging station agent."""

    def __init__(self, unique_id, model, number_of_charging_ports):
        super().__init__(unique_id, model)
        self.charging_power = 750 # In km/h
        self.number_of_charging_ports = number_of_charging_ports
        
        self.charging_cars = []  # [ChargeRecord]
        self.waiting_cars = []  # [ChargeRecord]

    def new_car_arrived(self, car):
        """A new car has arrived at the charging station."""
        car.is_on_charging_station = True

        if self.number_of_charging_ports > len(self.charging_cars): # There is a free charging port
            self.add_car_to_charging(car, self.model.schedule.time)

        else: # There is no free charging port
            self.add_car_to_queue(car, self.model.schedule.time)

    def add_car_to_charging(self, car, timestamp):
        """Add a car to the charging station."""
        chargeRecord = ChargeRecord(car, self, timestamp)
        chargeRecord.start_charging(timestamp)

        self.charging_cars.append(chargeRecord)

    def add_car_to_queue(self, car, timestamp):
        """Add a car to the queue of waiting cars."""
        chargeRecord = ChargeRecord(car, self, timestamp)
        
        self.waiting_cars.append(chargeRecord)

    def move_waiting_to_charging(self, number_of_free_charging_ports):
        """Move the n waiting cars to a charging port."""

        while number_of_free_charging_ports > 0 and len(self.waiting_cars) > 0:
            car_to_charge = self.waiting_cars.pop(0)
            print("Car {} is now charging.".format(car_to_charge.unique_id))
            
            car_to_charge.start_charging(self.model.schedule.time)
            self.charging_cars.append(car_to_charge)

            number_of_free_charging_ports -= 1
        
    def remove_from_station(car, list):
        car.is_on_charging_station = False
        list.remove(car)

    def step(self):
        """Advance the agent by one step."""
        # Assuming each step is 1 minute

        number_of_free_charging_ports = self.number_of_charging_ports - len(self.charging_cars)

        for chargeRecord in self.charging_cars:
            # Check if the car is done charging    
            if chargeRecord.car.current_battery_level >= chargeRecord.car.target_battery_level:
                print("Car {} is done charging.".format(chargeRecord.car.unique_id))

                chargeRecord.end_charging(self.model.schedule.time)
                self.remove_from_station(chargeRecord.car, self.charging_cars)

                number_of_free_charging_ports += 1
                
            else : # Charge the car
                chargeRecord.car.charge(self.charging_power / 60) # In minutes
        
        self.move_waiting_to_charging(number_of_free_charging_ports)
