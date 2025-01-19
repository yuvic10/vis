import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# URL לנתוני סל בסיסי ומשכורות
basket_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
salary_url = "https://raw.githubusercontent.com/yuvic10/vis/main/salary.xlsx"

# קריאת הנתונים
basket_data = pd.read_excel(basket_url, sheet_name=0)
salary_data = pd.read_excel(salary_url, sheet_name=0)

# עיגול מחירים ל-3 ספרות
basket_data["price for basic basket"] = basket_data["price for basic basket"].round(3)

# חישוב אחוזי גדילה במשכורות לכל שנה
salary_data["growth_rate"] = salary_data["salary"].pct_change().fillna(0)  # אחוז שינוי לפי השנה הקודמת

# יצירת עמודה חדשה למדמה
basket_data["simulated price"] = basket_data["price for basic basket"].iloc[0]  # ערך התחלתי - מחיר סל של 2015

# חישוב מחירים מדומים: שימוש באחוז הגדילה המצטבר
for i in range(1, len(basket_data)):
    cumulative_growth = 1 + salary_data["growth_rate"].iloc[:i + 1].sum()  # סכום האחוזים המצטברים עד השנה הנוכחית
    basket_data.loc[i, "simulated price"] = basket_data.loc[0, "price for basic basket"] * cumulative_growth  # חישוב מדומה

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
