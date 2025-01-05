import time
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use offscreen mode
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Mapping city names to their respective data files
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_user_input():
    """
    Prompts the user to specify a city, month, and day for data analysis.

    Returns:
        city_name (str): The name of the city to analyze
        filter_month (str): The month to filter by, or 'all' for no filter
        filter_day (str): The day of the week to filter by, or 'all' for no filter
    """
    print('Welcome! Let\'s analyze some US bikeshare data.')

    # Prompt user for city input
    while True:
        city_name = input("Enter the city (Chicago, New York City, Washington): ").strip().lower()
        if city_name in CITY_DATA:
            break
        else:
            print("Invalid input. Please choose from 'Chicago', 'New York City', or 'Washington'.")

    # Prompt user for month input
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        filter_month = input("Enter the month (January, February, ..., June, or 'all'): ").strip().lower()
        if filter_month in valid_months:
            break
        else:
            print("Invalid input. Please choose a valid month or 'all'.")

    # Prompt user for day input
    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        filter_day = input("Enter the day (Monday, Tuesday, ..., Sunday, or 'all'): ").strip().lower()
        if filter_day in valid_days:
            break
        else:
            print("Invalid input. Please choose a valid day or 'all'.")

    print('-' * 50) #print - with 50 characters
    return city_name, filter_month, filter_day

def load_filtered_data(city_name, filter_month, filter_day):
    """
    Loads and filters bikeshare data based on user inputs for city, month, and day.

    Args:
        city_name (str): The selected city for analysis
        filter_month (str): The selected month to filter by
        filter_day (str): The selected day to filter by

    Returns:
        pandas.DataFrame: Filtered bikeshare data
    """
    # Load city data into a DataFrame
    try:
        data_frame = pd.read_csv(CITY_DATA[city_name])
    except FileNotFoundError:
        print(f"Error: The data file for {city_name} was not found.")
        return pd.DataFrame()  # Return an empty DataFrame
    except Exception as e:
        print(f"An unexpected error occurred while loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame

    try:
        # Convert 'Start Time' to datetime
        data_frame['Start Time'] = pd.to_datetime(data_frame['Start Time'])

        # Create new columns for month and day of the week
        data_frame['month'] = data_frame['Start Time'].dt.month_name().str.lower()
        data_frame['day_of_week'] = data_frame['Start Time'].dt.day_name().str.lower()

        # Apply month filter if necessary
        if filter_month != 'all':
            data_frame = data_frame[data_frame['month'] == filter_month]

        # Apply day filter if necessary
        if filter_day != 'all':
            data_frame = data_frame[data_frame['day_of_week'] == filter_day]

    except KeyError as e:
        print(f"Error: Missing expected column in the data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame
    except Exception as e:
        print(f"An unexpected error occurred during filtering: {e}")
        return pd.DataFrame()  # Return an empty DataFrame

    return data_frame

def calculate_time_statistics(data_frame):
    """
    Calculates and displays statistics on the most frequent times of travel.

    Args:
        data_frame (pandas.DataFrame): The filtered bikeshare data
    """
    print('\nAnalyzing Most Frequent Travel Times...')
    start_time = time.time()

    # Identify the most common month
    most_common_month = data_frame['month'].mode()[0]
    print(f"- Most Common Month: {most_common_month.capitalize()}")

    # Identify the most common day of the week
    most_common_day = data_frame['day_of_week'].mode()[0]
    print(f"- Most Common Day of the Week: {most_common_day.capitalize()}")

    # Identify the most common start hour
    data_frame['start_hour'] = data_frame['Start Time'].dt.hour
    most_common_hour = data_frame['start_hour'].mode()[0]
    print(f"- Most Common Start Hour: {most_common_hour}:00")

    print(f"\nCalculation completed in {time.time() - start_time:.2f} seconds.")

def calculate_station_statistics(data_frame):
    """
    Calculates and displays statistics on the most popular stations and trips.

    Args:
        data_frame (pandas.DataFrame): The filtered bikeshare data
    """
    print('\nAnalyzing Most Popular Stations and Trips...')
    start_time = time.time()

    # Most common start station
    most_used_start_station = data_frame['Start Station'].mode()[0]
    print(f"- Most Common Start Station: {most_used_start_station}")

    # Most common end station
    most_used_end_station = data_frame['End Station'].mode()[0]
    print(f"- Most Common End Station: {most_used_end_station}")

    # Most frequent trip combination
    most_frequent_trip = data_frame.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"- Most Frequent Trip: {most_frequent_trip[0]} to {most_frequent_trip[1]}")

    print(f"\nCalculation completed in {time.time() - start_time:.2f} seconds.")

def calculate_trip_duration_statistics(data_frame):
    """
    Calculates and displays statistics on trip duration.

    Args:
        data_frame (pandas.DataFrame): The filtered bikeshare data
    """
    print('\nAnalyzing Trip Duration...')
    start_time = time.time()

    # Total travel time
    total_duration = data_frame['Trip Duration'].sum()
    print(f"- Total Travel Time: {total_duration} seconds")

    # Average travel time
    average_duration = data_frame['Trip Duration'].mean()
    print(f"- Average Travel Time: {average_duration:.2f} seconds")

    print(f"\nCalculation completed in {time.time() - start_time:.2f} seconds.")

def generate_visual_report(data_frame, city_name):
    """
    Generates a visual report summarizing key statistics and saves it as an image.

    Args:
        data_frame (pandas.DataFrame): The filtered bikeshare data
        city_name (str): The name of the selected city
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    report_path = f"reports/{timestamp}_{city_name}_report.jpg"

    # Create the 'reports' directory if it does not exist
    if not os.path.exists('reports'):
        os.makedirs('reports')

    # Plot various statistics
    plt.figure(figsize=(12, 8))

    # Plot most common start hour
    plt.subplot(2, 2, 1)
    data_frame['start_hour'].value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.title('Most Common Start Hours')
    plt.xlabel('Hour')
    plt.ylabel('Frequency')

    # Plot most common start stations
    plt.subplot(2, 2, 2)
    data_frame['Start Station'].value_counts().head(10).plot(kind='bar', color='orange')
    plt.title('Top 10 Start Stations')
    plt.xlabel('Station')
    plt.ylabel('Frequency')

    # Save and close the plot
    plt.tight_layout()
    plt.savefig(report_path, dpi=300)
    plt.close()
    print(f"Visual report saved: {report_path}")

def main():
    while True:
        city_name, filter_month, filter_day = get_user_input()
        filtered_data = load_filtered_data(city_name, filter_month, filter_day)

        calculate_time_statistics(filtered_data)
        calculate_station_statistics(filtered_data)
        calculate_trip_duration_statistics(filtered_data)
        generate_visual_report(filtered_data, city_name)

        restart = input("\nWould you like to analyze another city? Enter 'yes' or 'no': ").strip().lower()
        if restart != 'yes':
            print("\nThank you for using the Bikeshare Data Analysis tool. Goodbye!")
            break

if __name__ == "__main__":
    main()

