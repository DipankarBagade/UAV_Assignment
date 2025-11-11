import pandas as pd
import numpy as np
from geopy.distance import geodesic
import path

class Deconflict:
    def __init__(self, paths, spatial_threshold = 5,temporal_threshold = 5):
        """Initialize with a Paths object containing the primary path and multiple sim paths."""
        self.primary_path = paths.primary_path  # The primary path (self.paths.primary_path)
        self.sim_paths = paths.sim_paths  # List of simulation paths (self.paths.sim_paths)

        self.spatial_conflict_results = self.check_spatial_conflict(spatial_threshold)
        self.spatial_temporal_conflict_results = self.check_temporal_spatial_conflict(temporal_threshold)
        print(self.get_conflict_summary())

    def calculate_3d_distance(self, coord1, coord2):
        """Calculate the 3D distance between two points considering lat, lon, and alt."""
        lat1, lon1, alt1 = coord1
        lat2, lon2, alt2 = coord2
        
        # Calculate 2D distance (latitude, longitude)
        horizontal_distance = geodesic((lat1, lon1), (lat2, lon2)).meters
        
        # Calculate vertical distance (altitude)
        vertical_distance = abs(alt1 - alt2)
        
        # Calculate the 3D Euclidean distance
        distance = np.sqrt(horizontal_distance**2 + vertical_distance**2)
        
        return distance

    def find_points_within_threshold(self, df1, df2, spatial_threshold):
        """Find points within the threshold distance in 3D space (lat, long, alt)."""
        indices_df1 = []
        indices_df2 = []
        
        # Iterate through all points in df1
        for i, row1 in df1.iterrows():
            lat1, lon1, alt1 = row1[['lat', 'long', 'alt']]
            
            # Compare with every point in df2
            for j, row2 in df2.iterrows():
                lat2, lon2, alt2 = row2[['lat', 'long', 'alt']]
                
                # Calculate the 3D distance
                distance = self.calculate_3d_distance((lat1, lon1, alt1), (lat2, lon2, alt2))
                
                # If the distance is less than the threshold, store the indices
                if distance < spatial_threshold:
                    indices_df1.append(i)
                    indices_df2.append(j)
        
        return indices_df1, indices_df2

    def check_spatial_conflict(self, spatial_threshold):
        """Check deconflict between the primary path and all sim paths based on the threshold distance."""
        spatial_conflict_results = []
        
        # Compare the primary path against each simulation path
        for i, sim_path in enumerate(self.sim_paths):
            df1 = self.primary_path.wp_data  # DataFrame of the primary path waypoints
            df2 = sim_path.wp_data  # DataFrame of the current simulation path waypoints
                
            # Find points within the threshold distance
            indices_df1, indices_df2 = self.find_points_within_threshold(df1, df2, spatial_threshold)
                
            if indices_df1:  # If there are any conflicts
                spatial_conflict_results.append({
                    'sim_path': i,
                    'indices_df1': indices_df1,
                    'indices_df2': indices_df2
                })
        
        return spatial_conflict_results
    
    def check_temporal_spatial_conflict(self, temporal_threshold):
        """Check for temporal conflicts."""

        temporal_conflicts = []

        for conflict in self.spatial_conflict_results:
            indices_df1 = conflict['indices_df1']
            indices_df2 = conflict['indices_df2']
            sim_path_idx = conflict['sim_path']
            
            temporal_indices_df1 = []
            temporal_indices_df2 = []

            # Compare each conflicting pair for temporal conflict
            for i, j in zip(indices_df1, indices_df2):
                # Get the time for each conflicting point
                time1 = self.primary_path.wp_data.loc[i, 'timestamp']
                time2 = self.sim_paths[sim_path_idx].wp_data.loc[j, 'timestamp']
                
                # Temporal conflict check: Time difference between points
                time_diff = abs(time1 - time2)
                
                # If time difference is below the temporal threshold, consider it a temporal conflict
                if time_diff <= temporal_threshold:
                    temporal_indices_df1.append(i)
                    temporal_indices_df2.append(j)

            # If any temporal conflicts were found, record them
            if temporal_indices_df1:
                temporal_conflicts.append({
                    'sim_path': sim_path_idx,
                    'indices_df1': temporal_indices_df1,
                    'indices_df2': temporal_indices_df2
                })

        return temporal_conflicts

    def get_conflict_summary(self):
        summary_text = ""
        if len(self.spatial_temporal_conflict_results) > 0:
            self.conflict_bool = True
            summary_text += "Conflict Detected\n"
            
            conflict_indices_primary = set()
            for conflict in self.spatial_temporal_conflict_results:
                summary_text += f"sim drone: {conflict['sim_path']}\n"

                conflict_indices_primary.update(conflict['indices_df1'])

                for conflict_idx in conflict_indices_primary:
                    lat,long,alt,timestamp = self.primary_path.wp_data.iloc[conflict_idx] 
                    summary_text += f"location:\nlatitude:{lat}\nlongitude:{long}\naltitude:{alt}\ntime:{timestamp}\n"
        else:
            self.conflict_bool = False
            summary_text += "Path Clear"

        return summary_text