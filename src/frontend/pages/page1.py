import streamlit as st
import requests
import plotly.graph_objects as go
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
def fetch_country_data(country):
    url = f"http://localhost:8000/country-information/?country={country}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching country details")
        return []

# Convert the data to a DataFrame for easier handling
def convert_to_dataframe(data):
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

# Fetch region data
region_data = fetch_region_data()

# Convert region data to DataFrame
df_region = convert_to_dataframe(region_data)

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

# Create a plotly line chart for region data
fig_region = go.Figure()

regions = df_region["Region"].unique()
for region in regions:
    region_data = df_region[df_region["Region"] == region]
    fig_region.add_trace(go.Scatter(x=region_data["Year"], 
                                   y=region_data[selected_y_axis], 
                                   mode='lines', 
                                   name=region))

# Update chart layout for region data
fig_region.update_layout(
    title=f"{selected_y_axis} by Year and Region",
    xaxis_title="Year",
    yaxis_title=selected_y_axis,
    template="plotly_dark"
)

# Fetch country data
country = "Germany"  # Beispiel: Hier könnte das Land dynamisch eingegeben werden
country_data = fetch_country_data(country)

# Convert country data to DataFrame
df_country = convert_to_dataframe(country_data)

# Create a plotly line chart for country data
fig_country = go.Figure()

# Plot data for the selected country
fig_country.add_trace(go.Scatter(x=df_country["Year"], 
                                 y=df_country[selected_y_axis], 
                                 mode='lines', 
                                 name=country))

# Update chart layout for country data
fig_country.update_layout(
    title=f"{selected_y_axis} by Year for {country}",
    xaxis_title="Year",
    yaxis_title=selected_y_axis,
    template="plotly_dark"
)


# Fetch country data
country = "Germany"  # Beispiel: Hier könnte das Land dynamisch eingegeben werden
country_data = fetch_country_data(country)

# Convert country data to DataFrame
df_country = convert_to_dataframe(country_data)

# Filter the data for the last available year for the selected country
latest_year = df_country["Year"].max()
latest_year_data = df_country[df_country["Year"] == latest_year]

# Select the desired columns for the pie chart
pie_columns = [
    "Average_Monthly_Income",
    "Net_Income",
    "Cost_of_Living",
    "Housing_Cost",
    "Tax_Rate",
    "Savings",
    "Healthcare_Cost",
    "Education_Cost",
    "Transportation_Cost"
]

# Prepare the data for the pie chart (using the latest year)
pie_data = latest_year_data[pie_columns].iloc[0].to_dict()

# Create a Plotly pie chart
fig_pie = go.Figure(data=[go.Pie(labels=list(pie_data.keys()), values=list(pie_data.values()), hole=0.3)])

# Update pie chart layout
fig_pie.update_layout(
    title=f"Distribution for {latest_year}",
    template="plotly_dark"
)


# Layout with two columns
col1, col2 = st.columns([1, 1])

with col1:
    # Display the region plot
    st.plotly_chart(fig_region)
    
    # Display the country plot
    st.plotly_chart(fig_country)

with col2: 
    st.plotly_chart(fig_pie)   
    st.title("Hello World page 1")
