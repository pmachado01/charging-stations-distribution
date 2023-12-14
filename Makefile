.PHONY: clean

# Variables
RAW_STATIONS_FILENAME = electromaps_stations.json
RAW_INE_FILENAME = ine_2021.csv
PROCESSED_STATIONS_FILENAME = stations.csv
PROCESSED_CENTROIDS_FILENAME = centroids.csv

all: main

main: data_processing simulation

# Process raw data
data_processing: data/raw/$(RAW_INE_FILENAME) data/raw/${RAW_STATIONS_FILENAME}
	python -m src.processing.calculate_centroids_center $(RAW_INE_FILENAME) 
	python -m src.processing.process_stations $(RAW_STATIONS_FILENAME) $(RAW_INE_FILENAME) 

# Perform simulation
simulation: data/processed/centroids.csv data/processed/stations.csv
	mesa runserver src/simulation

# Clean generated files
clean:
	rm data/processed/*