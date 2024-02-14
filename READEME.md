# Design Doc writeup

## Solution Overview

The solution aims to analyze transaction data and identify the postcodes that have seen the highest increase in transactions over a specified period. It involves several steps:

1. **Loading Data**: Load transaction data and postcode data from CSV files into Pandas DataFrames.
2. **Data Preprocessing**: Preprocess the data, including handling missing values, converting data types, and generating a unique identifier for each property.
3. **Calculating Increase**: Calculate the increase in transactions for each postcode by comparing transaction counts between the most recent year and a specified number of years ago.
4. **Identifying Top Postcodes**: Identify the top postcodes with the highest increase in transactions.
5. **Visualization**: Visualize the top postcodes using matplotlib to create a bar plot showing the increase in transactions.

## Questions

1. There is no unique identifier for a property in the data. How would you approach this to come up with a column that can be used as a unique id for each property? Would you combine any columns for instance? Can you test your method that it returns unique values? Are there any
issues?

    I used a combination field of the following:

    ```python
        key_fields = ['Postcode', 'PAON', 'SAON', 'Street', 'Locality', 'Town/City', 'District', 'County']
    ```

    in hindsight, there is probably a better way to do this, but I think this works well. regardless of the issues with being unable to go back or the enforcement of determanism.

2. Once you have defined a property unique id (unfortunately this doesn’t exist in the data so it
needs to be defined by you), how would you store the data in your SQL database? What table
structure would you use?

    I've proposed a SQL schema below, but I would use uniqueID as the pk of the table for transactions.

3. How would you work on improving the performance of the queries? Would you use primary
keys, indexes?

    I've used primary keys on each table along with indexes of postcode and transactiondate, and lat and long

## Methods Breakdown

### 1. load_data()

- Description: Loads various data files into memory and returns them as separate objects.
- Parameters: None
- Returns: Transaction data, house price index data, average price data, CPI index data, and postcode coordinates data.

### 2. load_transaction_data()

- Description: Loads transaction data from CSV files into a Pandas DataFrame.
- Parameters: None
- Returns: DataFrame containing transaction data.

### 3. generate_unique_property_id(data)

- Description: Generates a unique identifier for each property based on key fields.
- Parameters: data (DataFrame) - DataFrame containing transaction data.
- Returns: DataFrame with an additional 'UniqueID' column.

### 4. store_data_in_sql_database(data)

- Description: Defines SQL table structures and stores data in a SQL database.
- Parameters: data (list) - List of data objects to be stored.
- Returns: None

### 5. load_postcode_data()

- Description: Loads postcode coordinates data from a CSV file into memory.
- Parameters: None
- Returns: List of Postcode objects.

### 7. query_transactions_by_postcode_and_date_range(postcode, start_date, end_date)

- Description: Queries transactions based on postcode and date range.
- Parameters:
  - postcode (str): Postcode to filter transactions.
  - start_date (str): Start date of the date range.
  - end_date (str): End date of the date range.
- Returns: Filtered DataFrame of transactions.

### 8. properties_sold_in_postcode(postcode)

- Description: Returns the number of properties sold in a given postcode and corresponding transaction IDs.
- Parameters: postcode (str) - Postcode to filter transactions.
- Returns: Tuple containing the number of properties sold and a list of transaction IDs.

### 9. top_postcodes_with_highest_increase(transaction_data, years=5, top_n=10)

- Description: Finds postcodes with the highest increase in transactions over the last `years` years.
- Parameters:
  - transaction_data (DataFrame): DataFrame containing transaction data.
  - years (int): Number of years to consider (default: 5).
  - top_n (int): Number of top postcodes to return (default: 10).
- Returns: DataFrame with top postcodes and their transaction increase.

### 10. plot_top_postcodes(top_postcodes)

- Description: Plots top postcodes with the highest increase in transactions.
- Parameters: top_postcodes (DataFrame) - DataFrame containing top postcodes and their transaction increase.
- Returns: None

## Data Model

### Transactions Table

| Column Name        | Data Type      | Description                           |
|--------------------|----------------|---------------------------------------|
| UniqueID           | VARCHAR(100)   | Primary key - Unique transaction identifier |
| TransactionID      | VARCHAR(50)    | Transaction identifier                |
| Price              | DECIMAL(18, 2) | Price of the transaction              |
| DateOfTransfer     | DATE           | Date of the transaction               |
| Postcode           | VARCHAR(20)    | Postcode where the property is located |
| PropertyType       | VARCHAR(50)    | Type of the property (e.g., house, flat) |
| OldOrNew           | VARCHAR(10)    | Indicates if the property is old or new |
| Duration           | VARCHAR(10)    | Duration of the property ownership    |
| PAON               | VARCHAR(100)   | Primary Addressable Object Name       |
| SAON               | VARCHAR(100)   | Secondary Addressable Object Name     |
| Street             | VARCHAR(100)   | Street name                           |
| Locality           | VARCHAR(100)   | Locality                              |
| TownCity           | VARCHAR(100)   | Town or city                          |
| District           | VARCHAR(100)   | District                              |
| County             | VARCHAR(100)   | County                                |
| PPDCategoryType    | VARCHAR(100)   | Category of the transaction           |
| RecordStatus       | VARCHAR(100)   | Record status                         |

#### HousePriceIndex Table

| Column Name   | Data Type      | Description                           |
|---------------|----------------|---------------------------------------|
| Date          | DATE           | Date of the index                     |
| IndexValue    | DECIMAL(18, 2) | House price index value               |

#### AveragePrice Table

| Column Name   | Data Type      | Description                           |
|---------------|----------------|---------------------------------------|
| Date          | DATE           | Date of the average price             |
| AveragePrice  | DECIMAL(18, 2) | Average property price                |

#### CPIIndex Table

| Column Name   | Data Type      | Description                           |
|---------------|----------------|---------------------------------------|
| Date          | DATE           | Date of the index                     |
| CPI           | DECIMAL(18, 2) | Consumer Price Index value            |

#### PostcodeCoordinates Table

| Column Name        | Data Type      | Description                           |
|--------------------|----------------|---------------------------------------|
| Postcode           | VARCHAR(20)    | Primary key - Postcode                |
| Latitude           | DECIMAL(9, 6)  | Latitude coordinate                   |
| Longitude          | DECIMAL(9, 6)  | Longitude coordinate                  |
| PositionalQuality  | INT            | Quality of the position               |
| LocalAuthorityName | VARCHAR(100)   | Name of the local authority           |
| SpatialAccuracy    | VARCHAR(100)   | Accuracy of spatial data              |
| LastUploaded       | TIMESTAMP      | Timestamp of last upload              |
| Location           | VARCHAR(100)   | Location description                  |
| SocrataID          | VARCHAR(100)   | Socrata ID for the data               |

### Proposed SQL Schema

```SQL
-- Table for transaction data
CREATE TABLE Transactions (
    UniqueID VARCHAR(100) PRIMARY KEY,
    TransactionID VARCHAR(50),
    Price DECIMAL(18, 2),
    DateOfTransfer DATE,
    Postcode VARCHAR(20),
    PropertyType VARCHAR(50),
    OldOrNew VARCHAR(10),
    Duration VARCHAR(10),
    PAON VARCHAR(100),
    SAON VARCHAR(100),
    Street VARCHAR(100),
    Locality VARCHAR(100),
    TownCity VARCHAR(100),
    District VARCHAR(100),
    County VARCHAR(100),
    PPDCategoryType VARCHAR(100),
    RecordStatus VARCHAR(100)
);
```

```SQL
CREATE INDEX idx_DateOfTransfer ON Transactions (DateOfTransfer);
CREATE INDEX idx_Postcode ON Transactions (Postcode);
```

```SQL
-- Table for house price index data
CREATE TABLE HousePriceIndex (
    Date DATE PRIMARY KEY,
    IndexValue DECIMAL(18, 2)
);
```

```SQL
-- Table for average price data
CREATE TABLE AveragePrice (
    Date DATE PRIMARY KEY,
    AveragePrice DECIMAL(18, 2)
);
```

```SQL
-- Table for CPI index data
CREATE TABLE CPIIndex (
    Date DATE PRIMARY KEY,
    CPI DECIMAL(18, 2)
);
```

```SQL
-- Table for postcode coordinates data
CREATE TABLE PostcodeCoordinates (
    Postcode VARCHAR(20) PRIMARY KEY,
    Latitude DECIMAL(9, 6),
    Longitude DECIMAL(9, 6),
    PositionalQuality INT,
    LocalAuthorityName VARCHAR(100),
    SpatialAccuracy VARCHAR(100),
    LastUploaded TIMESTAMP,
    Location VARCHAR(100),
    SocrataID VARCHAR(100)
);
```

```SQL
CREATE INDEX idx_Latitude ON PostcodeCoordinates (Latitude);
CREATE INDEX idx_Longitude ON PostcodeCoordinates (Longitude);
```
