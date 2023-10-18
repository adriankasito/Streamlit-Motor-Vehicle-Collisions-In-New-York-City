# Streamlit-Motor-Vehicle-Collisions-In-New-York-City

## Project Overview

This Streamlit-based project provides an interactive dashboard for analyzing motor vehicle collisions in New York City. It enables users to explore and visualize collision data, filter results based on various criteria, and gain insights into collision statistics in the city.

## Features

- Interactive data visualization.
- Filter and analyze data based on injury counts, times of the day, and more.
- Show the top dangerous streets and streets with the most deaths.
- Analyze the breakdown of vehicle types and contributing factors in collisions.

## Project Structure

The project includes the following files:

1. **adrian.py**: The Streamlit application code. It utilizes various Python libraries, including Streamlit, pandas, pydeck, and Plotly Express to create the interactive dashboard.

2. **requirements.txt**: Lists the project's Python dependencies required for the application to run. Install these dependencies using `pip install -r requirements.txt`.

3. **setup.sh**: Configuration script to set up the Streamlit environment.

4. **config.toml**: Configuration file for Streamlit to customize the application's appearance and behavior.

5. **procfile**: Configuration file used for deploying the application on platforms like Heroku.

6. **data files**: The project uses data files, including a default dataset in CSV format (new.csv and lat_long.csv) and a background image (collision.jpeg).

## Getting Started

Follow these steps to set up and run the project locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/Streamlit-Motor-Vehicle-Collisions-In-New-York-City.git
   cd Streamlit-Motor-Vehicle-Collisions-In-New-York-City
