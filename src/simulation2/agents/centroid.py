import mesa_geo as mg


class CentroidAgent(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs):
        super().__init__(unique_id, model, geometry, crs)
        self.stations = []

    def add_station(self, station):
        self.stations.append(station)
