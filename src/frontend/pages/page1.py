import streamlit as st
import requests
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

@st.cache_data
def fetch_region_data():
    response = requests.get('http://localhost:8000/all-information-for-region')
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching data.")
        return []
    
@st.cache_data
def fetch_country(storeid):
    url = f"http://localhost:8000/country-information/?country={country}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching store details")
        return None    

st.title("Hello World page 1")

# Convert the data to a DataFrame for easier handling
def convert_to_dataframe(data):
    # List to hold the region, year, and average monthly income
    records = []
    for entry in data:
        records.append({
            "Region": entry["Region"],
            "Year": entry["Year"],
            "Average_Monthly_Income": entry["Average_Monthly_Income"],
            "Net_Income": entry["Net_Income"],
            "Cost_of_Living": entry["Cost_of_Living"],
            "Housing_Cost_Percentage": entry["Housing_Cost_Percentage"],
            "Housing_Cost": entry["Housing_Cost"],
            "Tax_Rate": entry["Tax_Rate"],
            "Savings_Percentage": entry["Savings_Percentage"],
            "Savings": entry["Savings"],
            "Healthcare_Cost_Percentage": entry["Healthcare_Cost_Percentage"],
            "Healthcare_Cost": entry["Healthcare_Cost"],
            "Education_Cost_Percentage": entry["Education_Cost_Percentage"],
            "Education_Cost": entry["Education_Cost"],
            "Transportation_Cost_Percentage": entry["Transportation_Cost_Percentage"],
            "Transportation_Cost": entry["Transportation_Cost"],
            "Sum_Percentage": entry["Sum_Percentage"],
            "Sum": entry["Sum"],
            "Sum_Costs": entry["Sum_Costs"]
        })
    return pd.DataFrame(records)

# Fetch data
data = fetch_region_data()

# Convert data to DataFrame
df = convert_to_dataframe(data)

# Dropdown menu for selecting the Y-axis data
y_axis_options = [
    "Average_Monthly_Income",
    "Net_Income",
    "Cost_of_Living",
    "Housing_Cost_Percentage",
    "Housing_Cost",
    "Tax_Rate",
    "Savings_Percentage",
    "Savings",
    "Healthcare_Cost_Percentage",
    "Healthcare_Cost",
    "Education_Cost_Percentage",
    "Education_Cost",
    "Transportation_Cost_Percentage",
    "Transportation_Cost",
    "Sum_Percentage",
    "Sum",
    "Sum_Costs"
]

selected_y_axis = st.sidebar.selectbox("Wähle die Y-Achse", y_axis_options)

# Create a plotly line chart based on the selected Y-axis data
fig = go.Figure()

# Iterate over the regions and plot the data for each region
regions = df["Region"].unique()
for region in regions:
    region_data = df[df["Region"] == region]
    fig.add_trace(go.Scatter(x=region_data["Year"], 
                             y=region_data[selected_y_axis], 
                             mode='lines', 
                             name=region))

# Update chart layout
fig.update_layout(
    title=f"{selected_y_axis} by Year and Region",
    xaxis_title="Year",
    yaxis_title=selected_y_axis,
    template="plotly_dark"
)

# Display the plot
st.plotly_chart(fig)
