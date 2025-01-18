import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# יצירת הנתונים מהטבלה שהעלית
data = {
    "product": [
        "קמח לבן", "פסטה, ספגטי", "אורז רגיל ארוז", "בשר בקר טרי טחון", "חזה עוף",
        "שמן זית", "שמן קנולה", "טחינה גולמית"
    ],
    "year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    "price": [
        [4.088, 4.062, 3.978, 3.888, 3.798, 3.781, 4.032, 4.516],  # קמח לבן
        [5.343, 5.483, 5.305, 5.337, 5.303, 5.541, 5.470, 5.828],  # פסטה, ספגטי
        [9.596, 9.568, 9.426, 9.928, 10.119, 10.224, 10.515, 11.038],  # אורז רגיל ארוז
        [61.098, 60.137, 57.386, 56.425, 52.851, 51.945, 53.839, 55.003],  # בשר בקר טרי טחון
        [33.313, 32.648, 31.876, 31.750, 33.245, 32.949, 31.502, 33.887],  # חזה עוף
        [34.415, 33.750, 33.663, 33.798, 32.976, 32.412, 32.912, 32.547],  # שמן זית
        [10.741, 10.405, 10.345, 10.021, 10.067, 10.566, 11.055, 12.922],  # שמן קנולה
        [14.568, 13.226, 12.112, 11.696, 12.471, 13.184, 13.444, 13.576],  # טחינה גולמית
    ]
}

# המרת הנתונים לפורמט DataFrame
products = []
years = []
prices = []
for i, product in enumerate(data["product"]):
    for j, year in enumerate(data["year"]):
        products.append(product)
        years.append(year)
        prices.append(data["price"][i][j])

df = pd.DataFrame({"product": products, "year": years, "price": prices})

# Streamlit App
st.title("Real vs Simulated Prices for Selected Products")

# בחירת קצב גידול השכר
wage_growth_rate = st.slider("Select Wage Growth Rate (%)", 0, 10, 3)

# חישוב מחיר מדומה
def calculate_simulated_price(group, rate):
    start_price = group.iloc[0]
    simulated_prices = [start_price]
    for i in range(1, len(group)):
        simulated_prices.append(simulated_prices[-1] * (1 + rate / 100))
    return simulated_prices

df["simulated_price"] = df.groupby("product")["price"].transform(
    lambda x: calculate_simulated_price(x, wage_growth_rate)
)

# בחירת מוצר להצגה
selected_product = st.selectbox("Select a Product", df["product"].unique())

# סינון נתונים למוצר הנבחר
product_data = df[df["product"] == selected_product]

# הצגת גרף מגמה
plt.figure(figsize=(10, 6))
plt.plot(
    product_data["year"], 
    product_data["price"], 
    label="Real Price", 
    marker="o"
)
plt.plot(
    product_data["year"], 
    product_data["simulated_price"], 
    label="Simulated Price", 
    marker="o", 
    linestyle="--"
)
plt.title(f"Real vs Simulated Prices for {selected_product}")
plt.xlabel("Year")
plt.ylabel("Price")
plt.legend()
st.pyplot(plt)

# הצגת טבלה
st.write("Data Table", product_data)
