import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Input Data (Rent and Salary)
rent_data = {
    "Year": [2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "Actual Rent": [44594.4, 45664.8, 47383.2, 48624, 49102.8, 50668.8, 53721.6],
}

salary_data = {
    "Year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "Minimum Wage": [4650, 4825, 5000, 5300, 5300, 5300, 5300, 5300, 5571.75, 5880.02],
}

# Convert to DataFrames
rent_df = pd.DataFrame(rent_data)
salary_df = pd.DataFrame(salary_data)

# Calculate Wage Growth Rate (%)
salary_df["Growth Rate"] = salary_df["Minimum Wage"].pct_change() * 100
average_growth_rate = salary_df["Growth Rate"].mean()

# Simulate Rent Prices Based on Wage Growth
def simulate_rent(actual_rent, growth_rate):
    simulated = [actual_rent[0]]
    for i in range(1, len(actual_rent)):
        simulated.append(simulated[-1] * (1 + growth_rate / 100))
    return simulated

# User Input for Custom Growth Rate
st.title("Comparison of Actual vs. Simulated Rent Prices")
custom_growth_rate = st.slider("Set Custom Growth Rate (%)", min_value=-5.0, max_value=10.0, value=average_growth_rate, step=0.1)

# Calculate Simulated Rent
rent_df["Simulated Rent"] = simulate_rent(rent_df["Actual Rent"], custom_growth_rate)

# Visualization
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(rent_df["Year"], rent_df["Actual Rent"], label="Actual Rent", color="blue", marker="o")
ax.plot(rent_df["Year"], rent_df["Simulated Rent"], label="Simulated Rent", color="orange", linestyle="--", marker="o")
ax.fill_between(rent_df["Year"], rent_df["Actual Rent"], rent_df["Simulated Rent"], color="gray", alpha=0.3, label="Difference")

ax.set_title("Actual vs Simulated Rent Prices", fontsize=16)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Rent Price (Currency Unit)", fontsize=12)
ax.legend()
ax.grid(True, linestyle="--", alpha=0.6)

# Display on Streamlit
st.pyplot(fig)

# Data Table
st.subheader("Data Table")
st.write(rent_df)
