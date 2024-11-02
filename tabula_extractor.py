# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 15:19:36 2024

@author: COO1AV
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_building_data(country_request_mask, building_request_mask, country_code, request_id):
    # Ensure request_id is a 13-character numeric string
    request_id = ''.join(filter(str.isdigit, str(request_id)))[:13].zfill(13)
    
    # Build the country URL using the structured mask
    country_url = country_request_mask['Mask'].format(PartUntilCountryCode=country_request_mask['PartUntilCountryCode'],PartAfterCountryCode=country_request_mask['PartAfterCountryCode'],country_code=country_code, request_id=request_id)
    
    # API request for country buildings
    country_response = requests.get(country_url)
    if country_response.status_code != 200 or not country_response.json().get("success"):
        return None, None, False
    
    # Parse country response data
    country_data = country_response.json().get("data", [])
    df_country = pd.DataFrame(country_data)
    
   # Extract building codes by concatenating columns and suffixes
    building_codes = []
    for i in range(1, 5):  # Loop through 1 to 4 for the columns
        code_column = f"code_buildingtype_column{i}"
        suffix_column = f"suffix_building_column{i}"
        codes_with_suffix = df_country[code_column] +"."+ df_country[suffix_column]
        building_codes.extend(codes_with_suffix.dropna().tolist())  # Extend the building_codes list
        
    # Remove any empty strings from the building codes
    building_codes = list(filter(lambda x: x != ".", building_codes))

    
    # Create a list to hold building details
    building_details = []
    
    # Loop through building codes and get details
    for building_code in building_codes:
        building_url = building_request_mask['Mask'].format(PartUntilBuildingCode=building_request_mask['PartUntilBuildingCode'],PartAfterBuildingCode=building_request_mask['PartAfterBuildingCode'],building_code=building_code, request_id=request_id)
        
        try:
            building_response = requests.get(building_url)
            building_response.raise_for_status()  # Raise an error for bad responses
            
            # Check if the response was successful
            if building_response.json().get("success"):
            # Get the data and append building_code to each detail
                data = building_response.json().get("data", [])
                for item in data:
                    item['building_code'] = building_code  # Add the building_code to the item
                    building_details.append(item)  # Append the modified item
            else:
                print(f"Building code {building_code} returned unsuccessful response.")

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err} for building code {building_code}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err} for building code {building_code}")
        except ValueError as json_err:
            print(f"JSON decode error: {json_err} for building code {building_code}")
        except Exception as e:
            print(f"An unexpected error occurred: {e} for building code {building_code}")

    
    # Parse building details data
    df_building = pd.DataFrame(building_details)
    
    # Final success check based on successful requests and "success" key
    success = country_response.json().get("success") and len(df_building) > 0

    return df_country, df_building, success

def plot_weighted_histogram(df, value_column, count_column, bin_width=10, title="Weighted Histogram"):
    """
    Plots a weighted histogram where counts for each bin are determined by the `count_column`.
    
    Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - value_column (str): Column name for values to be binned (e.g., 'BuildingHeatDemand').
    - count_column (str): Column name for weights or counts (e.g., 'NoOfBuildings').
    - bin_width (float): Width of each bin.
    - title (str): Title of the histogram.
    """
    
    # Calculate min and max values for bins
    min_value = df[value_column].min()
    max_value = df[value_column].max()
    bins = np.arange(min_value, max_value + bin_width, bin_width)

    # Convert count_column to integers for np.repeat
    counts_as_int = df[count_column].astype(int).values
    
    # Repeat each BuildingHeatDemand value by the count in NoOfBuildings
    weighted_values = np.repeat(df[value_column].values, counts_as_int)
    
    # Plot histogram
    fig, ax = plt.subplots()  # Create a new figure and axes
    n, bins, patches = ax.hist(weighted_values, bins=bins, edgecolor='black')
    plt.xlabel(value_column)
    plt.ylabel(count_column)
    plt.title(title)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add value labels on top of each bar
    for count, patch in zip(n, patches):
        height = patch.get_height()
        ax.text(patch.get_x() + patch.get_width() / 2, height, str(round(count)), 
                ha='center', va='bottom', fontsize=10)
    
    plt.show()