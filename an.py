import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# יצירת נתונים עבור סל מוצרים ומחירי שכירות
product_data = {
    "product": [
        "קמח לבן", "פסטה, ספגטי", "אורז רגיל ארוז", "בשר בקר טרי טחון", "חזה עוף",
        "שמן זית", "טחינה גולמית"
    ],
    "year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "prices": [
        [4.1, 4.0, 3.9, 3.8, 3.8, 3.7, 4.0, 4.5, 4.7],
        [5.3, 5.5, 5.3, 5.3, 5.5, 5.4, 5.5, 5.8, 6.2],
        [9.6, 9.5, 9.4, 9.9, 10.1, 10.2, 10.5, 11.0, 11.2],
        [61.1, 60.1, 57.4, 56.4, 52.9, 51.9, 53.8, 55.0, 56.7],
        [33.3, 32.6, 31.9, 31.7, 33.2, 32.9, 31.5, 33.8, 39.2],
        [34.4, 33.8, 33.7, 33.8, 33.0, 32.4, 32.9, 32.5, 34.1],
        [14.5, 13.2, 12.1, 11.7, 12.4, 13.1, 13.4, 13.5, 14.1]
    ]
}

rent_data = {
    "year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "rent_prices": [4650, 4825, 5000, 5300, 5300, 5300, 5300, 5300, 5571.75]
}

wages = {
    "year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "wage": [4650, 4825, 5000, 5300, 5300, 5300, 5300, 5300, 5571.75]
}

# המרת הנתונים ל-DataFrame
product_df = pd.DataFrame(product_data)
rent_df = pd.DataFrame(rent_data)
wage_df = pd.DataFrame(wages)

# פונקציה לחישוב מחיר מדומה על בסיס אחוז הגידול של השכר
def calculate_simulated_prices(prices, wage_growth):
    simulated = [prices[0]]
    for i in range(1, len(prices)):
        simulated.append(simulated[-1] * (1 + wage_growth / 100))
    return simulated

# Streamlit app
st.title("Comparison of Real vs. Simulated Prices")

# בחירת אחוז גידול שכר
wage_growth_rate = st.slider("Select Wage Growth Rate (%)", 0, 10, 3)

# חישוב מחירים מדומים עבור כל מוצר
simulated_product_prices = []
for prices in product_data["prices"]:
    simulated_product_prices.append(calculate_simulated_prices(prices, wage_growth_rate))

# עדכון DataFrame
product_df["simulated_prices"] = simulated_product_prices

# חישוב מחיר מדומה עבור שכירות
rent_df["simulated_prices"] = calculate_simulated_prices(rent_df["rent_prices"], wage_growth_rate)

# הצגת גרפים
selected_years = st.slider("Select Year Range", min_value=2015, max_value=2023, value=(2015, 2023))

# סינון נתונים לפי שנים
filtered_product_df = product_df.loc[:, (product_df.columns != "prices")]
filtered_rent_df = rent_df[(rent_df["year"] >= selected_years[0]) & (rent_df["year"] <= selected_years[1])]

# גרף מגמה לסל מוצרים
st.subheader("Product Prices")
for i, product in enumerate(product_data["product"]):
    plt.figure(figsize=(10, 6))
    plt.plot(product_data["year"], product_data["prices"][i], label="Real Price", marker="o")
    plt.plot(product_data["year"], simulated_product_prices[i], label="Simulated Price", linestyle="--", marker="o")
    plt.title(f"{product}: Real vs Simulated Prices")
    plt.xlabel("Year")
    plt.ylabel("Price")
    plt.legend()
    st.pyplot(plt)

# גרף מגמה לשכירות
plt.figure(figsize=(10, 6))
plt.plot(rent_df["year"], rent_df["rent_prices"], label="Real Rent", marker="o")
plt.plot(rent_df["year"], rent_df["simulated_prices"], label="Simulated Rent", linestyle="--", marker="o")
plt.title("Real vs Simulated Rent Prices")
plt.xlabel("Year")
plt.ylabel("Price")
plt.legend()
st.pyplot(plt)

# הצגת נתונים כטבלה
st.subheader("Data")
st.write("Products:", product_df)
st.write("Rent:", rent_df)
