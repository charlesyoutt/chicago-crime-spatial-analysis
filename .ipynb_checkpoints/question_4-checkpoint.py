#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

FILE_1 = 'Crimes_-_2001_to_Present.csv'
FILE_2 = 'Census_Data_-_Selected_socioeconomic_indicators_in_Chicago__2008___\
2012.csv'
percentage_col = ['PERCENT OF HOUSING CROWDED',
                  'PERCENT HOUSEHOLDS BELOW POVERTY',
                  'PERCENT AGED 16+ UNEMPLOYED',
                  'PERCENT AGED 25+ WITHOUT HIGH SCHOOL DIPLOMA',
                  'PERCENT AGED UNDER 18 OR OVER 64',
                  'HARDSHIP INDEX']

def normalize_df(df):
    '''
    Go over a dataframe and normalize all columns
    '''
    df_normalized = (df - df.min()) / (df.max() - df.min())
    return df_normalized

def filter_df(df_crime):
    '''
    Keep only the data from 2008 to 2012 and filtered out the rows with 
    community area number equal 0 or NaN, then convert the column into int.
    '''
    # keep data from 2008-2012
    df_filtered = df_crime[(df_crime['Year'] >= 2008) 
                           & (df_crime['Year'] <= 2012)]
    
    # No area 0
    df_filtered = df_filtered[df_filtered['Community Area'] != 0]
    
    # drop NaN
    df_filtered = df_filtered.dropna(subset=['Community Area'])
    
    # Change the data type
    df_filtered['Community Area'] = df_filtered['Community Area'].astype(int)
    
    return df_filtered

def KMeans_clustering(community_data):
    '''
    Using KMeans to analyze each community area's crime level by its crime 
    count, arrest rate, domestic rate. Then using the centroids to determine 
    the crime level labels
    '''
    kmeans = KMeans(n_clusters=3, random_state= 20)
    community_data['Cluster'] = kmeans.fit_predict(community_data)
    
    # Getting the centroids of each cluster
    centroids = kmeans.cluster_centers_

    # Create a dataframe to save centroids data
    centroid_df = pd.DataFrame(centroids, columns=community_data.columns[:-1])

    # Sorted the centroids data by the crime count and determine the crime 
    # level
    sorted_centroids = centroid_df.sort_values(by='Crime Count', 
                                               ascending=False)
    crime_levels = ['High', 'Moderate', 'Low']
    sorted_centroids['Crime Level'] = crime_levels
    cluster_labels = sorted_centroids['Crime Level'].to_dict()
    
    # Assging the clustering label with the crime level
    community_data['Crime Level'] = community_data['Cluster']\
    .map(cluster_labels)
    
    return community_data

def logistic_regression(merged_df):
    '''
    Using multiple logistic regression to train a model, which allows us to 
    predict the crime level by a community area's characteristics
    '''
    # Preparing the independent data, normalization
    independent = merged_df[percentage_col]
    independent = normalize_df(independent)
    
    X_train, X_test, y_train, y_test = train_test_split(independent, 
                                                        merged_df['Cluster'], 
                                                        test_size=0.2, 
                                                        random_state=44)

    # Training the model
    model = LogisticRegression(multi_class='multinomial')
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    return model, X_train, y_test, y_pred

def plot_crime_level(community_data):
    '''
    Plot a graph showing the distribution of crime level of each community 
    area
    '''
    crime_level_counts = community_data['Crime Level'].value_counts()

    plt.figure(figsize=(8, 6))
    bars = plt.bar(crime_level_counts.index, crime_level_counts.values,
                   color=['#440154', '#3b528b', '#21908d'])

    for bar in bars:
        y_val = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, y_val , int(y_val), 
                 ha='center', va='bottom')

    plt.title('Distribution of Crime Levels')
    plt.xlabel('Crime Level')
    plt.ylabel('Number of Communities')
    plt.show()

def plot_confusion(y_test, y_pred):
    '''
    Plot the confusion matrix of the regression model
    '''
    confusion_matrix(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Spectral')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix for Regression Model')
    plt.show()
    
def main():
    df_crime = pd.read_csv(FILE_1)
    df_census = pd.read_csv(FILE_2)
    
    # Filtering the data
    df_filtered = filter_df(df_crime)
    
    # Compute the crime counts for each community
    crime_counts = df_filtered['Community Area'].value_counts().sort_index()
    
    # Compute the arrest rate for each community
    arrest_rate = df_filtered.groupby('Community Area')['Arrest'].mean()\
    .sort_index()
    
    # Compute the domestic rate for each community
    domestic_rate = df_filtered.groupby('Community Area')['Domestic'].mean()\
    .sort_index()
    
    # Gathering data
    community_data = pd.DataFrame({'Crime Count': crime_counts, 
                                   'Arrest Rate': arrest_rate, 
                                   'Domestic Rate': domestic_rate})
    
    # Clustering the data
    community_data = KMeans_clustering(community_data)
    
    # Plot the crime level distribution
    plot_crime_level(community_data)
    
    # Merging the data
    merged_df = pd.merge(community_data, df_census, left_on='Community Area',
                         right_on = 'Community Area Number', how='right')
    merged_df = merged_df.dropna()
    
    # Training the model and print a report about it
    logistic_model, X_test, y_test, y_pred = logistic_regression(merged_df)
    print(classification_report(y_test, y_pred))
    
    # Plot the confusion matrix
    plot_confusion(y_test, y_pred)
    
if __name__ == "__main__":
    main()