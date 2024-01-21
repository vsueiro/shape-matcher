from PIL import Image
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import random
# from shapely.geometry import MultiPolygon
from shapely.geometry import box

# Set the option to display all columns
pd.set_option('display.max_columns', None)

output_dir = './static/shapes/countries/'

# Check if output directory exists, if not, create it
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load Natural Earth map
world = gpd.read_file('./shape-files/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp')

# print(world[world["SOVEREIGNT"] == "Kazakhstan"])
# exit()

def clip_country_geometry(world_df, country_name, minx, miny, maxx, maxy):
    """
    Clips the geometry of a specified country within a GeoDataFrame to a given bounding box.

    Parameters:
    world_df (GeoDataFrame): The GeoDataFrame containing country geometries.
    country_name (str): The name of the country to clip.
    minx, miny, maxx, maxy (float): The minimum and maximum x and y coordinates of the bounding box.

    Returns:
    GeoDataFrame: The original GeoDataFrame with the specified country's geometry clipped.
    """

    # Create the bounding box
    bbox = box(minx, miny, maxx, maxy)

    # Isolate the specified country
    country = world_df[world_df['ADMIN'] == country_name]

    # Clip the country geometry with the bounding box
    country_clipped = gpd.clip(country, bbox)

    # Replace the original country geometry in the world DataFrame
    if not country_clipped.empty:
        world_df.loc[world_df['ADMIN'] == country_name, 'geometry'] = country_clipped.geometry.values[0]
    else:
        print(f"No part of {country_name} falls within the specified bounding box.")

    plot_country_multipolygons(world_df, country_name, 'test.png')

    return world_df

def plot_country_multipolygons(gdf, country_name, output_file):
    """
    Plots each polygon of a multipolygon geometry of a specified country in different colors.

    :param gdf: GeoDataFrame containing country geometries.
    :param country_name: The name of the country to plot.
    :param output_file: Path to save the output plot image.
    """

    # Get the geometry of the specified country
    country_geometry = gdf[gdf['ADMIN'] == country_name].geometry.iloc[0]

    # Check if the geometry is a MultiPolygon
    if country_geometry.geom_type == 'MultiPolygon':
        # Create a figure and axis for plotting
        fig, ax = plt.subplots()

        # Loop through each polygon in the MultiPolygon
        for polygon in country_geometry.geoms:
            # Generate a random color
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

            # Plot the polygon with the generated color
            gpd.GeoSeries([polygon]).plot(ax=ax, edgecolor=color, linewidth=3, facecolor=color)

        # Save the figure
        plt.savefig(output_file, dpi=300)
        # plt.show()
    else:
        print(f"The geometry of {country_name} is not a MultiPolygon.")

# Combine locations

# Cyprus
cyprus_areas = world[world['SOVEREIGNT'].isin(['Cyprus No Mans Area', 'Northern Cyprus', 'Cyprus'])]
world.loc[world['SOVEREIGNT'] == 'Cyprus', 'geometry'] = cyprus_areas.unary_union

# Kazakhstan and Baykonur Cosmodrome
kazakhstan_areas = world[world['SOVEREIGNT'].isin(['Kazakhstan'])]
world.loc[world['ADMIN'] == 'Kazakhstan', 'geometry'] = kazakhstan_areas.unary_union

# List of locations to remove
locations_to_remove = [
    "Bajo Nuevo Bank (Petrel Is.)",
    "Bir Tawil",
    "Brazilian Island",
    "Federated States of Micronesia",
    "Kiribati",
    "Maldives",
    "Marshall Islands",
    "Scarborough Reef",
    "Serranilla Bank",
    "Seychelles",
    "Spratly Islands",
    "Tonga",
    "Tuvalu",
    "Monaco", # looks like a blob
    "Vatican", # looks like a blob
    "Cyprus No Mans Area", # (merged
    "Northern Cyprus", # merged
    "Ashmore and Cartier Islands", # ADMIN
    "Clipperton Island", # ADMIN
    "Coral Sea Islands", # ADMIN
    "French Southern and Antarctic Lands", # ADMIN
    "Indian Ocean Territories", # ADMIN
    "Baykonur Cosmodrome", # ADMIN
    "Wallis and Futuna", # ADMIN
    "US Naval Base Guantanamo Bay", # ADMIN
    "Sint Maarten", # ADMIN
    "Saint Barthelemy", # ADMIN
    "Nauru", # ADMIN (too tiny)
]

# Remove locations
world = world[~world['SOVEREIGNT'].isin(locations_to_remove)]

world = world[~world['ADMIN'].isin(locations_to_remove)]

# Remove parts of locations

# United Kingdom: remove tiny islands
world = world[~((world['SOVEREIGNT'] == 'United Kingdom') & (world['SUBREGION'] != 'Northern Europe'))]

# Netherlands: keep only geometries near the main land
world = clip_country_geometry(world, 'Netherlands', -4, 46, 13, 55)

# Portugal: remove tiny islands
world = clip_country_geometry(world, 'Portugal', -12,35,-2,43)

# United States of America: remove Hawaii and Canada
world = clip_country_geometry(world, 'United States of America', -129.0,23.6,-59.3,50.2)

# France: remove tiny islands
world = clip_country_geometry(world, 'France', -6.41,38.11,12.87,51.89)

# Spain: remove Canary Islands
world = clip_country_geometry(world, 'Spain', -11.87,35.66,5.12,44.39)

# South Africa: remove tiny islands
world = clip_country_geometry(world, 'South Africa', 12.57,-36.33,36.66,-20.45)

# Equatorial Guinea: remove tiny islands
world = clip_country_geometry(world, 'Equatorial Guinea', 7.4759,0.4763,11.7965,4.2752)

# Norway: remove Svalbard
world = clip_country_geometry(world, 'Norway', 1.72,55.72,34.43,72.12)

# Antigua and Barbuda: remove tiny island
world = clip_country_geometry(world, 'Antigua and Barbuda', -62.1511,16.849,-61.4497,17.8856)

# Group by 'SOVEREIGNT' and combine geometries
grouped = world.groupby('ADMIN')

# TODO: Get more detailed shapes

# Nauru (looks like a blob)
# St Barthélemy (looks like a blob)

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
# 
# United States of America: remove islands (including Alaska and Puerto Rico)
# Venezuela: remove northernmost island

# TODO: Split locations

# Denmark = Denmark, Greenland, Faroe Islands?

def center_silhouette_and_save(file_path):
    width = 64
    height = 64
    margin = 1

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

    # Convert every pixel to black or white based on the average RGB value
    threshold = 128
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            if img_array[i, j].mean() > threshold:
                img_array[i, j] = [255, 255, 255]
            else:
                img_array[i, j] = [0, 0, 0]

    # Create an Image object from the modified array
    img = Image.fromarray(img_array)

    # Find non-white pixels (assuming white is [255, 255, 255])
    rows, cols = np.where(~np.all(img_array == [255, 255, 255], axis=2))

    # Check if any non-white pixels are found
    if rows.size == 0 or cols.size == 0:
        os.remove(file_path)
        print(f"Removed {file_path}")
        return

    # Calculate the bounding box of the silhouette
    min_row, max_row = rows.min(), rows.max()
    min_col, max_col = cols.min(), cols.max()

    # Cropping to the silhouette
    cropped_img = img.crop((min_col, min_row, max_col, max_row))

    # Check if the image is valid (non-zero width and height)
    if cropped_img.width == 0 or cropped_img.height == 0:
        print(f"Invalid dimensions {file_path} ({cropped_img.width}x{cropped_img.height})")
        os.remove(file_path)
        print(f"Removed {file_path}")
        return

    # Resize while maintaining aspect ratio within 98x98 area
    aspect_ratio = cropped_img.width / cropped_img.height
    if aspect_ratio > 1:
        # Width is greater than height
        new_width = width - (margin * 2)
        new_height = int(new_width / aspect_ratio)
    else:
        # Height is greater than or equal to width
        new_height = height - (margin * 2)
        new_width = int(new_height * aspect_ratio)

    resized_img = cropped_img.resize((new_width, new_height), Image.NEAREST)
    resized_img_array = np.array(resized_img)

    # Convert the resized image to black and white to ensure only these colors
    for i in range(resized_img_array.shape[0]):
        for j in range(resized_img_array.shape[1]):
            if resized_img_array[i, j].mean() > threshold:
                resized_img_array[i, j] = [255, 255, 255]
            else:
                resized_img_array[i, j] = [0, 0, 0]

    final_resized_img = Image.fromarray(resized_img_array)

    # Create a new 100x100 white image
    new_img = Image.new("RGB", (width, height), "white")
    # Calculate the position to paste (1px margin)
    x = (width - new_width) // 2
    y = (height - new_height) // 2
    new_img.paste(final_resized_img, (x, y))

    # Check if the new 100x100 image is fully white
    new_img_array = np.array(new_img)
    if np.all(new_img_array == [255, 255, 255]):
        os.remove(file_path)
        print(f"Removed {file_path}")
        return

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

    # Define the size of the figure in inches (for a 100x100 px image at 100 DPI)
    fig_size = 1 # 1 inch

    # Create the figure with the defined size
    fig, ax = plt.subplots(figsize=(fig_size, fig_size))

    # Plot the country
    # country_projected.plot(ax=ax, color='black' , edgecolor='red', linewidth=2)
    country_projected.plot(ax=ax, color='black')

    # Remove axis
    plt.axis('off')

    # Magic number is generating images with a maximum dimension of 200 pixels
    dpi = 300 * 1.3

    # Define file name
    filename = f'{output_dir}{country}.png'

    # Save the figure
    plt.savefig(filename, bbox_inches='tight', pad_inches=0, dpi=dpi)

    # Close the figure
    plt.close(fig)
    # print(f'Saved {country}')

    center_silhouette_and_save(filename)