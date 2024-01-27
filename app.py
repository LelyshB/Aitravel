from flask import Flask, jsonify, render_template, request, redirect, url_for
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
import csv
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from flask_cors import CORS
import os
import glob


# Data collection functions
def scrape_travel_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    destination_data = []

    # Find the relevant elements containing destination information on the webpage
    destinations = soup.find_all('div', class_='destination')

    for destination in destinations:
        name = destination.find('h2').text
        location = destination.find('span', class_='location').text
        activities = [activity.text for activity in destination.find_all('span', class_='activity')]
        costs = {
            'accommodation': float(destination.find('span', class_='accommodation-cost').text),
            'transportation': float(destination.find('span', class_='transportation-cost').text),
            'food': float(destination.find('span', class_='food-cost').text),
            'activities': float(destination.find('span', class_='activities-cost').text)
        }

        destination_data.append({
            'name': name,
            'location': location,
            'activities': activities,
            'costs': costs
        })

    return destination_data

def save_data_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'location', 'activities', 'costs']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

def collect_data():
    url = 'file:///C:/Users/User/Desktop/travel/index.html'  
    travel_data = scrape_travel_data(url)
    save_data_to_csv(travel_data, 'travel_data.csv')

# Data preprocessing functions
def preprocess_data(filename):
    data = pd.read_csv(filename)
    data.fillna(method='ffill', inplace=True)
    data['activities'] = data['activities'].apply(lambda x: x.strip('][').split(', '))
    data['costs'] = data['costs'].apply(lambda x: eval(x))
    data['accommodation_cost'] = data['costs'].apply(lambda x: x['accommodation'])
    data['transportation_cost'] = data['costs'].apply(lambda x: x['transportation'])
    data['food_cost'] = data['costs'].apply(lambda x: x['food'])
    data['activities_cost'] = data['costs'].apply(lambda x: x['activities'])
    data.drop(columns=['costs'], inplace=True)
    return data

def save_preprocessed_data_to_csv(data, filename):
    data.to_csv(filename, index=False)

# Clustering function
def cluster_destinations(data, n_clusters=10):
    numerical_columns = ['accommodation_cost', 'transportation_cost', 'food_cost', 'activities_cost']
    numerical_data = data[numerical_columns]
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(numerical_data)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    cluster_labels = kmeans.fit_predict(normalized_data)
    return cluster_labels

# Main function to run data collection, preprocessing, and clustering
def main():
    raw_data_folder_path = 'C:\Users\User\Desktop\DATASET'
    preprocessed_data_filename = 'preprocessed_travel_data.csv'
    clustered_data_filename = 'clustered_travel_data.csv'

    # Collect data
    collect_data()

    # Read and combine CSV files from the folder
    all_csv_files = glob.glob(os.path.join(raw_data_folder_path, '*.csv'))
    list_of_dataframes = [pd.read_csv(file) for file in all_csv_files]
    combined_dataframe = pd.concat(list_of_dataframes, ignore_index=True, sort=False)

    # Preprocess data
    preprocessed_data = preprocess_data(combined_dataframe)

    # Cluster destinations
    cluster_labels = cluster_destinations(preprocessed_data)
    preprocessed_data['cluster'] = cluster_labels

    # Save the preprocessed and clustered data to a CSV file
    save_preprocessed_data_to_csv(preprocessed_data, clustered_data_filename)

    # Check the preprocessed and clustered data
    print(preprocessed_data.head())

if __name__ == '__main__':
    main()


app = Flask(__name__)

# Load clustered_data.csv directly for simplicity
clustered_data = pd.read_csv('clustered_travel_data.csv')

@app.route('/')
def index():
    return render_template('plan.html')

@app.route('/submit', methods=['POST'])
def submit():
    budget_from = int(request.form['budget-from'])
    budget_to = int(request.form['budget-to'])
    budget = (budget_from + budget_to) / 2
    preferences = request.form.getlist('preferences[]')
    travel_date_from = request.form['travel-date-from']
    travel_date_to = request.form['travel-date-to']
    travel_dates = [travel_date_from, travel_date_to]
    
    def recommend_destination(budget, preferences, travel_dates, clustered_data):
        # Filter destinations based on the user's budget
        filtered_data = clustered_data[
            (clustered_data['accommodation_cost'] + clustered_data['transportation_cost'] + 
            clustered_data['food_cost'] + clustered_data['activities_cost']) <= budget
        ]

        # Filter destinations based on the user's preferences
        for preference in preferences:
            filtered_data = filtered_data[filtered_data[preference] == True]

        # Filter destinations based on the user's fears

        fears = request.form.getlist('fear[]')
        for fear in fears:
            filtered_data = filtered_data[filtered_data[fear] == False]

        # Pick a destination from the filtered data
        if not filtered_data.empty:
            recommended_destination = filtered_data.sample(n=1).iloc[0]
            return recommended_destination
        else:
            return None

    recommended_destination = recommend_destination(budget, preferences, travel_dates, clustered_data)

    if recommended_destination is not None:
        result = {
            "name": recommended_destination['name'],
            "location": recommended_destination['location'],
            "activities": json.loads(recommended_destination['activities']),
            "cluster": recommended_destination['cluster']
        }
    else:
        result = {"error": "No suitable destination found within the specified budget and preferences."
        }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
