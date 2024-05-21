import pandas as pd
import plotly.graph_objects as go
import numpy as np

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

# Define a consistent color for all markers
marker_color = 'rgb(163, 163, 163)'

# Apply logarithmic scaling to marker sizes
min_size = 10
max_size = 50
merged_df['scaled_size'] = np.log(merged_df['attendants'] + 1)  # Add 1 to avoid log(0)
merged_df['scaled_size'] = (merged_df['scaled_size'] - merged_df['scaled_size'].min()) / (merged_df['scaled_size'].max() - merged_df['scaled_size'].min()) * (max_size - min_size) + min_size

# Mapbox access token
mapbox_access_token = 'pk.eyJ1IjoidHJldm9ybXVycGh5MjQyIiwiYSI6ImNsd2ZtdjRwYjBwN2oycW10N3JnNHdybjcifQ.z688XO-OcOHzQNr5hOJnkw'

# Create the figure
fig = go.Figure()

# Add traces for each college
for _, row in merged_df.iterrows():
    max_displayed = 30
    attendees_list = row['name'][:max_displayed]
    truncated_text = "<br>".join(attendees_list)
    
    if len(row['name']) > max_displayed:
        truncated_text += f"<br>...and {len(row['name']) - max_displayed} more"
    
    hover_text = f"{row['college']}: {row['attendants']} attendees<br>{truncated_text}"
    
    fig.add_trace(go.Scattermapbox(
        lon=[row['long']],
        lat=[row['lat']],
        text=hover_text,
        hoverinfo='text',
        hovertemplate=f'<b>{row["college"]}</b><br>Attendees: {row["attendants"]}<br><br>{truncated_text}<extra></extra>',
        marker=dict(
            size=row['scaled_size'],  # Use scaled size
            color=marker_color,
            opacity=0.5  # Set the opacity to 0.5 for 50% transparency
        ),
        name=row['college']
    ))


# Update layout
fig.update_layout(
    title=go.layout.Title(
        text='College Attendants Map<br>Class of 2024'
    ),
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=39.5,
            lon=-98.35
        ),
        pitch=0,
        zoom=3,
        style='dark'  # You can also use 'satellite-streets', 'light', 'dark', etc.
    )
)

# Show the figure
fig.write_html("bubble.html")
