#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: diegobedoya
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def read_csv_to_data_frame(file_name):
    """
    Parameters:
    file_name (str): The name of the CSV file to be read.

    Returns:
    DataFrame: The content of the CSV file as a pandas DataFrame.

    Does:
    This function reads the content of a CSV file from the given file 
    name and returns it as a pandas DataFrame.
    """
    data_frame = pd.read_csv(file_name)
    
    return data_frame


def plot_crime_trend(df, time_interval):
    """
    This function generates a time series plot to analyze crime trends over 
    different time intervals.
    
    Parameters:
    df (pd.DataFrame): A DataFrame containing crime records with a 'Date' 
    column in the format MM/DD/YYYY HH:MM:SS AM/PM.
    time_interval (str): The time interval for aggregating the data. 
                         Options are 'DAY', 'MONTH', 'YEAR', 'WEEK', 'DAYWEEK'.
    
    The function converts the 'Date' column to datetime format, 
    creates a 'number of crimes' column, and aggregates the data based on the 
    specified time interval.
    
    Supported intervals:
    - 'DAY': Aggregates data by day.
    - 'MONTH': Aggregates data by month.
    - 'YEAR': Aggregates data by year.
    - 'WEEK': Aggregates data by week.
    - 'DAYWEEK': Aggregates data by the day of the week (e.g., Monday, 
                                                         Tuesday).
    
    For the 'MONTH' interval, the x-axis will display months, and a separate 
    curve will be plotted for each year.
    
    Returns:
    A time series plot showing the trend in crime rates over the selected 
    interval.
    """
    
    # Convert 'Date' column to datetime format, including AM/PM
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y %I:%M:%S %p')
    
    # Create 'number of crimes' column
    df['number of crimes'] = 1
    
    # Aggregate the data based on the specified time interval
    if time_interval == 'DAY':
        df_resampled = df.resample('D', on='Date').sum()
    elif time_interval == 'MONTH':
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df_resampled = df.groupby(['Year', 'Month'])['number of crimes'] \
        .sum().unstack(level=0)
        df_resampled.index = df_resampled.index.map(lambda x: pd \
                                    .Timestamp(f"2024-{x}-01").strftime('%B'))
    elif time_interval == 'YEAR':
        df_resampled = df.resample('Y', on='Date').sum().sort_index()
    elif time_interval == 'WEEK':
        df['Week'] = df['Date'].dt.isocalendar().week
        df_resampled = df.groupby('Week')['number of crimes'].sum().\
            sort_index()
    elif time_interval == 'DAYWEEK':
        df['DayOfWeek'] = df['Date'].dt.day_name()
        df_resampled = df.groupby('DayOfWeek')['number of crimes'].sum(). \
        reindex(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', \
             'Saturday', 'Sunday'])
   
    # Plot the data
    plt.figure(figsize=(10, 6))
    
    if time_interval == 'MONTH':
        df_resampled.plot()
        plt.xlabel('Month')
        plt.ylabel('Number of Crimes')
        plt.title('Crime Trend Analysis by Month')
        plt.legend(title='Year')
    elif time_interval == 'DAYWEEK':
        df_resampled.plot(kind='bar', color='skyblue')
        plt.xlabel('Day of the Week')
        plt.ylabel('Number of Crimes')
        plt.title('Crime Trend Analysis by Day of the Week')
    else:
        df_resampled['number of crimes'].plot()
        plt.xlabel('Date')
        plt.ylabel('Number of Crimes')
        plt.title(f'Crime Trend Analysis by {time_interval}')
        
    plt.grid(True)
    plt.show()



def plot_crime_trend_by_year(df, year):
    """
    This function generates a time series plot of crime trends by month 
    for a specific year.
    
    Parameters:
    df (pd.DataFrame): A DataFrame containing crime records with a 'Date' 
    column in the format MM/DD/YYYY HH:MM:SS AM/PM.
    year (int): The specific year to analyze.
    
    The function filters the data for the specified year, 
    aggregates the data by month, and then plots the time series.
    
    Returns:
    A time series plot showing the trend in crime rates by month for the 
    selected year.
    """
    
    # Convert 'Date' column to datetime format, including AM/PM
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y %I:%M:%S %p')
    
    # Filter the DataFrame for the specified year
    df_filtered = df[df['Date'].dt.year == year]
    
    # Aggregate the data by month
    df_filtered['Month'] = df_filtered['Date'].dt.month
    df_resampled = df_filtered.groupby('Month').size()
    
    # Create a mapping of month numbers to month names
    df_resampled.index = df_resampled.index.map(lambda x: pd \
                                .Timestamp(f"2024-{x}-01").strftime('%B'))
    
    # Plot the data
    plt.figure(figsize=(10, 6))
    df_resampled.plot(kind='line', marker='o', color='b')
    plt.xlabel('Month')
    plt.ylabel('Number of Crimes')
    plt.title(f'Crime Trend Analysis for the Year {year}')
    plt.grid(True)
    plt.show()



def plot_crime_trend_by_day_of_week(df, year):
    """
    This function generates a time series plot of crime trends by day 
    of the week for a specific year.
    
    Parameters:
    df (pd.DataFrame): A DataFrame containing crime records with a 'Date' 
    column in the format MM/DD/YYYY HH:MM:SS AM/PM.
    year (int): The specific year to analyze.
    
    The function filters the data for the specified year, 
    aggregates the data by day of the week, and then plots the time series.
    
    Returns:
    A time series plot showing the trend in crime rates by day of the week 
    for the selected year.
    """
    
    # Convert 'Date' column to datetime format, including AM/PM
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y %I:%M:%S %p')
    
    # Filter the DataFrame for the specified year
    df_filtered = df[df['Date'].dt.year == year]
    
    # Aggregate the data by day of the week
    df_filtered['DayOfWeek'] = df_filtered['Date'].dt.day_name()
    df_resampled = df_filtered.groupby('DayOfWeek').size().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', \
         'Sunday'])
    
    # Plot the data as a bar chart
    plt.figure(figsize=(10, 6))
    df_resampled.plot(kind='bar', color='skyblue')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Crimes')
    plt.title(f'Crime Trend Analysis by Day of the Week for the Year {year}')
    plt.grid(True)
    plt.show()



def plot_crime_trend_by_day_of_week_years(df, years):
    """
    This function generates a time series plot of crime trends by day 
    of the week for a specific list of years.
    
    Parameters:
    df (pd.DataFrame): A DataFrame containing crime records with a 'Date' 
    column in the format MM/DD/YYYY HH:MM:SS AM/PM.
    years (list): A list of years to analyze.
    
    The function filters the data for the specified years, 
    aggregates the data by day of the week and year, and then plots the 
    time series with grouped bars.
    
    Returns:
    A bar plot showing the trend in crime rates by day of the week 
    for the selected years.
    """
    
    # Convert 'Date' column to datetime format, including AM/PM
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y %I:%M:%S %p')
    
    # Filter the DataFrame for the specified years
    df_filtered = df[df['Date'].dt.year.isin(years)]
    
    # Aggregate the data by day of the week and year
    df_filtered['DayOfWeek'] = df_filtered['Date'].dt.day_name()
    df_filtered['Year'] = df_filtered['Date'].dt.year
    
    # Group by DayOfWeek and Year, then count occurrences
    df_grouped = df_filtered.groupby(['DayOfWeek', 'Year']).size(). \
    unstack(fill_value=0)
    
    # Reindex to ensure the days of the week are in the correct order
    df_grouped = df_grouped.reindex(['Monday', 'Tuesday', 'Wednesday', 
                                     'Thursday', 
                                     'Friday', 'Saturday', 'Sunday'])
    
    # Plotting using seaborn for better aesthetics
    plt.figure(figsize=(12, 7))
    df_grouped.plot(kind='bar', stacked=False, colormap='viridis')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Crimes')
    plt.title('Crime Trend Analysis by Day of the Week for Years ')
    plt.grid(True)
    plt.legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    plt.show()


def plot_crime_trend_by_years(df, years):
    """
    This function generates a time series plot of crime trends by month 
    for a specific list of years.
    
    Parameters:
    df (pd.DataFrame): A DataFrame containing crime records with a 'Date' 
    column in the format MM/DD/YYYY HH:MM:SS AM/PM.
    years (list): A list of years to analyze.
    
    The function filters the data for the specified years, 
    aggregates the data by month and year, and then plots the time series 
    with lines for each year.
    
    Returns:
    A line plot showing the trend in crime rates by month for the 
    selected years.
    """
    
    # Convert 'Date' column to datetime format, including AM/PM
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y %I:%M:%S %p')
    
    # Filter the DataFrame for the specified years
    df_filtered = df[df['Date'].dt.year.isin(years)]
    
    # Aggregate the data by month and year
    df_filtered['Month'] = df_filtered['Date'].dt.month
    df_filtered['Year'] = df_filtered['Date'].dt.year
    df_grouped = df_filtered.groupby(['Year', 'Month']).size().unstack(fill_value=0)
    
    # Create a mapping of month numbers to month names
    df_grouped.columns = df_grouped.columns.map(lambda x: pd \
                                .Timestamp(f"2024-{x}-01").strftime('%B'))
    
    # Plot the data with lines for each year
    plt.figure(figsize=(12, 7))
    df_grouped.T.plot(kind='line', marker='o', figsize=(12, 7))
    plt.xlabel('Month')
    plt.ylabel('Number of Crimes')
    plt.title('Crime Trend Analysis for Years')
    plt.grid(True)
    plt.legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    plt.show()





def main():

    #Creating the dataframe

    df = read_csv_to_data_frame('Crimes_-_2001_to_Present.csv')

    #Criminal Analysis over years
    plot_crime_trend(df, 'YEAR')
    
    #Criminal Analysis over years by month
    plot_crime_trend(df, 'MONTH')
    
    
    #Criminal Analysis over month in a specific year
    
    plot_crime_trend_by_year(df, 2004)
    plot_crime_trend_by_year(df, 2009)
    plot_crime_trend_by_year(df, 2014)
    plot_crime_trend_by_year(df, 2019)
    plot_crime_trend_by_year(df, 2024)
    
    
    #Criminal Analysis over week days in a specific year
    
    plot_crime_trend_by_day_of_week(df, 2024)
    plot_crime_trend_by_day_of_week(df, 2019)
    plot_crime_trend_by_day_of_week(df, 2014)
    plot_crime_trend_by_day_of_week(df, 2009)
    plot_crime_trend_by_day_of_week(df, 2004)
    
    plot_crime_trend_by_day_of_week_years(df, [2004,2009,2014,2019,2024])
    plot_crime_trend_by_years(df, [2004,2009,2014,2019,2024])


if __name__ == "__main__":
    main()