#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Charles Youtt

File: working_project.py

Date: August 16 2024

Class: DS 2500

Description: Analyzes Chicago's crime from 2001 - present. Creates
plots of Chicago's crime hotspots and most common arrest
types by district. Uses geopandas to make a map of Chicago's
districts to be able to visually see changes in crime throughout every year.
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import seaborn as sns

CRIME_FILEPATH = 'data/Crimes_-_2001_to_Present.csv'
SHAPE_FILEPATH = 'data/Boundaries - Police Districts (current)/'
'geo_export_1e709dcc-0435-46d9-83db-53fa67d92f5e.shp'
YEAR = 2023
CRIME_TYPE_COL = 'Primary Type'
LAT_COL = 'Latitude'
LON_COL = 'Longitude'
SHAPE_DISTRICT_COL = 'dist_num'
CRIME_DISTRICT_COL = 'District'
CRIME_COUNT_COL = 'Crime Count'
CHOSEN_CRIME = 'BATTERY'

def filter_chunk_data_by_year(csv_path, year, chunk_size=1000000):
    """
    Takes in a CSV file path, a year, and an optional chunk size
    and returns a dataframe that is filtered by the specified
    year loaded in chunks.
    """
    filtered_data = []
   
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
        # filter each chunk by the specified year
        chunk_filtered = chunk[chunk['Year'] == year]
        filtered_data.append(chunk_filtered)
   
    # combine all filtered chunks into one dataframe
    df_filtered = pd.concat(filtered_data, ignore_index=True)
   
    return df_filtered

def clean_data(df):
    """
    Takes in a dataframe and returns the dataframe with no missing
    latitude, longitude, and crime type values and also makes
    sure the crime type is cleaned and uppercased.
    """
    # drops rows with missing values and clean crime type column
    df = df.dropna(subset=[LAT_COL, LON_COL, CRIME_TYPE_COL]).copy()
    df[CRIME_TYPE_COL] = df[CRIME_TYPE_COL].str.strip().str.upper()
   
    return df

def geodataframe(df):
    """
    Takes in a dataframe and returns a geodataframe with a Point
    geoemtry column that has the latitude and longitude.
    """
    # create a geometry column that is Point objects
    geometry = [Point(xy) for xy in zip(df[LON_COL], df[LAT_COL])]
   
    # convert to geodataframe
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    return gdf

def plot_crime_hotspots_by_district(gdf, districts, year, dpi=150):
    """
    Takes in a geodataframe, a districts geodatafeame, and a year.
    Creates a plot of crime hotspots by district in Chicago for
    the specified year.
    """
    # group crimes by district and the number of times the crime occured
    crime_counts = gdf.groupby(CRIME_DISTRICT_COL).size()
    crime_counts = crime_counts.reset_index(name=CRIME_COUNT_COL)

    # make sure district numbers are in string format so it can merge
    crime_counts[CRIME_DISTRICT_COL] = crime_counts[CRIME_DISTRICT_COL] \
        .astype(float).astype(int).astype(str).str.strip()
    districts[SHAPE_DISTRICT_COL] = districts[SHAPE_DISTRICT_COL] \
        .astype(int).astype(str).str.strip()
   
    # merge crime data and drop rows where crime count is missing
    districts_merged = districts.merge(crime_counts, how='left',
                    left_on=SHAPE_DISTRICT_COL, right_on=CRIME_DISTRICT_COL)
    districts_merged = districts_merged.dropna(subset=[CRIME_COUNT_COL])

    # create plot
    plt.figure(figsize=(16, 12), dpi=dpi)
    ax = districts_merged.plot(column=CRIME_COUNT_COL, cmap='OrRd', \
                          edgecolor='black', legend=True, vmax=25000)
   
    # add titles and labe;s
    plt.title(f"Chicago's Crime Hotspots by District: {year}", \
              fontsize=15, fontweight='bold')
    plt.xlabel('Longitude', fontsize=12)
    plt.ylabel('Latitude', fontsize=12)
    add_district_labels(ax)
    plt.tight_layout()
   
    # save and show fig
    plt.savefig(f"crime_hostpots_{year}.png")
    plt.show()

def plot_districts_by_most_common_arrest(gdf, districts, year, dpi=150):
    """
    Takes in a geodataframe, a districts geodataframe, and a year.
    Creates a plot that shows the most common arrest type in each
    district for the specified year.
    """
    # group crimes by district and crime type and then find most common crime
    # type that is in each district
    crimes_by_district = gdf.groupby([CRIME_DISTRICT_COL, CRIME_TYPE_COL]) \
                        .size().reset_index(name='Count')
    most_common_crimes = crimes_by_district.loc[crimes_by_district \
                        .groupby(CRIME_DISTRICT_COL)['Count'].idxmax()]
   
    # make sure district numbers are in string format
    most_common_crimes[CRIME_DISTRICT_COL] = most_common_crimes \
        [CRIME_DISTRICT_COL].astype(float).astype(int).astype(str).str.strip()
    districts[SHAPE_DISTRICT_COL] = districts[SHAPE_DISTRICT_COL] \
        .astype(int).astype(str).str.strip()
   
    # merge common crime data with district boundaries
    districts_merged = districts.merge(most_common_crimes, how='left',
                                       left_on=SHAPE_DISTRICT_COL,
                                       right_on=CRIME_DISTRICT_COL)
   
    # drop rows where crime type is missing
    districts_merged = districts_merged.dropna(subset=[CRIME_TYPE_COL])
   
    # map each crime type tp a color
    unique_crime_types = districts_merged[CRIME_TYPE_COL].unique()
    colors = plt.get_cmap('tab20')(range(len(unique_crime_types)))
    color_map = dict(zip(unique_crime_types, colors))
    districts_merged['color'] = districts_merged[CRIME_TYPE_COL].map(color_map)

    # create plot
    plt.figure(figsize=(16, 12), dpi=dpi)
    ax = districts_merged.plot(color=districts_merged['color'],
                               edgecolor='black')

    # Set aspect ratio and add a legend
    ax.set_aspect(aspect=1.2)
    handles = [plt.Line2D([0], [0], marker='o', color='w',
                markerfacecolor=color_map[crime],
                markersize=10, label=crime)
               for crime in unique_crime_types]
    plt.legend(handles=handles, title="Most Common Arrest Type", \
               loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)
   
    # add title and labels
    plt.title(f'Most Common Arrest Type - {year}', fontsize=15,
              fontweight='bold')
    plt.xlabel('Longitude', fontsize=12)
    plt.ylabel('Latitude', fontsize=12)
    add_district_labels(ax)
    plt.tight_layout()
   
    # save and show fig
    plt.savefig(f"most_common_arrests_{year}.png")
    plt.show()
 


def plot_arrest_locations_by_crime_type(gdf, districts, crime_type, year,
                                        dpi=150):
    """
    Takes in a geodataframe, a districts geodataframe,crime type, and a year.
    Creates a hexbin plot showing the locations in Chicagoe of where arrests
    took place for the crime type that was chosen.
    """
    # clean crime type column bu uppercasing all strings
    gdf[CRIME_TYPE_COL] = gdf[CRIME_TYPE_COL].str.upper()

    # Filter geodataframe for the specific crime type
    specific_crimes = gdf[(gdf['Year'] == year) & (gdf[CRIME_TYPE_COL] ==
                                                   crime_type.upper())]

    # choose a color scheme
    cmap = sns.color_palette("coolwarm", as_cmap=True)

    # adjust grid size based on the number of data points
    gridsize = max(10, min(50, len(specific_crimes) // 200))

    # Create the plot
    plt.figure(figsize=(16, 12), dpi=dpi)
    ax = districts.plot(color='#e0e0e0', edgecolor='#333333', linewidth=0.7)
    hb = plt.hexbin(
        specific_crimes[LON_COL], specific_crimes[LAT_COL],
        gridsize=gridsize, cmap=cmap, mincnt=1, alpha=0.7, edgecolors='none',
        vmin=0, vmax=100
        )
    districts.boundary.plot(ax=ax, color='#333333', linewidth=1.5)

    # add color bar, titles, and labels
    plt.colorbar(hb, orientation='vertical')
    plt.title(f'{crime_type.capitalize()} Arrests in Chicago: {year}',
              fontsize=18, fontweight='bold')
    plt.xlabel('Longitude', fontsize=14)
    plt.ylabel('Latitude', fontsize=14)
    add_district_labels(ax)
   
    # save and show fig
    plt.savefig(f"{crime_type.capitalize()}_crime_distribution_{year}.png")
    plt.show()

def add_district_labels(ax):
    # northern district label
    ax.text(-87.72, 41.97, 'Northern Districts', fontsize=9, ha='center',
            color='black', weight='bold')
   
    # southern district label
    ax.text(-87.61, 41.69, 'Southern Districts', fontsize=9, ha='center',
            color='black', weight='bold')
   
    # eastern district label
    ax.text(-87.58, 41.90, 'Eastern Districts', fontsize=9, ha='center',
            color='black', weight='bold')

def main():   
    df = filter_chunk_data_by_year(CRIME_FILEPATH, YEAR)
    df = clean_data(df)
    gdf = geodataframe(df)
    districts = gpd.read_file(SHAPE_FILEPATH)

    plot_crime_hotspots_by_district(gdf, districts, YEAR, dpi=400)
    plot_districts_by_most_common_arrest(gdf, districts, YEAR, dpi=400)
    plot_arrest_locations_by_crime_type(gdf, districts,
                                        crime_type=CHOSEN_CRIME,
                                        year=YEAR, dpi=400)

if __name__ == "__main__":
    main()
 