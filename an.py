import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample data for testing
years = list(range(2010, 2023))
minimum_wage = [5000, 5200, 5400, 5500, 5600, 5800, 5900, 6000, 6200, 6300, 6400, 6500, 6700]
expenses = [4500, 4800, 5000, 5200, 5300, 5600, 5700, 5900, 6100, 6200, 6300, 6400, 6600]

# Calculate savings
savings = [max(0, mw - exp) for mw, exp in zip(minimum_wage, expenses)]

# Create a DataFrame
data = {
    "Year": years,
    "Expenses": expenses,
    "Savings": savings
}
df = pd.DataFrame(data)

# Streamlit app setup
st.title("Yearly Financial Analysis")
st.sidebar.header("Visualization Options")

# Select year range
start_year, end_year = st.sidebar.slider(
    "Select Year Range",
    min_value=min(years),
    max_value=max(years),
    value=(min(years), max(years)),
    step=1
)

filtered_df = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]

# Stacked Bar Chart
st.header("Stacked Bar Chart of Expenses and Savings")
fig, ax = plt.subplots(figsize=(10, 6))

# Plotting the stacked bars
ax.bar(filtered_df["Year"], filtered_df["Expenses"], label="Expenses", color="red")
ax.bar(filtered_df["Year"], filtered_df["Savings"], bottom=filtered_df["Expenses"], label="Savings", color="green")

# Chart labels and legend
ax.set_title("Yearly Expenses and Savings")
ax.set_xlabel("Year")
ax.set_ylabel("Amount (NIS)")
ax.legend()

st.pyplot(fig)
