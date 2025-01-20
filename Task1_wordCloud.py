import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
import seaborn as sns

# Cache for data loading
@st.cache_data
def load_data():
    salary_df = pd.read_excel("https://raw.githubusercontent.com/inbalkat/ProjectVisu/main/salary.xlsx")
    rent_df = pd.read_excel("https://raw.githubusercontent.com/inbalkat/ProjectVisu/main/rent.xlsx")
    fuel_df = pd.read_excel("https://raw.githubusercontent.com/inbalkat/ProjectVisu/main/fuel.xlsx")
    basket_df = pd.read_excel("https://raw.githubusercontent.com/inbalkat/ProjectVisu/main/basic_basket.xlsx")
    products_df = pd.read_excel("https://raw.githubusercontent.com/inbalkat/ProjectVisu/main/all_products.xlsx")
    return salary_df, rent_df, fuel_df, basket_df, products_df

# Load data
salary_df, rent_df, fuel_df, basket_df, products_df = load_data()

# App 1: Supermarket Product Prices Over Time
def app1():
    st.title("Supermarket Product Prices Over Time")

    item_icons = {
        "apple": "🍎", "avocado": "🥑", "banana": "🍌", "brown bread": "🍞", "canola oil": "🛢️",
        "chicken breast": "🍗", "chocolate bar": "🍫", "coffee": "☕", "corn": "🌽", "cottage": "⬜",
        "cucumber": "🥒", "eggs": "🥚", "fresh ground beef": "🥩", "honey": "🍯", "lemon": "🍋",
        "milk": "🥛", "olive oil": "🫒", "onion": "🧅", "pasta": "🍝", "potato": "🥔", "rice": "🍚",
        "strawberry": "🍓", "tahini": "🥣", "tomato": "🍅", "tomato sauce": "🥫", "white bread": "🥖",
        "white cheese": "🫕", "white flour": "🌾", "yellow cheese": "🧀",
    }
    
    # Initialize session state for basket
    if "basket" not in st.session_state:
        st.session_state.basket = []

    for product, icon in item_icons.items():
        if st.button(f"{icon} {product.capitalize()}"):
            if product not in st.session_state.basket:
                st.session_state.basket.append(product)

    st.write("### Selected Products:", st.session_state.basket)

    if st.session_state.basket:
        filtered_df = products_df[products_df['product'].isin(st.session_state.basket)]
        total_prices = filtered_df.groupby('year')['yearly average price'].sum().reset_index()

        fig, ax = plt.subplots()
        ax.plot(total_prices['year'], total_prices['yearly average price'], marker='o')
        ax.set_title("Total Basket Cost Over Time")
        ax.set_xlabel("Year")
        ax.set_ylabel("Total Cost (₪)")
        st.pyplot(fig)

# App 2: Categories as % of Salary
def app2():
    st.title("Categories as % of Salary")

    def prepare_data():
        rent_percent = rent_df["price for month"] / salary_df["salary"] * 100
        fuel_percent = fuel_df["price per liter"] * 100 / salary_df["salary"]
        basket_percent = basket_df["price for basic basket"] * 4 / salary_df["salary"]

        data = pd.DataFrame({
            "Year": salary_df["year"],
            "Rent": rent_percent,
            "Fuel": fuel_percent,
            "Basic Basket": basket_percent
        })
        return data

    data = prepare_data()
    category = st.selectbox("Choose a category:", ["Rent", "Fuel", "Basic Basket"])

    fig, ax = plt.subplots()
    ax.plot(data["Year"], data[category], marker='o')
    ax.set_title(f"{category} as % of Salary")
    ax.set_xlabel("Year")
    ax.set_ylabel("Percentage of Salary (%)")
    st.pyplot(fig)

# App 3: Income vs Expenses
def app3():
    st.title("Income vs Expenses")

    def calculate_yearly_expenses():
        basket_df["yearly_expenses"] = basket_df["price for basic basket"] * 48
        fuel_df["yearly_expenses"] = fuel_df["price per liter"] * 1200
        rent_df["yearly_expenses"] = rent_df["price for month"] * 12

        salary_df["yearly_salary"] = salary_df["salary"] * 12
        merged_df = salary_df[["year", "yearly_salary"]].copy()
        merged_df["yearly_expenses"] = (
            basket_df["yearly_expenses"].values +
            fuel_df["yearly_expenses"].values +
            rent_df["yearly_expenses"].values
        )
        merged_df["difference"] = merged_df["yearly_salary"] - merged_df["yearly_expenses"]
        return merged_df

    merged_df = calculate_yearly_expenses()
    fig, ax = plt.subplots()
    x = np.arange(len(merged_df["year"]))
    ax.bar(x - 0.2, merged_df["yearly_salary"], width=0.4, label="Salary", color="blue")
    ax.bar(x + 0.2, merged_df["yearly_expenses"], width=0.4, label="Expenses", color="red")
    ax.set_xticks(x)
    ax.set_xticklabels(merged_df["year"])
    ax.set_title("Yearly Salary vs Expenses")
    ax.legend()
    st.pyplot(fig)

# Main App
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to:", ["Supermarket Product Prices", "Categories as % of Salary", "Income vs Expenses"])

if choice == "Supermarket Product Prices":
    app1()
elif choice == "Categories as % of Salary":
    app2()
elif choice == "Income vs Expenses":
    app3()
