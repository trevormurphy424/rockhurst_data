import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2

# Load the CSV files into DataFrames
graduates_df = pd.read_csv('classOf2024master.csv')
coordinates_df = pd.read_csv('collegeCoord.csv')

# Count the number of graduates attending each college and group names
college_counts = graduates_df['college'].value_counts().reset_index()
college_counts.columns = ['college', 'attendants']

# Merge the attendance counts and names with the coordinates
merged_df = pd.merge(college_counts, coordinates_df, on='college', how='left')

# Define the Haversine function
def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

# Main function
def main():
    while True:
        try:
            lat = float(input("Enter the latitude of the center point: "))
            lon = float(input("Enter the longitude of the center point: "))
            radius = float(input("Enter the radius in kilometers: "))
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            continue

        total_students = 0

        for _, row in merged_df.iterrows():
            distance = haversine(lat, lon, row['lat'], row['long'])
            if distance <= radius:
                total_students += row['attendants']

        print(f"Total number of students within {radius} km of ({lat}, {lon}): {total_students}")

        cont = input("Do you want to enter another set of coordinates? (y/n): ")
        if cont.lower() != 'y':
            break

if __name__ == "__main__":
    main()
