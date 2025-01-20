import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define separate app functions
def app1():
    # Load data from Excel file
    @st.cache_data
    def load_data():
        url = "https://raw.githubusercontent.com/inbalkat/ProjectVisu/main/all_products.xlsx"
        return pd.read_excel(url)
    
    products_df = load_data()
    
    # Streamlit app title
    st.title("Supermarket Product Prices Over Time")
    
    # Define item icons
    item_icons = {
        "apple": "🍎",
        "avocado": "🥑",
        "banana": "🍌",
        "brown bread": "🍞",
        "canola oil": "🛢️",
        "chicken breast": "🍗",
        "chocolate bar": "🍫",
        "coffee": "☕",
        "corn": "🌽",
        "cottage": "⬜",
        "cucumber": "🥒",
        "eggs": "🥚",
        "fresh ground beef": "🥩",
        "honey": "🍯",
        "lemon": "🍋",
        "milk": "🥛",
        "olive oil": "🫒",
        "onion": "🧅",
        "pasta": "🍝",
        "potato": "🥔",
        "rice": "🍚",
        "strawberry": "🍓",
        "tahini": "🥣",
        "tomato": "🍅",
        "tomato sauce": "🥫",
        "white bread": "🥖",
        "white cheese": "🫕",
        "white flour": "🌾",
        "yellow cheese": "🧀",
    }
    
    # Sort the items alphabetically
    item_icons = dict(sorted(item_icons.items()))
    
    # Initialize session state for basket
    if "basket" not in st.session_state:
        st.session_state.basket = []
    
    if "selected_products" not in st.session_state:
        st.session_state.selected_products = []
    
    # Display the supermarket layout
    supermarket_html = """
    <style>
        .item {
            display: flex;
            margin: 10px;
            cursor: pointer;
            font-size: 20px;
            text-align: center;
            justify-content: center;
            align-items: center;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 10px;
            white-space: nowrap; /* Prevent line breaks */
            max-width: 180px; /* Set a maximum width */
            overflow: hidden; /* Hide overflow */
            text-overflow: ellipsis; /* Show '...' if text is too long */
            height: 50px;
        }
        .item:hover {
            transform: scale(1.2);
            transition: transform 0.2s;
            background-color: #f0f0f0;
        }
        .cart {
            font-size: 100px;
            margin-top: 20px;
            text-align: right;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: flex-end;
        }
        .cart-items {
            font-size: 40px;
            margin-right: 20px;
        }
    </style>
    """
    
    st.markdown(supermarket_html, unsafe_allow_html=True)
    
    columns = st.columns(5)
    for index, (product, icon) in enumerate(item_icons.items()):
        with columns[index % 5]:
            if st.button(f"{icon} {product.capitalize()}"):
                if product in st.session_state.selected_products:
                    st.session_state.selected_products.remove(product)
                    st.session_state.basket.remove(icon)
                else:
                    st.session_state.selected_products.append(product)
                    st.session_state.basket.append(icon)
    
    # Display the cart
    cart_html = f"""
    <div class='cart'>
        <div class='cart-items'>{' '.join(st.session_state.basket)}</div>
        🛒
    </div>
    """
    st.markdown(cart_html, unsafe_allow_html=True)
    
    # Filter the dataset based on selected products
    filtered_df = products_df[products_df['product'].isin(st.session_state.selected_products)]
    
    # Calculate the yearly total for the selected products
    if not filtered_df.empty:
        total_prices = (
            filtered_df.groupby('year')['yearly average price']
            .sum()
            .reset_index()
        )
    else:
        total_prices = pd.DataFrame(columns=['year', 'yearly average price'])
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    if not filtered_df.empty:
        ax.plot(
            total_prices['year'],
            total_prices['yearly average price'],
            marker='o',
            color='black',
            linewidth=2,
            label="Total Basket Cost"
        )
        ax.set_xticks(range(2015, 2025))
        ax.legend()
    else:
        ax.text(0.5, 0.5, "No items selected", fontsize=14, ha='center', va='center')
        ax.set_xticks([])
    
    # Customize the plot
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Cost (₪)")
    ax.set_title("Total Cost of Selected Products Over Time")
    ax.grid(True)
    
    # Display the plot in Streamlit
    st.pyplot(fig)


def app2():
    # Load data from uploaded Excel files
    @st.cache_data
    def load_data():
        salary_df = pd.read_excel("https://raw.githubusercontent.com/inbalkat/ProjectVisu/main/salary.xlsx")
        rent_df = pd.read_excel("https://raw.githubusercontent.com/inbalkat/ProjectVisu/main/rent.xlsx")
        fuel_df = pd.read_excel("https://raw.githubusercontent.com/inbalkat/ProjectVisu/main/fuel.xlsx")
        basket_df = pd.read_excel("https://raw.githubusercontent.com/inbalkat/ProjectVisu/main/basic_basket.xlsx")
        return salary_df, rent_df, fuel_df, basket_df
    
    # Load the data
    salary_df, rent_df, fuel_df, basket_df = load_data()
    
    # Prepare data for visualization
    def prepare_data_monthly(salary_df, rent_df, fuel_df, basket_df):
        # Calculate monthly expenses for each category
        basket_df["monthly_expenses"] = basket_df["price for basic basket"] * 4
        fuel_df["monthly_expenses"] = fuel_df["price per liter"] * 100
    
        # Merge with salary data
        merged_rent = rent_df.merge(salary_df, on="year")
        merged_fuel = fuel_df.merge(salary_df, on="year")
        merged_basket = basket_df.merge(salary_df, on="year")
    
        # Calculate percentages of salary
        rent_percent = merged_rent["price for month"] / merged_rent["salary"] * 100
        fuel_percent = merged_fuel["monthly_expenses"] / merged_fuel["salary"] * 100
        basket_percent = merged_basket["monthly_expenses"] / merged_basket["salary"] * 100
    
        years = salary_df["year"]
    
        data = pd.DataFrame({
            "Year": years,
            "Rent": rent_percent,
            "Fuel": fuel_percent,
            "Basic Basket": basket_percent
        })
        return data
    
    data = prepare_data_monthly(salary_df, rent_df, fuel_df, basket_df)
    
    # Visualization function: Radar Plot for Each Category
    def plot_category_star(data, category, color):
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
        years = data["Year"].values
        values = data[category].values
    
        # Define angles for each year
        angles = np.linspace(0, 2 * np.pi, len(years), endpoint=False).tolist()
        angles += angles[:1]  # Close the loop
    
        # Add the closing value to close the radar plot
        values = np.append(values, values[0])
    
        # Plot the radar chart
        ax.plot(angles, values, label=f"{category} as % of Salary", color=color)
        ax.fill(angles, values, alpha=0.25, color=color)
    
        # Customize plot ranges
        max_value = np.max(values)
        min_value = np.min(values)
        range_buffer = (max_value - min_value) * 0.1  # Add a 10% buffer to the range
    
        ax.set_ylim(min_value - range_buffer, max_value + range_buffer)  # Adjust radial limits
    
        # Customize plot
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(years)
        ax.set_yticks(np.linspace(min_value, max_value, 5))  # Dynamically set radial ticks
        ax.set_yticklabels([f"{tick:.1f}%" for tick in np.linspace(min_value, max_value, 5)])
        ax.set_title(f"Radar Plot: {category} as % of Salary", va="bottom", pad=30)
    
        return fig
    
    
    # Streamlit UI
    st.title("Categories as % of Salary")
    
    # User selects category
    category = st.selectbox("Choose a category:", ["Rent", "Fuel", "Basic Basket"])
    
    # Assign unique colors for each category
    category_colors = {
        "Rent": "green",
        "Fuel": "orange",
        "Basic Basket": "purple"
    }
    
    # Display radar plot for selected category
    selected_color = category_colors[category]
    st.pyplot(plot_category_star(data, category, selected_color))


def app3():
    # Load data from uploaded Excel files
    @st.cache_data
    def load_data():
        salary_df = pd.read_excel("https://raw.githubusercontent.com/inbalkat/ProjectVisu/main/salary.xlsx")
        rent_df = pd.read_excel("https://raw.githubusercontent.com/inbalkat/ProjectVisu/main/rent.xlsx")
        fuel_df = pd.read_excel("https://raw.githubusercontent.com/inbalkat/ProjectVisu/main/fuel.xlsx")
        basket_df = pd.read_excel("https://raw.githubusercontent.com/inbalkat/ProjectVisu/main/basic_basket.xlsx")
        return salary_df, rent_df, fuel_df, basket_df
    
    # Load the data
    salary_df, rent_df, fuel_df, basket_df = load_data()
    
    # Update calculations to yearly
    def calculate_yearly_expenses(salary_df, rent_df, fuel_df, basket_df):
        # Update basket to 4 per month * 12 months = 48 baskets per year
        basket_df["yearly_expenses"] = basket_df["price for basic basket"] * 48
        # Fuel: Assume 100 liters per month * 12 months = 1200 liters per year
        fuel_df["yearly_expenses"] = fuel_df["price per liter"] * 1200
        # Rent: Already yearly
        rent_df["yearly_expenses"] = rent_df["price for month"] * 12
        # Combine all yearly expenses
        salary_df["yearly_salary"] = salary_df["salary"] * 12
        merged_df = salary_df[["year", "yearly_salary"]].copy()
        merged_df["yearly_expenses"] = (
            basket_df["yearly_expenses"].values
            + fuel_df["yearly_expenses"].values
            + rent_df["yearly_expenses"].values
        )
        return merged_df
    
    # Visualization: Combined Yearly Salary and Expenses
    def plot_combined_salary_and_expenses(merged_df):
        fig, ax = plt.subplots(figsize=(12, 8))
        x = np.arange(len(merged_df["year"]))  # the label locations
        width = 0.35  # the width of the bars
    
        # Define custom colors
        salary_color = "cornflowerblue"
        expenses_color = "indianred"
    
        ax.bar(x - width/2, merged_df["yearly_salary"], width, label="Yearly Salary", color=salary_color)
        ax.bar(x + width/2, merged_df["yearly_expenses"], width, label="Yearly Expenses", color=expenses_color)
    
        # Add labels, title, grid, and customize y-axis range
        ax.set_xlabel("Year")
        ax.set_ylabel("Amount (₪)")
        ax.set_title("Yearly Salary vs Yearly Expenses")
        ax.set_xticks(x)
        ax.set_xticklabels(merged_df["year"])
        ax.set_ylim(50000, 80000)  # Adjusted to reflect yearly values
        ax.legend()
        ax.grid(axis="y")
    
        return fig
    
    # Streamlit UI
    st.title("Income vs Expenses")
    
    # Calculate yearly expenses and salaries
    merged_df = calculate_yearly_expenses(salary_df, rent_df, fuel_df, basket_df)
    
    # Display combined graph
    st.header("Yearly Salary vs Yearly Expenses")
    st.markdown("<p style='font-size:18px; color:white;'>Expenses = Rent + Basic Shopping Basket + Fuel</p>", unsafe_allow_html=True) 
    # st.subheader("Expenses = Rent + Basic Shopping Basket + Fuel")
    st.pyplot(plot_combined_salary_and_expenses(merged_df))


# Main navigation
def main():
    st.sidebar.title("Navigation")
    app_choice = st.sidebar.radio(
        "Choose an app:", 
        ["Supermarket Product Prices Over Time", "Categories as % of Salary", "Income vs Expenses"]
    )

    if app_choice == "Supermarket Product Prices Over Time":
        app1()
    elif app_choice == "Categories as % of Salary":
        app2()
    elif app_choice == "Income vs Expenses":
        app3()

if __name__ == "__main__":
    main()
