import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data from uploaded Excel files
@st.cache_data
def load_data():
    salary_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/salary.xlsx")
    rent_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx", sheet_name="Sheet2")
    fuel_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx")
    basket_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx")
    return salary_df, rent_df, fuel_df, basket_df

# Load the data
salary_df, rent_df, fuel_df, basket_df = load_data()

# Calculate yearly ratios (slopes) for salaries
def calculate_salary_ratios(df):
    df["ratio"] = df["salary"] / df["salary"].shift(1)
    df["ratio"].iloc[0] = 1  # Set the first year ratio to 1
    return df

salary_df = calculate_salary_ratios(salary_df)

# Calculate predicted prices based on salary ratios
def calculate_predicted_prices(real_prices, salary_ratios):
    predicted_prices = [real_prices.iloc[0]]  # Start with the first real price
    for i in range(1, len(real_prices)):
        predicted = predicted_prices[-1] * salary_ratios.iloc[i]
        predicted_prices.append(predicted)
    return predicted_prices

# Prepare data for visualization
def prepare_data(real_df, salary_df, value_column):
    real_prices = real_df.set_index("year")[value_column]
    salary_ratios = salary_df.set_index("year")["ratio"].fillna(1)
    predicted_prices = calculate_predicted_prices(real_prices, salary_ratios)
    return real_prices, predicted_prices

# Visualization function
def plot_data(title, real_prices, predicted_prices):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(real_prices.index, real_prices, marker='o', label="Real Prices", color='blue')
    ax.plot(real_prices.index, predicted_prices, marker='o', linestyle='--', label="Predicted Prices", color='orange')
    ax.set_title(title)
    ax.set_xlabel("Year")
    ax.set_ylabel("Price")
    ax.set_xticks(range(2015, 2025))
    ax.legend()
    ax.grid(True)
    return fig

# Streamlit UI
st.title("Price Trends vs. Salaries")
st.sidebar.title("Select Category")
category = st.sidebar.radio("Choose a category:", ("Fuel", "Basic Basket", "Rent"))

if category == "Fuel":
    real_prices, predicted_prices = prepare_data(fuel_df, salary_df, "price per liter")
    st.pyplot(plot_data("Fuel Prices vs. Predicted Prices", real_prices, predicted_prices))

elif category == "Basic Basket":
    real_prices, predicted_prices = prepare_data(basket_df, salary_df, "price for basic basket")
    st.pyplot(plot_data("Basic Basket Prices vs. Predicted Prices", real_prices, predicted_prices))

elif category == "Rent":
    real_prices, predicted_prices = prepare_data(rent_df, salary_df, "price for month")
    st.pyplot(plot_data("Rent Prices vs. Predicted Prices", real_prices, predicted_prices))
