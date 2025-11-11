import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import path,deconflict

def visualize_paths(paths):
    """Visualizes the paths in 3D space using Matplotlib."""

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    lat = paths.primary_path.wp_data['lat']
    long = paths.primary_path.wp_data['long']
    alt = paths.primary_path.wp_data['alt']
    
    # Plot the path in 3D space
    ax.plot(lat, long, alt, label="primary drone",color='green')

    # Iterate over each Path object in the Paths instance
    for i,path in enumerate(paths.sim_paths):
        # Extract lat, long, and alt data from each path
        
        lat = path.wp_data['lat']
        long = path.wp_data['long']
        alt = path.wp_data['alt']
        
        # Plot the path in 3D space
        ax.plot(lat, long, alt, label=f"sim drone: {i}")

    # Set labels for the axes
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Altitude (m)')

    ax.set_title('Flight Plan')

    # Show legend
    ax.legend()
    ax.set_zlim([0, alt.max() + 10]) 

    # Display the plot
    plt.show()

def visualize_conflicts(paths,deconflict_results):
    """Visualizes the paths in 3D space with enhanced conflict markers."""

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    # Set dark background for better contrast
    ax.set_facecolor('#1a1a1a')
    fig.patch.set_facecolor('#2d2d2d')

    lat = paths.primary_path.wp_data['lat']
    long = paths.primary_path.wp_data['long']
    alt = paths.primary_path.wp_data['alt']
    
    # Plot the primary path in 3D space
    ax.plot(lat, long, alt, label="Primary Drone", color='#00ff88', linewidth=2, alpha=0.8)

    # Iterate over each Path object in the Paths instance
    colors = ['#00d4ff', '#ff9500', '#ff00ff', '#ffff00']  # Different colors for sim drones
    for i, path in enumerate(paths.sim_paths):
        # Extract lat, long, and alt data from each path
        lat = path.wp_data['lat']
        long = path.wp_data['long']
        alt = path.wp_data['alt']
        
        # Plot the path in 3D space with distinct colors
        color = colors[i % len(colors)]
        ax.plot(lat, long, alt, label=f"Sim Drone {i+1}", color=color, linewidth=2, alpha=0.7)

    # Collect all conflicting indices
    conflicting_indices = []
    for conflict in deconflict_results:
        conflicting_indices.extend(conflict['indices_df1'])

    if conflicting_indices:
        # Remove duplicates and sort
        conflicting_indices = sorted(set(conflicting_indices))
        
        lat_conflict = paths.primary_path.wp_data.loc[conflicting_indices, 'lat']
        long_conflict = paths.primary_path.wp_data.loc[conflicting_indices, 'long']
        alt_conflict = paths.primary_path.wp_data.loc[conflicting_indices, 'alt']

        # Plot conflict zones with multiple visual indicators
        # 1. Large red spheres for conflict points
        ax.scatter(lat_conflict, long_conflict, alt_conflict, 
                  label="⚠ CONFLICT ZONE", 
                  color='red', 
                  s=300, 
                  alpha=0.8,
                  edgecolors='yellow',
                  linewidths=3,
                  marker='o')
        
        # 2. Add smaller inner markers for emphasis
        ax.scatter(lat_conflict, long_conflict, alt_conflict, 
                  color='yellow', 
                  s=100, 
                  alpha=1.0,
                  marker='*')
        
        # 3. Add vertical lines from ground to conflict points for better visibility
        for lat_c, long_c, alt_c in zip(lat_conflict, long_conflict, alt_conflict):
            ax.plot([lat_c, lat_c], [long_c, long_c], [0, alt_c], 
                   color='red', 
                   linestyle='--', 
                   linewidth=2, 
                   alpha=0.5)

    ax.set_zlim([0, alt.max() + 10]) 

    # Set labels for the axes with better styling
    ax.set_xlabel('Latitude', fontsize=12, fontweight='bold', color='white')
    ax.set_ylabel('Longitude', fontsize=12, fontweight='bold', color='white')
    ax.set_zlabel('Altitude (m)', fontsize=12, fontweight='bold', color='white')
    
    # Style the tick labels
    ax.tick_params(colors='white', labelsize=9)
    
    # Set title with conflict count
    conflict_count = len(conflicting_indices) if conflicting_indices else 0
    title = f'⚠ CONFLICT VISUALIZATION - {conflict_count} Conflict Points Detected' if conflict_count > 0 else 'Conflict Visualization - No Conflicts'
    ax.set_title(title, fontsize=14, fontweight='bold', color='#ff3366' if conflict_count > 0 else '#00ff88', pad=20)

    # Customize legend
    legend = ax.legend(loc='upper left', fontsize=10, framealpha=0.9, facecolor='#2d2d2d', edgecolor='#00d4ff')
    for text in legend.get_texts():
        text.set_color('white')

    # Set grid with custom styling
    ax.grid(True, alpha=0.3, color='#00d4ff', linestyle='--', linewidth=0.5)
    
    # Adjust viewing angle for better perspective
    ax.view_init(elev=25, azim=45)

    # Display the plot
    plt.tight_layout()
    plt.show()


def visualize_flight(paths):
    """Visualizes the UAV paths in 3D space with animation."""
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('Flight Visualization (4D)')
    # Primary path data
    primary_df = paths.primary_path.wp_data
    primary_lat = primary_df['lat']
    primary_long = primary_df['long']
    primary_alt = primary_df['alt']
    primary_time = primary_df['timestamp']
    
    # Get primary drone start and end time
    start_time, end_time = paths.primary_path.start_time, paths.primary_path.end_time
    
    # Plot static paths
    ax.plot(primary_lat, primary_long, primary_alt, label="primary drone", color='green')
    for i,path in enumerate(paths.sim_paths):
        ax.plot(path.wp_data['lat'], path.wp_data['long'], path.wp_data['alt'], label=f"sim drone: {i}")
    
    # Set axis labels
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Altitude')
    ax.legend()
    
    # Scatter points for animation
    primary_scatter, = ax.plot([], [], [], 'ro', label='Primary Drone')
    sim_scatters = [ax.plot([], [], [], 'go', label=f'Sim Drone {i}')[0] for i in range(len(paths.sim_paths))]
    
    def update(frame):
        current_time = start_time + frame
        
        # Update primary drone position
        idx = (primary_time <= current_time).sum() - 1
        if idx >= 0:
            primary_scatter.set_data([primary_lat.iloc[idx]], [primary_long.iloc[idx]])
            primary_scatter.set_3d_properties([primary_alt.iloc[idx]])
            primary_scatter.set_visible(True)
        else:
            primary_scatter.set_visible(False)
        
        # Update simulation drones' positions
        for i, path in enumerate(paths.sim_paths):
            sim_time = path.wp_data['timestamp']
            sim_lat, sim_long, sim_alt = path.wp_data['lat'], path.wp_data['long'], path.wp_data['alt']
            
            # Check if sim drone should be visible
            if sim_time.min() <= current_time <= sim_time.max():
                sim_idx = (sim_time <= current_time).sum() - 1
                if sim_idx >= 0:
                    sim_scatters[i].set_data([sim_lat.iloc[sim_idx]], [sim_long.iloc[sim_idx]])
                    sim_scatters[i].set_3d_properties([sim_alt.iloc[sim_idx]])
                    sim_scatters[i].set_visible(True)
            else:
                sim_scatters[i].set_visible(False)  # Hide drone
                
        return [primary_scatter] + sim_scatters

    # Create animation
    frames = int(end_time - start_time) + 1
    ani = FuncAnimation(fig, update, frames=frames, interval=100, blit=True)
    
    plt.show()
