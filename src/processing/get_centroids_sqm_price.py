from src.utils.constants import Constants
import src.utils.files as Files
import pandas as pd
import argparse


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("sqm_price_file", help="Price per sqm file name")
    args = arg_parser.parse_args()

    # Get the price per sqm file path
    sqm_price_file_path = Files.get_raw_file_path(args.sqm_price_file)

    # Read the prices per place CSV file into a pandas DataFrame
    sqm_price = Files.read_csv_file(sqm_price_file_path)

    # Get the centroids file path
    centroids_file_path = Files.get_processed_file_path(Constants.Data.PROCESSED_CENTROIDS_FILE_NAME)

    # Read the centroids file
    centroids = Files.read_csv_file(centroids_file_path)

    # Merge the two DataFrames on the common column 'DTMNFR21'
    merged = pd.merge(centroids, sqm_price, on='DTMNFR21')

    # Save the merged DataFrame to a new CSV file
    output_file_path = centroids_file_path
    Files.write_csv_file(output_file_path, merged)
