import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Example dataset
data = {
    'Year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    'Wage': [4650, 4825, 5000, 5300, 5300, 5300, 5300, 5571.75, 5880.02],
    'Fuel': [6.1, 6.3, 6.5, 6.6, 6.7, 6.8, 7.0, 7.2, 7.5],
    'Rent': [3000, 3100, 3200, 3300, 3400, 3500, 3600, 3800, 4000],
    'Groceries': [1500, 1550, 1600, 1650, 1700, 1750, 1800, 1900, 2000]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Function to calculate adjusted prices based on wage growth
def calculate_adjusted_prices(df, category, wage_growth_rate):
    adjusted_prices = [df[category].iloc[0]]
    for i in range(1, len(df)):
        adjusted_price = adjusted_prices[-1] * (1 + wage_growth_rate / 100)
        adjusted_prices.append(adjusted_price)
    return adjusted_prices

# Streamlit layout
st.title("Income vs. Prices Dashboard")
st.sidebar.header("Controls")

# Select category
default_categories = ['Fuel', 'Rent', 'Groceries']
selected_categories = st.sidebar.multiselect("Select categories to display:", default_categories, default=default_categories)

# Wage growth rate slider
wage_growth_rate = st.sidebar.slider("Set Wage Growth Rate (% per year):", min_value=1.0, max_value=10.0, value=3.0, step=0.1)

# Plot the data
fig, ax = plt.subplots(figsize=(10, 6))

for category in selected_categories:
    # Real prices
    ax.plot(df['Year'], df[category], label=f"{category} (Real)", linestyle='-', marker='o')

    # Adjusted prices
    adjusted_prices = calculate_adjusted_prices(df, category, wage_growth_rate)
    ax.plot(df['Year'], adjusted_prices, label=f"{category} (Adjusted)", linestyle='--')

# Add wage line
ax.plot(df['Year'], df['Wage'], label="Wage", color='blue', linewidth=2, linestyle='-')

# Customize plot
ax.set_title("Comparison of Real vs. Adjusted Prices", fontsize=16)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Amount (NIS)", fontsize=12)
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, linestyle='--', alpha=0.6)

# Display plot
st.pyplot(fig)

# Explanation text
st.markdown("""
### Insights:
- **Blue Line**: Represents the minimum wage across the years.
- **Solid Lines**: Represent the real prices of selected categories.
- **Dashed Lines**: Show the adjusted prices if they followed the selected wage growth rate.

Use the controls on the left to adjust the growth rate or toggle categories.
""")
