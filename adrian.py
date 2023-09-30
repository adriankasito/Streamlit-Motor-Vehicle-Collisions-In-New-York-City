import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

DATE_TIME = "accident date_accident time"
DATA_URL = (r"new.csv")

st.title("Motor Vehicle Collisions in New York City")
st.markdown("Streamlit Application to analyze Motor Vehicle Collision in New York City 🚗")

#processing data
@st.cache_data(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['ACCIDENT DATE', 'ACCIDENT TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data.rename(columns={"number of persons injured": "number_of_persons_injured"}, inplace=True)
    #data.rename(columns={"crash_date_crash_time": "crash date/ crash time"}, inplace=True)
    #data = data[['date/time', 'latitude', 'longitude']]
    return data

max_nrows = 2247
original_data = load_data(max_nrows)

data = load_data(2200)
data[['latitude','longitude']].to_csv('lat_long.csv', index=False)


#Slider to filter based on no of injured people
st.header("Where are the most people injured in NYC?")
injured_people = st.slider("Number of persons injured in vehicle collisions", 0, 19)
st.map(data.query("number_of_persons_injured >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))

#slider to filter based on time
st.header("How many collisions occur during a given time of day?")
hour = st.slider("Hour to look at", 0, 23)
original_data = data
data = data[data['accident date_accident time'].dt.hour == hour]
st.markdown("Vehicle collisions between %i:00 and %i:00" % (hour, (hour + 1) % 24))

#Showing 3D Map and chart
midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data=data[['accident date_accident time', 'latitude', 'longitude']],
        get_position=["longitude", "latitude"],
        auto_highlight=True,
        radius=100,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0, 1000],
        ),
    ],
))

#Showing Histogram based on time
st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
filtered = data[
    (data['accident date_accident time'].dt.hour >= hour) & (data['accident date_accident time'].dt.hour < (hour + 1))
]
hist = np.histogram(filtered['accident date_accident time'].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "crashes": hist})

fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
st.write(fig)

#st.write(original_data.columns)
#st.write(original_data.head())

#Showing Top 5 Dangerous streets by filtering
# Sidebar with user input
st.sidebar.header("Select Affected Class")
select = st.sidebar.selectbox("Affected class", ["Pedestrians", "Cyclists", "Motorists"])

# Filter and display top 5 dangerous streets
st.title("Top 5 Dangerous Streets by Affected Class")
if select == "Pedestrians":
    column_name = "number of pedestrians injured"
elif select == "Cyclists":
    column_name = "number of cyclist injured"
else:
    column_name = "number of motorist injured"

# Filter the data based on the selected class and injury count
filtered_data = original_data[
    (original_data[column_name] >= 1) & original_data["on street name"].notna()
]

# Sort the data by the injury count in descending order and get the top 5
sorted_data = filtered_data.sort_values(by=[column_name], ascending=False).head(5)

# Display the results in a table
st.write(sorted_data[["on street name", column_name]])

#Checkbox to show raw table data
if st.checkbox("Show raw data", False):
    st.subheader("Raw data by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
    st.write(data)
