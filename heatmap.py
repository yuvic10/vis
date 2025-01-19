import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# URLs של קבצי הנתונים
basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"

# טעינת הנתונים
@st.cache_data
def load_data():
    basket_df = pd.read_excel(basket_file_url, engine="openpyxl")
    rent_df = pd.read_excel(rent_file_url, engine="openpyxl", sheet_name="Sheet2")
    fuel_df = pd.read_excel(fuel_file_url, engine="openpyxl")
    return basket_df, rent_df, fuel_df

basket_df, rent_df, fuel_df = load_data()

# חישוב שיעורי הגדילה
def calculate_growth_rate(data, column):
    return data[column].pct_change().fillna(0) * 100

basket_df["basket_growth"] = calculate_growth_rate(basket_df, "price for basic basket")
rent_df["rent_growth"] = calculate_growth_rate(rent_df, "price for month")
fuel_df["fuel_growth"] = calculate_growth_rate(fuel_df, "price per liter")

# יצירת DataFrame של קורלציות
correlation_data = pd.DataFrame({
    "Basket Growth": basket_df["basket_growth"],
    "Rent Growth": rent_df["rent_growth"],
    "Fuel Growth": fuel_df["fuel_growth"]
}).corr()

# גרף בועות
st.title("Bubble Chart: Correlations Between Categories")
fig, ax = plt.subplots(figsize=(8, 8))

scaler = MinMaxScaler()
bubble_sizes = scaler.fit_transform(correlation_data.values**2) * 1000  # גודל הבועות מבוסס על ערך הקורלציה

for i, row in enumerate(correlation_data.columns):
    for j, col in enumerate(correlation_data.columns):
        ax.scatter(i, j, s=bubble_sizes[i, j], color='blue' if correlation_data.iloc[i, j] > 0 else 'red', alpha=0.6)
        ax.text(i, j, f"{correlation_data.iloc[i, j]:.2f}", color="black", ha="center", va="center")

ax.set_xticks(range(len(correlation_data.columns)))
ax.set_yticks(range(len(correlation_data.columns)))
ax.set_xticklabels(correlation_data.columns, rotation=45)
ax.set_yticklabels(correlation_data.columns)
ax.set_title("Bubble Chart of Correlations Between Categories")
ax.grid(True)

st.pyplot(fig)
