import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# URLs של קבצי הנתונים
basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
salary_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/salary1.xlsx"
rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"

# טעינת הנתונים
@st.cache_data
def load_data():
    basket_df = pd.read_excel(basket_file_url, engine="openpyxl")
    salary_df = pd.read_excel(salary_file_url, engine="openpyxl")
    rent_df = pd.read_excel(rent_file_url, engine="openpyxl", sheet_name="Sheet2")
    fuel_df = pd.read_excel(fuel_file_url, engine="openpyxl")
    return basket_df, salary_df, rent_df, fuel_df

basket_df, salary_df, rent_df, fuel_df = load_data()

# ממשק Streamlit
st.title("Budget Allocation Analysis Over Time")
st.sidebar.title("Budget Allocation")

# בחירת אחוזים לכל קטגוריה
basket_percentage = st.sidebar.slider("Percentage for Basket:", 0, 100, 30)
rent_percentage = st.sidebar.slider("Percentage for Rent:", 0, 100, 40)
fuel_percentage = st.sidebar.slider("Percentage for Fuel:", 0, 100, 30)

# בדיקה שסך האחוזים הוא 100%
if basket_percentage + rent_percentage + fuel_percentage != 100:
    st.error("The total budget allocation must equal 100%. Please adjust the sliders.")
else:
    # חישוב התקציב לכל קטגוריה
    salary_df["basket_budget"] = (salary_df["salary"] * basket_percentage) / 100
    salary_df["rent_budget"] = (salary_df["salary"] * rent_percentage) / 100
    salary_df["fuel_budget"] = (salary_df["salary"] * fuel_percentage) / 100

    # חישוב היחידות שניתן להרשות לעצמך בכל קטגוריה
    basket_df["basket_units"] = salary_df["basket_budget"] / basket_df["price for basic basket"]
    rent_df["rent_months"] = salary_df["rent_budget"] / rent_df["price for month"]
    fuel_df["fuel_liters"] = salary_df["fuel_budget"] / fuel_df["price per liter"]

    # הכנה לשרטוט הגרף
    data_to_plot = pd.DataFrame({
        "Year": salary_df["year"],
        "Basket Units": basket_df["basket_units"],
        "Rent Months": rent_df["rent_months"],
        "Fuel Liters": fuel_df["fuel_liters"]
    })

    # גרף קווי להצגת יחידות
    fig, ax = plt.subplots(figsize=(10, 6))
    for column in data_to_plot.columns[1:]:
        ax.plot(data_to_plot["Year"], data_to_plot[column], marker="o", label=column)
    ax.set_title("Purchasing Power Based on Budget Allocation")
    ax.set_xlabel("Year")
    ax.set_ylabel("Units Affordable")
    ax.legend()
    ax.grid(True)

    # הצגת הגרף
    st.pyplot(fig)

    # גרף עוגה להצגת חלוקת התקציב
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    ax2.pie(
        [basket_percentage, rent_percentage, fuel_percentage],
        labels=["Basket", "Rent", "Fuel"],
        autopct='%1.1f%%',
        startangle=90
    )
    ax2.set_title("Budget Allocation")
    st.pyplot(fig2)

    # הצגת תובנות
    st.subheader("Insights")
    st.write("""
    This analysis allows you to explore how your budget allocation affects your ability to afford various categories over time. 
    You can see if certain categories, like rent or fuel, consume more of your salary as years progress.
    """)
