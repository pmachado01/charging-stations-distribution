from src.utils.constants import Constants
import src.utils.files as Files
from math import ceil


def estimate_number_of_evs(price_per_sqm, population, average_ev_price, total_population_for_place):
    """Estimate the number of EVs in a given place based on the price per sqm, the population over 15 years old, the average EV price and the total population for the region.

    Args:
        price_per_sqm (float): The price per sqm in the given place.
        population (int): The population over 15 years old in the given place.
        average_ev_price (float): The average EV price in the given place.
        total_population_for_place (int): The total population for the gven place.

    Returns:
        int: The estimated number of EVs in the given place.
    """

    print('Price per sqm: ', price_per_sqm)
    print('Population: ', population)
    print('Average EV price: ', average_ev_price)
    print('Total population for place: ', total_population_for_place)

    
    total_evs_in_portugal = 50000

    average_ev_price_portugal = 35000
    number_of_evs_in_portugal = total_evs_in_portugal * (average_ev_price_portugal / average_ev_price)

    population_in_porto = 234438 # (https://www.pordata.pt/Municipios/Popula%C3%A7%C3%A3o+residente+segundo+os+Censos+total+e+por+grandes+grupos+et%C3%A1rios-390)
    population_in_portugal = 10407707 # (https://www.pordata.pt/Municipios/Popula%C3%A7%C3%A3o+residente+segundo+os+Censos+total+e+por+grandes+grupos+et%C3%A1rios-390)
    population_ratio_porto_portugal = population_in_porto / population_in_portugal
    
    evs_per_capita_porto = (number_of_evs_in_portugal * population_ratio_porto_portugal) / population_in_porto

    price_per_sqm_porto = 2981 # https://www.idealista.pt/media/relatorios-preco-habitacao/venda/porto/porto/historico/
    ratio_sqm_place  = price_per_sqm / price_per_sqm_porto
    number_of_evs_place = evs_per_capita_porto * ratio_sqm_place * total_population_for_place

    print('Number of EVs: ', number_of_evs_place)

    return number_of_evs_place


def add_ev_number_column(centroids_df):
    """Add a new column to the given DataFrame with the estimated number of EVs in the given place.

    Args:
        centroids_df (DataFrame): The DataFrame with the centroids.

    Returns:
        DataFrame: The DataFrame with the estimated number of EVs in the given place.
    """

    average_ev_price = 35000

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

        # Retrieve the place's population
        total_population_for_place = row['N_INDIVIDUOS']-row['N_INDIVIDUOS_0_14']

        # Retrieve the price per sqm for the given place
        sqm_price = row['sqm_price']

        # Add a new column with the estimated number of EVs in the given place.
        centroids_df.loc[index, 'number_of_ev_cars'] = estimate_number_of_evs(sqm_price, row['N_INDIVIDUOS']-row['N_INDIVIDUOS_0_14'], average_ev_price, total_population_for_place)

    # Print the sum of the estimated number of EVs in the given place.
    print('Estimated number of EVs in Porto: ', centroids_df['number_of_ev_cars'].sum())

    return centroids_df


def main():
    # Get the centroids file path
    centroids_file_path = Files.get_processed_file_path(Constants.Data.PROCESSED_CENTROIDS_FILE_NAME)

    # Read centroids file
    centroids_data = Files.read_csv_file(centroids_file_path)

    # Add a new column with the estimated number of EVs in the given place.
    centroids_data = add_ev_number_column(centroids_data)

    # Save the DataFrame to a CSV file
    Files.write_csv_file(centroids_file_path, centroids_data)


if __name__ == "__main__":
    main()
