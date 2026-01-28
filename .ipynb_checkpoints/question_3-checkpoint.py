#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:49:54 2024

@author: Samantha Pierre
Class: DS 2500
Assignment: Final project
Date: August 16, 2024
Work cited: I used the csv file from data.gov the one from crime 2001 to 
present. Used the code from previous assigns as a guide, looked at previous
Lecture code nd google searched the documention. 
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


"""
The function prepare data is turning the arrest column into a binary variable.
If there was an arrest that was made then 1 but if there wasn't any arrest 
any arrest made then 0. 
"""
def prepare_data(df):
    df['Arrest'] = df['Arrest'].apply(lambda x: 1 if x else 0)

    # Selects only the Primary Type and Arrest
    df = df[['Primary Type', 'Arrest']]
    # Removes rows where primary type is non-criminal. I only wanted Criminal.
    df = df[df['Primary Type'] != 'NON-CRIMINAL']

    # The rows with missing values are dropped.
    df.dropna(inplace=True)

    return df

def calculate_arrest_rates(df):
    """
    They are grouped by 'Primary Type' the arrest rate for each crime type 
    calculates the mean for it. 
    """
    arrest_rate = df.groupby('Primary Type')['Arrest'].mean()
    return arrest_rate


''' 
    Provides clarity to the plot because of the big fonts size to help 
    make it easier to read the plot. for the function plot_arrest_rates
'''
def plot_arrest_rates(arrest_rate):
    # Meant to help with better clarity
    plt.figure(figsize=(14, 12), dpi=150) 
    sns.barplot(x=arrest_rate.values, y=arrest_rate.index, palette='deep')

    # This is the title and labels
    plt.title('Arrest Rate by Crime Type', fontsize=20)
    plt.xlabel('Arrest Rate', fontsize=16)
    plt.ylabel('Crime Type', fontsize=16)
  


    # This is for the font size to make it easier to read/
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    # This part helps with making the axis have a smoother appearance.
    for spine in plt.gca().spines.values():
        spine.set_antialiased(True)

    plt.show()
""" 
analzye_arrest_rates preps data,the calculates the actual arrest rates,
and then it plots the results.

"""  
def analyze_arrest_rates(df):
    df_prepared = prepare_data(df)
    arrest_rate = calculate_arrest_rates(df_prepared)
    # prints the arrest by crime type
    print("Arrest Rate by Crime Type:\n", arrest_rate)
    plot_arrest_rates(arrest_rate)
    

def main():

    df_one = pd.read_csv("/Users/samanthapierre/Desktop/DS2500/Crimes_\
-_2001_to_Present.csv") 
    # this just prints out the first few rowa of the dataframe.
    print(df_one)
    # This just prints all the names in the dataframe
    print("Columns in the DataFrame:", df_one.columns.tolist())

    data = {
       'crime_type': ['Theft', 'Assault', 'Burglary', 'Theft', 'Assault',\
                    'Burglary', 'Theft', 'Assault', 'Burglary'],
       'arrest_made': ['Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', \
                       'Yes']
   }
    # Displays the unique crimes 
    print(df_one['Primary Type'].unique())


    df = pd.DataFrame(data)

   # Counts the number of arrests and non-arrests per crime type
    arrest_counts = df.groupby(['crime_type', 'arrest_made']).size()\
   .unstack(fill_value=0)

   # Calculate percentages of the two (arrests and non-arrests )
    percentages = arrest_counts.div(arrest_counts.sum(axis=1), axis=0) * 100

   # Plotting the bar chart
    ax = percentages.plot(kind='bar', stacked=True, color=['black', 'brown'])

   # This annotating the bars so that they can display exact percentages
    for p in ax.patches:
       width = p.get_width()
       height = p.get_height()
       x, y = p.get_xy() 
       ax.text(x + width / 2, y + height / 2, f'{height:.1f}%', ha='center',\
       va='center', color='white', fontsize=10)

    plt.title('Percentage of Crimes Leading to Arrest vs. No Arrest')
    plt.xlabel('Crime Type')
    plt.ylabel('Percentage of Incidents')
    plt.legend(title='Arrest Made')

   # Displays plot
    plt.show()

    # Displays the arrest rates
    analyze_arrest_rates(df_one)
    


if __name__ == "__main__":
    main()  

