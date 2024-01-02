import mesa_geo as mg


class CentroidAgent(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs):
        super().__init__(unique_id, model, geometry, crs)
        self.stations = []

    def add_station(self, station):
        self.stations.append(station)

    def get_available_charging_station(self):
        for station in self.stations:
            if station.is_free():
                return station

        return None
