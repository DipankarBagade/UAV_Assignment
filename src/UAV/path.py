import pandas as pd
import numpy as np
from geopy.distance import geodesic
import json
import glob
import os

class Path:
    def __init__(self, path_csv, path_json):
        self.waypoints = []
        self.wp_data = self.load_csv(path_csv)
        self.start_time,self.end_time = self.load_json(path_json)
        self.duration = self.end_time - self.start_time
        self.num_waypoints = len(self.wp_data)
        self.wp_data = self.interpolate()
        #print(self.wp_data)

    def load_csv(self, path_csv):
        return(pd.read_csv(path_csv))

    def load_json(self, path_json):
        with open(path_json, 'r') as file:
            data = json.load(file)
            start_time = data['T_start']
            end_time = data['T_end']
        return (start_time,end_time)
    
    def calculate_total_distance(self):
        """Calculates total distance along the waypoints."""
        total_distance = 0.0
        for i in range(1, len(self.wp_data)):
            coord1 = (self.wp_data.loc[i-1, 'lat'], self.wp_data.loc[i-1, 'long'])
            coord2 = (self.wp_data.loc[i, 'lat'], self.wp_data.loc[i, 'long'])
            total_distance += geodesic(coord1, coord2).meters  # Distance in meters
        return total_distance

    def interpolate(self):
        """Interpolates waypoints to ensure equidistant points."""
        interpolated_points = []
        total_points = self.duration  # Total points based on time difference

        for i in range(len(self.wp_data) - 1):
            lat1, lon1, alt1 = self.wp_data.loc[i, ['lat', 'long', 'alt']]
            lat2, lon2, alt2 = self.wp_data.loc[i + 1, ['lat', 'long', 'alt']]

            # Interpolate waypoints between each pair
            segment_points = max(2, total_points // (self.num_waypoints - 1))
            lats = np.linspace(lat1, lat2, segment_points)
            lons = np.linspace(lon1, lon2, segment_points)
            alts = np.linspace(alt1, alt2, segment_points)
            times = np.linspace(self.start_time, self.end_time, total_points, dtype=int)

            # Store interpolated points with corresponding times
            for j in range(segment_points):
                interpolated_points.append([lats[j], lons[j], alts[j], times[len(interpolated_points)]])
        
        return pd.DataFrame(interpolated_points, columns=['lat', 'long', 'alt', 'timestamp'])

class Paths:
    def __init__(self, sim_data_path='data/', primary_path_csv='primary_drone.csv', primary_path_json='primary_drone.json'):
        self.folder_path = sim_data_path
        self.sim_paths = self.load_sim_paths()

        primary_csv = os.path.join(os.getcwd(), primary_path_csv)
        primary_json = os.path.join(os.getcwd(), primary_path_json)
        
        # Load the primary path
        self.primary_path = Path(primary_csv, primary_json)

    def load_sim_paths(self):
        """Loads all sim_drone_*.csv and sim_drone_*.json files and creates Path objects."""
        # Find all matching CSV and JSON files
        csv_files = glob.glob(os.path.join(self.folder_path, "sim_drone_*.csv"))
        json_files = glob.glob(os.path.join(self.folder_path, "sim_drone_*.json"))
        
        sim_paths = []
        
        # Ensure each CSV and JSON corresponds to the same number
        for csv_file in csv_files:
            # Match the CSV file with its corresponding JSON file
            json_file = csv_file.replace(".csv", ".json")
            if json_file in json_files:
                # Create a Path object and add it to the paths list
                sim_paths.append(Path(csv_file, json_file))
            else:
                raise FileNotFoundError("File not found: " + json_file)

        return sim_paths