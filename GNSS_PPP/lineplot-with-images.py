import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os
import mplcursors

# Path to merged_df CSV file
merged_file = '/home/s186/Documents/merged-data2.csv'  # Adjust the path as needed

# Load the merged_df data
merged_df = pd.read_csv(merged_file)

# Extract data from merged_df
latitudes = merged_df['latitude'].values
longitudes = merged_df['longitude'].values
speeds = merged_df['hor_speed'].values
image_paths = merged_df['image_path'].values

# Calculate distances between consecutive points
distances = [0]  # Starting point, distance is zero
for i in range(1, len(latitudes)):
    point1 = (latitudes[i-1], longitudes[i-1])
    point2 = (latitudes[i], longitudes[i])
    distance = geodesic(point1, point2).meters  # Calculate the distance in meters
    distances.append(distances[-1] + distance)  # Cumulative distance

# Convert distances to a numpy array
distances = np.array(distances)

# Print the total distance traveled
total_distance = distances[-1]
print(f'Total distance traveled: {total_distance:.2f} meters')

# Plot speed vs distance
fig, ax = plt.subplots(figsize=(10, 6))
sc = ax.scatter(distances, speeds, label='Speed vs Distance', color='b', s=10)  # Adjust marker size here
ax.set_xlabel('Distance (meters)')
ax.set_ylabel('Speed (m/s)')
ax.set_title('Speed vs Distance')
ax.legend()
ax.grid(True)

# Directory containing images
image_dir = '/home/s186/Documents/7/folder0/'  # Adjust the directory path as needed

# Initialize variables to keep track of displayed image and annotation
current_annotation = None
current_image = None

# Function to load and resize image
def get_image_with_info(path, lat, lon, speed, zoom=0.1):
    global current_annotation, current_image
    
    # Close previously displayed image and annotation
    if current_image is not None:
        plt.close(current_image)
    
    # Create new figure for the image
    current_image = plt.figure()
    image = plt.imread(path)
    plt.imshow(image)
    plt.axis('off')  # Hide axes
    plt.title(f"Latitude: {lat}, Longitude: {lon}, Speed: {speed} m/s")
    plt.show()

# Add interactive cursor
cursor = mplcursors.cursor(sc, hover=False)

# Define action on click
@cursor.connect("add")
def on_add(sel):
    idx = sel.index
    image_path = os.path.join(image_dir, image_paths[idx])  # Full path to the image
    if os.path.exists(image_path):
        lat = latitudes[idx]
        lon = longitudes[idx]
        speed = speeds[idx]
        get_image_with_info(image_path, lat, lon, speed)

plt.show()
