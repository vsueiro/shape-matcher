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

# TODO: Get more detailed shapes

# Nauru (looks like a blob)
# Monaco (looks like a blob)
# Vatican (looks like a blob)

# TODO: Remove locations

# Bajo Nuevo Bank (Petrel Is.)
# Bir Tawil * Kinda intersting tho
# Brazilian Island
# Federated States of Micronesia (too tiny?)
# Kiribati (too tiny?)
# Maldives (too tiny?)
# Marshall Islands (too tiny?)
# Scarborough Reef
# Serranilla Bank
# Seychelles (too tiny?)
# Spratly Islands (too tiny?)
# Tonga (too tiny?)
# Tuvalu (too tiny?)

# TODO: Remove parts of locations

# Antigua and Barbuda: remove tiny island
# Australia: remove tiny islands
# Brazil: remove tiny islands
# Chile: remove tiny islands
# Colombia: remove tiny islands
# Costa Rica: remove tiny islands
# Equador: remove Galápagos Islands
# Equatorial Guinea: remove Annobón
# Fiji: remove northenmost island and southernmost island
# France: remove all except continental France and Corse
# Honduras: remove northenmost island
# Netherlands: remove tiny islands
# New Zealand: remove tiny islands
# Norway: remove Svalbard and Jan Mayen
# Portugal: remove tiny islands
# South Africa: remove southernmost island
# Spain: remove Canary Islands
# United Kingdom: remove tiny islands
# United States of America: remove islands (including Alaska and Puerto Rico)
# Venezuela: remove northernmost island

# TODO: Split locations

# Denmark = Denmark, Greenland, Faroe Islands?

# TODO: Combine locations

# Cyprus + Cyprus No Mans Area + Northern Cyprus = Cyprus

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
  # country_projected.plot(ax=ax, color='black' , edgecolor='red', linewidth=2)
  country_projected.plot(ax=ax, color='black')
  plt.axis('off')
  plt.savefig(f'{output_dir}/{country}.png', bbox_inches='tight', pad_inches=0)
  plt.close(fig)

  print(f'Saved {country}')