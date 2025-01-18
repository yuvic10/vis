import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample data for testing
years = list(range(2010, 2023))
minimum_wage = [5000, 5200, 5400, 5500, 5600, 5800, 5900, 6000, 6200, 6300, 6400, 6500, 6700]
expenses = [4500, 4800, 5000, 5200, 5300, 5600, 5700, 5900, 6100, 6200, 6300, 6400, 6600]

# Create a DataFrame
data = {
    "Year": years,
    "Minimum Wage": minimum_wage,
    "Expenses": expenses
}
df = pd.DataFrame(data)

# Streamlit app setup
st.title("Savings and Expenses Analysis")
st.sidebar.header("Visualization Options")

# Select year from slider
year = st.sidebar.slider("Select Year", min_value=min(years), max_value=max(years), step=1)
selected_data = df[df["Year"] == year].iloc[0]

# Savings calculation
savings = selected_data["Minimum Wage"] - selected_data["Expenses"]

# Display data
st.write(f"**Year:** {year}")
st.write(f"**Minimum Wage:** {selected_data['Minimum Wage']} NIS")
st.write(f"**Expenses:** {selected_data['Expenses']} NIS")
st.write(f"**Savings:** {savings} NIS")

# Option to view pie chart
st.header("Savings Distribution")
labels = ["Savings", "Expenses"]
sizes = [max(0, savings), selected_data["Expenses"]]
colors = ["green", "red"]

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax.axis("equal")  # Equal aspect ratio ensures the pie chart is circular.

st.pyplot(fig)

# Option to view yearly bar chart
st.header("Yearly Savings and Expenses")
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(df["Year"], df["Minimum Wage"], color="blue", label="Minimum Wage")
ax.bar(df["Year"], df["Expenses"], color="red", label="Expenses", alpha=0.7)
ax.plot(df["Year"], [mw - exp for mw, exp in zip(df["Minimum Wage"], df["Expenses"])],
        color="green", label="Savings", linewidth=2)

ax.set_title("Yearly Financial Analysis")
ax.set_xlabel("Year")
ax.set_ylabel("Amount (NIS)")
ax.legend()

st.pyplot(fig)
