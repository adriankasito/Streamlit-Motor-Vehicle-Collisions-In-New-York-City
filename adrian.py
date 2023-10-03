import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

# Sidebar with user data input
st.sidebar.header("Upload Your Own Data")
user_data = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

@st.cache_data(persist=True)
def load_data(file):
    if file is not None:
        # Load user-provided data
        data = pd.read_csv(file, parse_dates=[['ACCIDENT DATE', 'ACCIDENT TIME']])
    else:
        # Load default data
        data = pd.read_csv("new.csv", parse_dates=[['ACCIDENT DATE', 'ACCIDENT TIME']])
    return data

original_data = load_data(user_data)

DATE_TIME = "accident date_accident time"
DATA_URL = "new.csv"

# Title and Image
st.markdown(
    "<h1 style='text-align: center; color: #FF5733; font-family: Arial, sans-serif;'>"
    "Motor Vehicle Collisions in New York City"
    "</h1>",
    unsafe_allow_html=True,
)
st.image('collision.jpeg', use_column_width=True)

# Subtitle
st.markdown(
    "<h4 style='text-align: center; color: #1E90FF; font-family: Helvetica, sans-serif;'>"
    "Analysis of Motor Vehicle Collisions in New York City 🚗"
    "</h4>",
    unsafe_allow_html=True,
)

# The rest of your code remains unchanged

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
#st.header("How many collisions occur during a given time of day?")
st.markdown("<h3 style='text-align: center; color: #FF5733;'>How many collisions occur during a given time of day?</h3>", unsafe_allow_html=True)
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
         colorRange=[[255, 0, 0]],
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

fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400, color_discrete_sequence=['darkred'])
st.write(fig)

#st.write(original_data.columns)
#st.write(original_data.head())

#Showing Top 5 Dangerous streets by filtering
# Sidebar with user input
st.sidebar.header("Select Affected Class - Injuries")
select = st.sidebar.selectbox("Affected class", ["Pedestrians", "Cyclists", "Motorists"])


# Filter and display top 5 dangerous streets
#st.title("Top 5 Dangerous Streets by Affected Class")
st.markdown('<h3 style="color: yellow;"><span>&#9888;</span> Top 5 Dangerous Streets by Affected Class</h3>', unsafe_allow_html=True)

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

#Showing Top 10 streets by deaths filtering
# Sidebar with user input
st.sidebar.header("Select Affected Class - Deaths")
select = st.sidebar.selectbox("Affected class", ["Pedestrians Killed", "Cyclists Killed", "Motorists Killed"])
# Filter and display top 10 streets with most deaths
#st.title("Top 10 Streets by deaths Affected Class")
st.markdown(
    "<h3 style='color: darkred;'>Top 10 Streets by Deaths - Affected Class</h3>",
    unsafe_allow_html=True
)
if select == "Pedestrians Killed":
    column_name_ = "number of pedestrians killed"
elif select == "Cyclists Killed":
    column_name_ = "number of cyclist killed"
else:
    column_name_ = "number of motorist killed"

# Filter the data based on the selected class and death count
filtered_data = original_data[
    (original_data[column_name_] >= 1) & original_data["on street name"].notna()
]

# Sort the data by the injury count in descending order and get the top 10
sorted_data = filtered_data.sort_values(by=[column_name_], ascending=False).head(10)

# Display the results in a table
st.write(sorted_data[["on street name", column_name_]])

#Breakdown of vehicle type by collision involvement
value_counts = data['vehicle type code 1'].value_counts()

# Display the value counts in Streamlit
#st.write("Breakdown of vehicle type by collision involvement")
st.markdown(
    "<h3 style='color: cyan;'>Breakdown of vehicle type by collision involvement</h3>",
    unsafe_allow_html=True
)
st.write(value_counts)

#Breakdown of factors contributing to collision 
value_counts = data['contributing factor vehicle 1'].value_counts()

# Display the value counts in Streamlit
#st.write("Breakdown of vehicle type by collision involvement")
st.markdown(
    "<h3 style='color: darkgreen;'>Breakdown of factors contributing to collisions</h3>",
    unsafe_allow_html=True
)
st.write(value_counts)

#Checkbox to show raw table data
if st.checkbox("Show raw data", False):
    st.subheader("Raw data by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
    st.write(data)
