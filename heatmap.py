import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
@st.cache_data
def load_data():
    basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
    rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
    fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"

    basket_df = pd.read_excel(basket_file_url, engine="openpyxl")
    rent_df = pd.read_excel(rent_file_url, engine="openpyxl", sheet_name="Sheet2")
    fuel_df = pd.read_excel(fuel_file_url, engine="openpyxl")

    basket_df["growth"] = basket_df["price for basic basket"].pct_change() * 100
    rent_df["growth"] = rent_df["price for month"].pct_change() * 100
    fuel_df["growth"] = fuel_df["price per liter"].pct_change() * 100

    growth_data = pd.DataFrame({
        "Basket Growth": basket_df["growth"].dropna(),
        "Rent Growth": rent_df["growth"].dropna(),
        "Fuel Growth": fuel_df["growth"].dropna()
    })

    return growth_data

growth_data = load_data()

# Streamlit UI
st.title("Histogram Overlay: Comparing Two Categories")
st.sidebar.title("Select Categories")

# Dropdowns for category selection
categories = growth_data.columns.tolist()
category1 = st.sidebar.selectbox("Select First Category:", categories)
category2 = st.sidebar.selectbox("Select Second Category:", [cat for cat in categories if cat != category1])

# Plot the overlayed histograms
fig, ax = plt.subplots(figsize=(8, 6))
ax.hist(
    growth_data[category1], bins=10, alpha=0.6, label=category1, color="blue", edgecolor="black"
)
ax.hist(
    growth_data[category2], bins=10, alpha=0.6, label=category2, color="orange", edgecolor="black"
)
ax.set_title(f"Histogram Overlay: {category1} vs {category2}")
ax.set_xlabel("Growth Rate (%)")
ax.set_ylabel("Frequency")
ax.legend()
st.pyplot(fig)
