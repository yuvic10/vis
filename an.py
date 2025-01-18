import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# נתוני השכר ומחירי הקטגוריות לאורך השנים
data = {
    "Year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "Minimum Wage": [4650, 4825, 5000, 5300, 5300, 5300, 5300, 5571.75, 5880.02],
    "Fuel Prices": [6.5, 6.7, 6.9, 7.0, 7.2, 7.3, 7.5, 8.0, 8.5],
    "Rent Prices": [2000, 2100, 2200, 2400, 2500, 2600, 2700, 2900, 3100],
    "Product Prices": [500, 520, 540, 560, 580, 600, 620, 650, 680]
}

df = pd.DataFrame(data)

# חישוב אחוז העלייה הממוצע בשכר המינימום במהלך השנים
def calculate_growth_rate(df):
    df["Wage Growth Rate"] = df["Minimum Wage"].pct_change() * 100
    avg_growth_rate = df["Wage Growth Rate"].mean(skipna=True)
    return avg_growth_rate

# חישוב מחירים מדומים בהתבסס על קצב עליית השכר
def calculate_adjusted_prices(df, custom_rate):
    adjusted_prices = {}
    for category in ["Fuel Prices", "Rent Prices", "Product Prices"]:
        adjusted_prices[category] = [df[category].iloc[0]]
        for i in range(1, len(df)):
            adjusted_prices[category].append(adjusted_prices[category][i-1] * (1 + custom_rate / 100))
    return pd.DataFrame(adjusted_prices)

# קצב עלייה ממוצע בשכר המינימום
avg_growth_rate = calculate_growth_rate(df)

# הגדרות של Streamlit
st.title("Real vs. Adjusted Prices Based on Wage Growth")
st.sidebar.write("### Settings")

# אפשרות לבחור קצב עלייה מותאם אישית
custom_growth_rate = st.sidebar.slider("Select Wage Growth Rate (%)", min_value=0.0, max_value=10.0, value=avg_growth_rate)

# אפשרות לבחור קטגוריה
selected_categories = st.sidebar.multiselect(
    "Select Categories to Display",
    ["Fuel Prices", "Rent Prices", "Product Prices"],
    default=["Fuel Prices", "Rent Prices", "Product Prices"]
)

# חישוב מחירים מדומים
adjusted_prices = calculate_adjusted_prices(df, custom_growth_rate)

def plot_prices(df, adjusted_prices, selected_categories):
    plt.figure(figsize=(10, 6))
    years = df["Year"]
    
    for category in selected_categories:
        plt.plot(years, df[category], label=f"{category} (Real)", linestyle="-", marker="o")
        plt.plot(years, adjusted_prices[category], label=f"{category} (Adjusted)", linestyle="--", marker="x")

    plt.title("Real vs. Adjusted Prices Over Time")
    plt.xlabel("Year")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# הצגת הגרף
plot_prices(df, adjusted_prices, selected_categories)

# הצגת אחוז העלייה הממוצע
st.sidebar.write(f"### Average Wage Growth Rate: {avg_growth_rate:.2f}%")
