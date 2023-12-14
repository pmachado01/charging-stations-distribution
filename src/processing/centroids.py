import csv
from shapely.ops import cascaded_union
from shapely.wkt import loads


# Read the CSV file
csv_file_path = './ine/ine_2021_bom_wgs.csv'  # Update with your CSV file path
output_file_path = 'centroids.csv'

# Assuming the column containing WKT geometries is named 'wkt_geom'
wkt_geom_column_name = '\ufeffWKT'

# Function to extract the geometric center of Multipolygons
def extract_geometric_center(wkt_str):
    multipolygon = loads(wkt_str)
    center_point = cascaded_union(multipolygon).centroid
    return center_point.x, center_point.y

# Open the CSV file for reading
with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
    # Create a CSV reader
    reader = csv.DictReader(csvfile)

    # Create a new CSV file for writing the results
    with open(output_file_path, 'w', newline='', encoding='utf-8') as output_csvfile:
        # Define the fieldnames for the output CSV file
        fieldnames = reader.fieldnames + ['lon', 'lat']
        
        # Create a CSV writer
        writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
        
        # Write the header to the output CSV file
        writer.writeheader()
        # Iterate over rows in the input CSV file
        for row in reader:
            # Extract the geometric center and add it to the row
            center_x, center_y = extract_geometric_center(row[wkt_geom_column_name])
            row['lon'] = center_x
            row['lat'] = center_y
            
            # Write the updated row to the output CSV file
            writer.writerow(row)
            
        

print(f"Geometric centers have been added to {output_file_path}.")