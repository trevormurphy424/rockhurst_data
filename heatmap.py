import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

# Load the CSV files into DataFrames
graduates_df = pd.read_csv('classOf2024master.csv')
coordinates_df = pd.read_csv('collegeCoord.csv')

# Count the number of graduates attending each college and group names
college_groups = graduates_df.groupby('college')['name'].apply(list).reset_index()
college_counts = graduates_df['college'].value_counts().reset_index()
college_counts.columns = ['college', 'attendants']

# Merge the attendance counts and names with the coordinates
merged_df = pd.merge(college_counts, coordinates_df, on='college', how='left')
merged_df = pd.merge(merged_df, college_groups, on='college', how='left')

# Apply a transformation to the number of attendants
def transform_attendants(attendants):
    if attendants <= 1:
        return 1
    else:
        return np.log(attendants) *1.2  # Adjust the multiplier to balance the scale

merged_df['transformed_attendants'] = merged_df['attendants'].apply(transform_attendants)

# Create a heatmap using Plotly Express with the transformed scale
fig = px.density_mapbox(
    merged_df,
    lat='lat',
    lon='long',
    z='transformed_attendants',
    radius=40,
    center=dict(lat=39.5, lon=-98.35),
    zoom=3,
    mapbox_style='dark'
)

fig.update_traces(hovertemplate=None, selector=dict(type='densitymapbox'))

# Add a pin at a specific location
pin_location = {
    'lat': 38.9602059,  # Latitude for the pin
    'lon': -94.6095244,  # Longitude for the pin
    'name': 'Rockhurst High School',
    'info': ''
}

fig.add_trace(go.Scattermapbox(
    lat=[pin_location['lat']],
    lon=[pin_location['lon']],
    mode='markers+text',
    marker=go.scattermapbox.Marker(
        size=10,
        color='rgb(255, 255, 255)',
        opacity=1
    ),
    text=pin_location['name'],
    textposition='top right',
    hoverinfo='text',
    hovertext=pin_location['info'],
    textfont=dict(
        size=12,
        color='rgb(255, 255, 255)'  # Change this to your desired color
)))

# Update the layout
fig.update_layout(
    title='College Attendants Map<br>Class of 2024 (Transformed Scale)',
    mapbox=dict(
        accesstoken='pk.eyJ1IjoidHJldm9ybXVycGh5MjQyIiwiYSI6ImNsd2ZtdjRwYjBwN2oycW10N3JnNHdybjcifQ.z688XO-OcOHzQNr5hOJnkw',
        center=dict(
            lat=39.5,
            lon=-98.35
        ),
        style="mapbox://styles/trevormurphy242/clwfq6aag02fp01qg6c9i0en0"
    )
)

# Show the figure
fig.write_html("heatmap.html")
