from PIL import Image
import numpy as np
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

def center_silhouette_and_save(file_path):
    # Load the image
    try:
        img = Image.open(file_path)
    except IOError:
        print(f"Error: Cannot open the image at {file_path}")
        return

    # Convert to RGB if not
    if img.mode != 'RGB':
        img = img.convert('RGB')

    img_array = np.array(img)

    # Check if the image array is empty
    if img_array.size == 0:
        print("Error: The image is empty.")
        return

    # Find non-white pixels (assuming white is [255, 255, 255])
    rows, cols = np.where(~np.all(img_array == [255, 255, 255], axis=2))

    # Check if any non-white pixels are found
    if rows.size == 0 or cols.size == 0:
        print(f"No silhouette found in the image at {file_path}.")
        return

    # Calculate the bounding box of the silhouette
    min_row, max_row = rows.min(), rows.max()
    min_col, max_col = cols.min(), cols.max()

    # Cropping to the silhouette
    cropped_img = img.crop((min_col, min_row, max_col, max_row))

    # Resize while maintaining aspect ratio within 98x98 area
    aspect_ratio = cropped_img.width / cropped_img.height
    if aspect_ratio > 1:
        # Width is greater than height
        new_width = 98
        new_height = int(98 / aspect_ratio)
    else:
        # Height is greater than or equal to width
        new_height = 98
        new_width = int(98 * aspect_ratio)

    resized_img = cropped_img.resize((new_width, new_height), Image.NEAREST)

    # Create a new 100x100 white image
    new_img = Image.new("RGB", (100, 100), "white")
    # Calculate the position to paste (1px margin)
    x = (100 - new_width) // 2
    y = (100 - new_height) // 2
    new_img.paste(resized_img, (x, y))

    # Check if the new 100x100 image is fully white
    new_img_array = np.array(new_img)
    if np.all(new_img_array == [255, 255, 255]):
        print(f"The resulting image is fully white. Deleting the original image at {file_path}.")
        os.remove(file_path)
        return
    else:
        # Save the result if it's not fully white
        new_img.save(file_path)
        # print(f"Image saved as {file_path}")

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

    filename = f'{output_dir}{country}.png'

    # Plot and save the image
    fig, ax = plt.subplots()
    # country_projected.plot(ax=ax, color='black' , edgecolor='red', linewidth=2)
    country_projected.plot(ax=ax, color='black')
    plt.axis('off')
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    # print(f'Saved {country}')

    center_silhouette_and_save(filename)