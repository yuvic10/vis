import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# נתיב לקובץ סל בסיסי
basket_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
salary_url = "https://raw.githubusercontent.com/yuvic10/vis/main/salary.xlsx"

# קריאת הנתונים
basket_data = pd.read_excel(basket_url, sheet_name=0)
salary_data = pd.read_excel(salary_url, sheet_name=0)

# עיגול מחירים ל-3 ספרות
basket_data["price for basic basket"] = basket_data["price for basic basket"].round(3)

# חישוב אחוזי גדילה במשכורות
salary_data["growth_rate"] = salary_data["salary"].pct_change().fillna(0)

# חישוב מחירים מדומים
basket_data["simulated price"] = basket_data.iloc[0]["price for basic basket"]  # אתחול עם הערך הראשון
for i in range(1, len(basket_data)):
    growth_factor = 1 + salary_data.loc[i, "growth_rate"]
    basket_data.loc[i, "simulated price"] = basket_data.loc[i - 1, "simulated price"] * growth_factor

# ממשק Streamlit
st.title("Real vs Simulated Prices Line Chart")

# בחירת נתונים להצגה
data_options = ["Real Basket Price", "Simulated Basket Price"]
selected_data = st.multiselect("Select Data to Display", data_options, default=data_options)

# הכנת הנתונים לגרף
graph_data = pd.DataFrame({
    "Year": basket_data["year"],
    "Real Basket Price": basket_data["price for basic basket"],
    "Simulated Basket Price": basket_data["simulated price"]
}).set_index("Year")

# ציור גרף
st.write("### Line Chart of Real vs Simulated Prices")
fig, ax = plt.subplots(figsize=(10, 5))
if "Real Basket Price" in selected_data:
    ax.plot(graph_data.index, graph_data["Real Basket Price"], label="Real Basket Price", color="blue")
if "Simulated Basket Price" in selected_data:
    ax.plot(graph_data.index, graph_data["Simulated Basket Price"], label="Simulated Basket Price", color="orange")
ax.set_title("Real vs Simulated Prices Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Price")
ax.legend()
st.pyplot(fig)
