import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Example data
data = {
    'Year': [2000, 2005, 2010, 2015, 2020],
    'Minimum Wage': [3000, 3500, 4000, 4500, 5000],
    'Fuel Cost': [1000, 1500, 2000, 2500, 3000],
    'Basic Products': [1200, 1600, 2000, 2500, 3000],
    'Rent': [800, 1200, 1600, 2000, 2500]
}
df = pd.DataFrame(data)

# User input: Adjust proportions of categories
st.sidebar.header("Adjust Proportions")
fuel_rate = st.sidebar.slider('Fuel (%)', 0, 100, 30)
product_rate = st.sidebar.slider('Basic Products (%)', 0, 100, 50)
rent_rate = st.sidebar.slider('Rent (%)', 0, 100, 20)

# Recalculate costs based on user input
df['Adjusted Cost of Living'] = (
    df['Fuel Cost'] * (fuel_rate / 100) +
    df['Basic Products'] * (product_rate / 100) +
    df['Rent'] * (rent_rate / 100)
)

# Calculate the difference between minimum wage and cost of living
df['Difference (NIS)'] = df['Minimum Wage'] - df['Adjusted Cost of Living']

# Line chart with shaded areas
st.title("Minimum Wage vs. Cost of Living (Interactive)")

fig, ax = plt.subplots()
ax.plot(df['Year'], df['Minimum Wage'], label='Minimum Wage', color='blue')
ax.plot(df['Year'], df['Adjusted Cost of Living'], label='Adjusted Cost of Living', color='red')

# Highlight areas of surplus and deficit
ax.fill_between(df['Year'], df['Minimum Wage'], df['Adjusted Cost of Living'], 
                where=(df['Minimum Wage'] >= df['Adjusted Cost of Living']), color='lightgreen', alpha=0.3, label='Surplus')
ax.fill_between(df['Year'], df['Minimum Wage'], df['Adjusted Cost of Living'], 
                where=(df['Minimum Wage'] < df['Adjusted Cost of Living']), color='pink', alpha=0.3, label='Deficit')

ax.set_title("Adjusted Cost of Living vs. Minimum Wage")
ax.set_xlabel("Year")
ax.set_ylabel("NIS")
ax.legend()

st.pyplot(fig)

# Allow user to select two years for comparison
st.subheader("Compare Two Years")
year_1 = st.selectbox('Select First Year', df['Year'])
year_2 = st.selectbox('Select Second Year', df['Year'])

# Extract data for the selected years
year_1_data = df[df['Year'] == year_1].iloc[0]
year_2_data = df[df['Year'] == year_2].iloc[0]

# Display comparison
st.write(f"### Comparison: {year_1} vs {year_2}")
st.metric(f"Surplus/Deficit in {year_1}", f"{year_1_data['Difference (NIS)']:.2f} NIS")
st.metric(f"Surplus/Deficit in {year_2}", f"{year_2_data['Difference (NIS)']:.2f} NIS")

# Display data table
st.subheader("Data Table")
st.dataframe(df)
