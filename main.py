import hashlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from postcode import Postcode
from transaction import Transaction
from property import Property


def load_data():
    transaction_data = load_transaction_data()
    house_price_index_data = pd.read_csv('data/house-price-index.csv')
    average_price_data = pd.read_csv('data/Average-prices-2021-03.csv')
    cpi_index_data = pd.read_csv('data/cpi.csv', low_memory=False)
    postcode_coordinates_data = load_postcode_data()

    return transaction_data, house_price_index_data, average_price_data, cpi_index_data, postcode_coordinates_data

def load_transaction_data():
    transaction_columns = [
        'Transaction unique identifier',
        'Price',
        'Date of Transfer',
        'Postcode',
        'Property Type',
        'Old/New',
        'Duration',
        'PAON',
        'SAON',
        'Street',
        'Locality',
        'Town/City',
        'District',
        'County',
        'PPD Category Type',
        'Record Status'
    ]

    dtype_dict = {
        'Transaction unique identifier': str,
        'Price': float,
        'Date of Transfer': str,  # You might want to convert this to datetime later
        'Postcode': str,
        'Property Type': str,
        'Old/New': str,
        'Duration': str,
        'PAON': str,
        'SAON': str,
        'Street': str,
        'Locality': str,
        'Town/City': str,
        'District': str,
        'County': str,
        'PPD Category Type': str,
        'Record Status': str
    }

    transaction_data_part1 = pd.read_csv('data/transaction-2022.csv', names=transaction_columns, dtype=dtype_dict,
                                         low_memory=False)
    transaction_data_part2 = pd.read_csv('data/transaction-2023.csv', names=transaction_columns, dtype=dtype_dict,
                                         low_memory=False)

    # Concatenate the two DataFrames vertically
    transaction_data = pd.concat([transaction_data_part1, transaction_data_part2], ignore_index=True)
    transaction_data = generate_unique_property_id(transaction_data)

    return transaction_data

def generate_unique_property_id(data):
    key_fields = ['Postcode', 'PAON', 'SAON', 'Street', 'Locality', 'Town/City', 'District', 'County']

    # Concat key fields for each property
    data['UniqueID'] = data[key_fields].fillna('').astype(str).apply('_'.join, axis=1)

    data['UniqueID'] = data['UniqueID'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())


    return data

def load_postcode_data():
    # Load postcode data into a pandas DataFrame
    postcode_coordinates_data = pd.read_csv('data/post-code-data.csv')
    
    # Concatenate the three postcode columns into a single postcode string
    postcode_coordinates_data['Postcode'] = postcode_coordinates_data[['Postcode 1', 'Postcode 2', 'Postcode 3']].fillna('').astype(str).apply('_'.join, axis=1)

    # Drop the individual postcode columns
    postcode_coordinates_data.drop(['Postcode 1', 'Postcode 2', 'Postcode 3'], axis=1, inplace=True)

    return postcode_coordinates_data

def top_postcodes_with_highest_increase(transaction_data, years=5, top_n=10):
    transaction_data['Date of Transfer'] = pd.to_datetime(transaction_data['Date of Transfer'])
    recent_transactions = transaction_data[transaction_data['Date of Transfer'] >= pd.Timestamp.now() - pd.DateOffset(years=years)]

    transaction_counts = recent_transactions.groupby('Postcode').size().reset_index(name='Transaction Count')
    transaction_counts['Increase'] = transaction_counts.groupby('Postcode')['Transaction Count'].diff()

    transaction_counts['Increase'].fillna(0, inplace=True)  # Replace NaN with 0 for postcodes with missing data

    # Sort postcodes by increase
    sorted_postcodes = transaction_counts.sort_values(by='Increase', ascending=False)
    top_postcodes = sorted_postcodes.head(top_n)

    return top_postcodes


def plot_top_postcodes(top_postcodes):
    # Check if increase column contains zeros
    if top_postcodes['Increase'].eq(0).all():
        print("No increase in transactions.")
    else:
        # Replace NaN values in 'Increase' column with 0
        top_postcodes['Increase'].fillna(0, inplace=True)

        plt.figure(figsize=(10, 6))
        plt.barh(top_postcodes['Postcode'], top_postcodes['Increase'], color='skyblue')
        plt.xlabel('Increase in Transactions')
        plt.ylabel('Postcode')
        plt.title('Postcodes with Highest Increase')
        plt.gca().invert_yaxis()
        plt.show()


def properties_sold_in_postcode(postcode):
    properties = []
    transaction_ids = []
    for transaction in transaction_data:
        if transaction.postcode == postcode:
            properties.append(transaction.unique_id)
            transaction_ids.append(transaction.transaction_id)
    return len(set(properties)), transaction_ids

def plot_postcode_data():
    postcodes = ['EC1A', 'W1A', 'SW1A', 'NW1A', 'SE1A']
    sales = [100, 150, 80, 120, 200]
    plt.bar(postcodes, sales)
    plt.xlabel('Postcode')
    plt.ylabel('Number of Sales')
    plt.title('Sales in Different Postcodes')

    plt.show()

def calculate_ec1a_center(postcode_coordinates_data):
    ec1a_postcodes = ['EC1A']
    ec1a_postcode_data = postcode_coordinates_data[postcode_coordinates_data['Postcode'].isin(ec1a_postcodes)]
    ec1a_center_latitude = ec1a_postcode_data['Latitude'].mean()
    ec1a_center_longitude = ec1a_postcode_data['Longitude'].mean()
    return ec1a_center_latitude, ec1a_center_longitude

def calculate_distance(x1, y1, x0, y0):
    return np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

def plot_average_price_vs_distance(transaction_data, postcode_coordinates_data):
    ec1a_center_latitude, ec1a_center_longitude = calculate_ec1a_center(postcode_coordinates_data)

    # Calculate dist from EC1A
    transaction_data['Distance'] = calculate_distance(postcode_coordinates_data['Latitude'], postcode_coordinates_data['Longitude'],
                                                      ec1a_center_latitude, ec1a_center_longitude)

    plt.figure(figsize=(10, 6))
    plt.scatter(transaction_data['Distance'], transaction_data['Price'], alpha=0.5)
    plt.xlabel('Distance from EC1A')
    plt.ylabel('Average Transaction Price')
    plt.title('Average Transaction Price vs. Distance from EC1A')
    plt.show()

def main():
    transaction_data, house_price_index_data, average_price_data, cpi_index_data, postcode_coordinates_data = load_data()
    top_postcodes = top_postcodes_with_highest_increase(transaction_data, 2, 5)
    print(top_postcodes)
    print(transaction_data)
    print(house_price_index_data)
    print(average_price_data)
    plot_postcode_data()
    plot_top_postcodes(top_postcodes)
    plot_average_price_vs_distance(transaction_data, postcode_coordinates_data)


if __name__ == "__main__":
    main()
