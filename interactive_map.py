import os
import folium
import geopandas as gpd
import pandas as pd
from folium.plugins import MarkerCluster
import webbrowser

# Your data dictionary
data = {
    'State': [
        'California', 'New York', 'Florida', 'Texas', 'Washington',
        'North Dakota', 'Oklahoma', 'Illinois', 'Arizona', 'Nevada',
        'Oregon', 'Colorado', 'Hawaii', 'New Jersey', 'Alaska',
        'Michigan', 'Louisiana', 'Delaware', 'Vermont', 'Massachusetts',
        'Connecticut', 'Maine', 'Rhode Island', 'Minnesota', 'Wisconsin',
        'Iowa', 'Nebraska', 'South Dakota', 'Wyoming', 'New Hampshire',
        'Arkansas', 'Georgia', 'Idaho', 'Indiana', 'Kansas',
        'Kentucky', 'Maryland', 'Mississippi', 'Missouri', 'Montana',
        'New Mexico', 'North Carolina', 'Ohio', 'Pennsylvania', 'South Carolina',
        'Tennessee', 'Utah', 'Virginia', 'West Virginia', 'Alabama'
    ],
    'Status': [
        'Increased', 'Increased', 'Increased', 'Increased', 'Increased',
        'Increased', 'Increased', 'Increased', 'Increased', 'Increased',
        'Increased', 'Increased', 'Increased', 'Increased', 'Increased',
        'Decreased', 'Decreased', 'Decreased', 'Decreased', 'Decreased',
        'Decreased', 'Decreased', 'Decreased', 'Decreased', 'Decreased',
        'Decreased', 'Decreased', 'Decreased', 'Decreased', 'Decreased',
        'Stable', 'Stable', 'Stable', 'Stable', 'Stable',
        'Stable', 'Stable', 'Stable', 'Stable', 'Stable',
        'Stable', 'Stable', 'Stable', 'Stable', 'Stable',
        'Stable', 'Stable', 'Stable', 'Stable', 'Stable'
    ],
    'Description': [
        "California: Homelessness rose from 136,826 in 2013 to 173,800 in 2023.",
        "New York: Homeless population increased from 77,430 in 2013 to 91,000 in 2023.",
        "Florida: 18.5% increase from 2022 to 2023, reaching 30,756.",
        "Texas: Homeless population increased to over 30,000 in 2023.",
        "Washington: Homelessness rose from 17,144 in 2013 to 26,000 in 2023.",
        "North Dakota: 28.5% increase in homelessness from 2022 to 2023.",
        "Oklahoma: 23.8% increase from 2022 to 2023.",
        "Illinois: 29% increase in homelessness in 2023.",
        "Arizona: 33% increase in Maricopa County from 2022 to 2023.",
        "Nevada: 14% increase in Las Vegas from 2022 to 2023.",
        "Oregon: 15% increase in Portland from 2022 to 2023.",
        "Colorado: 22% increase from 2022 to 2023.",
        "Hawaii: 12% increase from 2022 to 2023.",
        "New Jersey: 11% increase from 2022 to 2023.",
        "Alaska: 9% increase from 2022 to 2023.",
        "Michigan: 68% reduction over the past decade.",
        "Louisiana: 57% reduction from 2022 to 2023.",
        "Delaware: 47.4% decrease from 2022 to 2023.",
        "Vermont: 96% of homeless population sheltered by 2023.",
        "Massachusetts: 2% increase over the past decade.",
        "Connecticut: 50% reduction over the past decade.",
        "Maine: 10% decrease from 2022 to 2023.",
        "Rhode Island: 3% increase over the past decade.",
        "Minnesota: 15% reduction over the last decade.",
        "Wisconsin: 5% decrease from 2022 to 2023.",
        "Iowa: 12% decrease from 2022 to 2023.",
        "Nebraska: 1% increase over the past decade.",
        "South Dakota: 7% decrease from 2022 to 2023.",
        "Wyoming: Stable with minor fluctuations.",
        "New Hampshire: 20% reduction over the past decade.",
        "Arkansas: No significant change in homelessness trends over the last decade.",
        "Georgia: No significant change in homelessness trends over the last decade.",
        "Idaho: No significant change in homelessness trends over the last decade.",
        "Indiana: No significant change in homelessness trends over the last decade.",
        "Kansas: No significant change in homelessness trends over the last decade.",
        "Kentucky: No significant change in homelessness trends over the last decade.",
        "Maryland: No significant change in homelessness trends over the last decade.",
        "Mississippi: No significant change in homelessness trends over the last decade.",
        "Missouri: No significant change in homelessness trends over the last decade.",
        "Montana: No significant change in homelessness trends over the last decade.",
        "New Mexico: No significant change in homelessness trends over the last decade.",
        "North Carolina: No significant change in homelessness trends over the last decade.",
        "Ohio: No significant change in homelessness trends over the last decade.",
        "Pennsylvania: No significant change in homelessness trends over the last decade.",
        "South Carolina: No significant change in homelessness trends over the last decade.",
        "Tennessee: No significant change in homelessness trends over the last decade.",
        "Utah: No significant change in homelessness trends over the last decade.",
        "Virginia: No significant change in homelessness trends over the last decade.",
        "West Virginia: No significant change in homelessness trends over the last decade.",
        "Alabama: No significant change in homelessness trends over the last decade."
    ]
}

df = pd.DataFrame(data)

url = "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/us-states.json"
geo_data = gpd.read_file(url)

# Reproject to a projected CRS
geo_data = geo_data.to_crs(epsg=4326)  # Use WGS84 (epsg:4326) for compatibility with Folium

# Create a Base Map
m = folium.Map(location=[37.8, -96], zoom_start=4)


def get_color(status):
    if status == 'Increased':
        return 'red'
    elif status == 'Decreased':
        return 'blue'
    else:  # Stable
        return 'gray'


# Add GeoJson and Markers
for _, row in df.iterrows():
    state_geometry = geo_data[geo_data['name'] == row['State']].geometry.iloc[0]
    folium.GeoJson(
        state_geometry,
        style_function=lambda x, status=row['Status']: {'fillColor': get_color(status), 'color': 'black', 'weight': 2,
                                                        'fillOpacity': 0.5},
        name=row['State']
    ).add_to(m)

marker_cluster = MarkerCluster().add_to(m)

# Add Markers at the centroid of each state
for _, row in df.iterrows():
    state_geometry = geo_data[geo_data['name'] == row['State']].geometry.centroid.iloc[0]
    folium.Marker(
        location=[state_geometry.y, state_geometry.x],
        popup=f"<b>{row['State']}</b><br>{row['Description']}",
        icon=folium.Icon(color=get_color(row['Status']))
    ).add_to(marker_cluster)

# Save the map
m.save("us_homelessness_map.html")

# Open the map in the default browser
file_path = os.path.abspath("us_homelessness_map.html")
webbrowser.open(f"file://{file_path}")

print(f"Map saved to: {file_path}")
