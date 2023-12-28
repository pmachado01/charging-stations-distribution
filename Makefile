.PHONY: clean

# Variables
RAW_STATIONS_FILENAME = electromaps_stations.json
RAW_INE_FILENAME = ine_2021.csv

PROCESSED_STATIONS_FILENAME = stations.csv
PROCESSED_CENTROIDS_FILENAME = centroids.csv
SQM_PRICE_FILENAME = sqm_price.csv

all: main

requirements:
	pip3 install -r requirements.txt

main: data_processing

# Process raw data
data_processing: data/raw/$(RAW_INE_FILENAME) data/raw/${RAW_STATIONS_FILENAME}
	python3 -m src.processing.calculate_centroids_center $(RAW_INE_FILENAME) 
	@echo "Centroids calculated"
	python3 -m src.processing.process_stations $(RAW_STATIONS_FILENAME)
	@echo "Stations processed"
ifeq ($(CALCULATE_DISTANCE_MATRIX),true)
    python3 -m src.processing.calculate_distance_matrix
    @echo "Distance matrix calculated"
endif
	python3 -m src.processing.merge_centroids_sqm_price $(SQM_PRICE_FILENAME)
	@echo "Centroids merged with sqm price"
	python3 -m src.processing.get_EVs
	@echo "EVs obtained"

# Perform simulation
simulation: data/processed/centroids.csv data/processed/stations.csv
	mesa runserver src/simulation

# Clean generated files
clean:
	rm data/processed/*
