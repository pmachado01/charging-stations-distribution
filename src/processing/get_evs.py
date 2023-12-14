import csv


# Read the CSV file
csv_file_path = './processed/centroids.csv'
sqm_file_path = './raw/sqm_price_per_place.csv'
output_file_path = 'evs.csv'

sqm_per_place_dict = {}
# Read the prices per place CSV file
with open(sqm_file_path, 'r', newline='', encoding='utf-8') as sqm_csvfile:
    sqm_reader = csv.DictReader(sqm_csvfile)
    sqm_per_place_dict = {}
    for row in sqm_reader:
        sqm_per_place_dict[row['DTMNFR21']] = row['sqm_price']

# Open the CSV file for reading
with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
    # Create a CSV reader
    reader = csv.DictReader(csvfile)

    # Create a new CSV file for writing the results
    with open(output_file_path, 'w', newline='', encoding='utf-8') as output_csvfile:
        # Define the fieldnames for the output CSV file
        fieldnames = reader.fieldnames + ['sqm_price']
        
        # Create a CSV writer
        writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
        
        # Write the header to the output CSV file
        writer.writeheader()
        # Iterate over rows in the input CSV file
        for row in reader:
            row['sqm_price'] = sqm_per_place_dict[row['DTMNFR21']]            
            # Write the updated row to the output CSV file
            writer.writerow(row)

print(f"The price per sqm has been added to {output_file_path}.")