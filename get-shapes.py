import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
from shapely.affinity import translate, scale
from shapely.geometry import box

# Set the option to display all columns
pd.set_option('display.max_columns', None)

output_dir = './static/shapes/countries/'

# Load Natural Earth map
world = gpd.read_file('./shape-files/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp')

# Group by 'SOVEREIGNT' and combine geometries
grouped = world.groupby('SOVEREIGNT')

# Combine geometries
combined_geometries = grouped['geometry'].apply(lambda x: x.unary_union)

# Aggregate other columns. Adjust this based on your specific needs
aggregated_data = grouped.agg({
    'LABELRANK': 'first',
    'ISO_A2': 'first',
})

# Combine aggregated data with combined geometries
world_combined = aggregated_data.join(combined_geometries)

# Reset the index to make 'SOVEREIGNT' a column again, if needed
world_combined.reset_index(inplace=True)

# TODO: FIX -99 ISO_A2 for some countries

print(world_combined.shape)

def process_country(geometry):
    # Get the bounds of the geometry and calculate its dimensions and aspect ratio
    minx, miny, maxx, maxy = geometry.bounds
    width, height = maxx - minx, maxy - miny
    aspect_ratio = width / height

    # Scale the geometry to fit within the 100x100 boundary
    if aspect_ratio > 1:
        # Wider than tall: scale based on width
        scale_factor = 100 / width
    else:
        # Taller than wide: scale based on height
        scale_factor = 100 / height

    scaled_geo = scale(geometry, xfact=scale_factor, yfact=scale_factor, origin='center')

    # Center the scaled geometry in a 100x100 square
    minx, miny, maxx, maxy = scaled_geo.bounds
    x_offset = (100 - (maxx - minx)) / 2 - minx
    y_offset = (100 - (maxy - miny)) / 2 - miny
    final_geo = translate(scaled_geo, xoff=x_offset, yoff=y_offset)

    return final_geo


def save_country_image(geometry, name):
    fig, ax = plt.subplots(figsize=(1, 1), dpi=100)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_axis_off()
    gpd.GeoSeries(geometry).plot(ax=ax, color='black', edgecolor='red', linewidth=2)
    plt.gca().set_position([0, 0, 1, 1])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig(f'{output_dir}{name}.png', bbox_inches='tight', pad_inches=0)
    plt.close()

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Process and save each country
for index, row in world_combined.iterrows():
    geometry = process_country(row['geometry'])  # Pass only the geometry

    filename = f"{row['SOVEREIGNT'].replace(' ', '_')}-{row['ISO_A2']}"

    save_country_image(geometry, filename)

    print(f'Saved {filename}')

