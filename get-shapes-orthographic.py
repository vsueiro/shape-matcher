import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
from shapely.geometry import box

# Set the option to display all columns
pd.set_option('display.max_columns', None)

output_dir = './static/shapes/countries/'

# Check if output directory exists, if not, create it
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load Natural Earth map
world = gpd.read_file('./shape-files/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp')

# Group by 'SOVEREIGNT' and combine geometries
grouped = world.groupby('SOVEREIGNT')

# Loop through each country
for country, data in grouped:
  # Project geometries to a Cartesian coordinate system
  data_projected = data.to_crs(epsg=3857)

  # Calculate the centroid of the projected country
  centroid_projected = data_projected.geometry.centroid

  # Convert the centroid back to geographic coordinates
  centroid = centroid_projected.to_crs(epsg=4326).iloc[0]

  # Define the Orthographic projection centered on the centroid
  proj = f'+proj=ortho +lat_0={centroid.y} +lon_0={centroid.x}'

  # Reproject the original country geometry
  country_projected = data.to_crs(proj)

  # Plot and save the image
  fig, ax = plt.subplots()
  country_projected.boundary.plot(ax=ax)
  plt.axis('off')  # Turn off axis
  plt.savefig(f'{output_dir}/{country}.png', bbox_inches='tight', pad_inches=0)
  plt.close(fig)
