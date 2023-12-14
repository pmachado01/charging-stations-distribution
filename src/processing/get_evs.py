from math import ceil
import pandas as pd

# File paths
csv_file_path = '../../data/processed/centroids.csv'
sqm_file_path = '../../data/raw/sqm_price_per_place.csv'
output_file_path = 'evs.csv'

def estimate_number_of_evs(price_per_sqm, population, average_ev_price, total_population_for_region):
    """Estimate the number of EVs in a given place based on the price per sqm, the population over 15 years old, the average EV price and the total population for the region.

    Args:
        price_per_sqm (float): The price per sqm in the given place.
        population (int): The population over 15 years old in the given place.
        average_ev_price (float): The average EV price in the given place.
        total_population_for_region (int): The total population for the region.

    Returns:
        int: The estimated number of EVs in the given place.
    """

    print('Price per sqm: ', price_per_sqm)
    print('Population: ', population)
    print('Average EV price: ', average_ev_price)
    print('Total population for region: ', total_population_for_region)

    # The number of EVs per 1000 people. This is like saying that the percentage of EVs in a given place is 0.005%.
    number_of_evs_cars_per_1000 = 4

    # Ratio between the population over 15 years old and the total population for the region.
    population_ratio = population / total_population_for_region

    # The number of EVs based on the population and the number of EVs per 10000 people.
    number_of_evs_based_on_population = ceil(population_ratio * 1000 * number_of_evs_cars_per_1000)

    # The number of EVs based on the price per sqm and the average EV price.
    number_of_evs_based_on_price = ceil(population_ratio * 35000 * (price_per_sqm / average_ev_price))

    print('Number of EVs based on population: ', number_of_evs_based_on_population)
    print('Number of EVs based on price: ', number_of_evs_based_on_price)

    return min(number_of_evs_based_on_population, number_of_evs_based_on_price)


def add_ev_number_column(centroids_df):
    """Add a new column to the given DataFrame with the estimated number of EVs in the given place.

    Args:
        centroids_df (DataFrame): The DataFrame with the centroids.

    Returns:
        DataFrame: The DataFrame with the estimated number of EVs in the given place.
    """

    average_ev_price = 45000

    # Retrieve the sum of 'row['N_INDIVIDUOS']-row['N_INDIVIDUOS_0_14']' for each region based on the column 'DTMNFR21'.
    sum_of_population_for_region = {} # {DTMNFR21: sum_of_population_for_region}
    for index, row in centroids_df.iterrows():
        if row['DTMNFR21'] not in sum_of_population_for_region:
            sum_of_population_for_region[row['DTMNFR21']] = row['N_INDIVIDUOS']-row['N_INDIVIDUOS_0_14']
        else:
            sum_of_population_for_region[row['DTMNFR21']] += row['N_INDIVIDUOS']-row['N_INDIVIDUOS_0_14']

    for index, row in centroids_df.iterrows():
        # Retrieve the total population for the region
        total_population_for_region = sum_of_population_for_region[row['DTMNFR21']]

        # Retrieve the price per sqm for the given place
        sqm_price = sqm_df.loc[sqm_df['DTMNFR21'] == row['DTMNFR21'], 'sqm_price'].iloc[0]

        # Add a new column with the estimated number of EVs in the given place.
        centroids_df.loc[index, 'number_of_ev_cars'] = estimate_number_of_evs(sqm_price, row['N_INDIVIDUOS']-row['N_INDIVIDUOS_0_14'], average_ev_price, total_population_for_region)

    # Print the sum of the estimated number of EVs in the given place.
    print('Estimated number of EVs in Portugal: ', centroids_df['number_of_ev_cars'].sum())

    return centroids_df


# Read the prices per place CSV file into a pandas DataFrame
sqm_df = pd.read_csv(sqm_file_path, encoding='utf-8')

# Read the centroids CSV file into a pandas DataFrame
centroids_df = pd.read_csv(csv_file_path, encoding='utf-8')

# Merge the two DataFrames on the common column 'DTMNFR21'
merged_df = pd.merge(centroids_df, sqm_df, on='DTMNFR21')

# Add a new column with the estimated number of EVs in the given place.
merged_df = add_ev_number_column(merged_df)

# Save the merged DataFrame to a new CSV file
merged_df.to_csv(output_file_path, index=False, encoding='utf-8')