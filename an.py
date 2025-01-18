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
st.title("Yearly Financial Breakdown: Expenses vs. Savings")
st.sidebar.header("Visualization Options")

# Select year range
start_year, end_year = st.sidebar.slider(
    "Select Year Range",
    min_value=min(years),
    max_value=max(years),
    value=(min(years), max(years)),
    step=1
)

# Filter data by the selected year range
filtered_df = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]

# Generate pie charts for the selected years
st.header("Pie Charts for Selected Years")
columns = st.columns(len(filtered_df))

for idx, (col, row) in enumerate(zip(columns, filtered_df.iterrows())):
    _, row_data = row
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(
        [row_data["Expenses"], row_data["Savings"]],
        labels=["Expenses", "Savings"],
        autopct="%1.1f%%",
        colors=["red", "green"],
        startangle=90,
    )
    ax.set_title(f"Year {int(row_data['Year'])}")
    col.pyplot(fig)
