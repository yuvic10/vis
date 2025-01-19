import streamlit as st
import pandas as pd
import seaborn as sns
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
st.title("Scatter Plot with Trend Line: Correlation Between Categories")
st.sidebar.title("Select Categories")

# Dropdowns for category selection
categories = growth_data.columns.tolist()
category1 = st.sidebar.selectbox("Select First Category:", categories)
category2 = st.sidebar.selectbox("Select Second Category:", [cat for cat in categories if cat != category1])

# Scatter plot with trend line
fig, ax = plt.subplots(figsize=(8, 6))
sns.regplot(
    x=growth_data[category1],
    y=growth_data[category2],
    ax=ax,
    scatter_kws={'color': 'blue', 'alpha': 0.6},
    line_kws={'color': 'red'}
)
ax.set_title(f"Scatter Plot with Trend Line: {category1} vs {category2}")
ax.set_xlabel(category1)
ax.set_ylabel(category2)

st.pyplot(fig)
