import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# URLs of the datasets
basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"

# Load the data
@st.cache_data
def load_data():
    basket_df = pd.read_excel(basket_file_url, engine="openpyxl")
    rent_df = pd.read_excel(rent_file_url, engine="openpyxl", sheet_name="Sheet2")
    fuel_df = pd.read_excel(fuel_file_url, engine="openpyxl")
    return basket_df, rent_df, fuel_df

basket_df, rent_df, fuel_df = load_data()

# Calculate growth rates for each category
def calculate_growth_rate(data, column):
    return data[column].pct_change().fillna(0) * 100

basket_df["basket_growth"] = calculate_growth_rate(basket_df, "price for basic basket")
rent_df["rent_growth"] = calculate_growth_rate(rent_df, "price for month")
fuel_df["fuel_growth"] = calculate_growth_rate(fuel_df, "price per liter")

# Combine growth data into a single DataFrame
growth_data = pd.DataFrame({
    "year": basket_df["year"],
    "Basket Growth": basket_df["basket_growth"],
    "Rent Growth": rent_df["rent_growth"],
    "Fuel Growth": fuel_df["fuel_growth"],
})

# Calculate correlations
correlation_matrix = growth_data.drop(columns=["year"]).corr()

# Streamlit UI
st.title("Network Graph of Correlations Between Categories")

# Create a Network Graph
def plot_network_graph(correlation_matrix):
    G = nx.Graph()

    # Add nodes and edges
    for i, category1 in enumerate(correlation_matrix.columns):
        for j, category2 in enumerate(correlation_matrix.columns):
            if i < j:  # Only use upper triangle of the correlation matrix
                weight = correlation_matrix.iloc[i, j]
                if abs(weight) > 0.3:  # Add only significant correlations
                    G.add_edge(category1, category2, weight=weight)

    pos = nx.circular_layout(G)  # Circular layout for better visualization
    plt.figure(figsize=(8, 8))

    # Draw the nodes and edges
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="skyblue",
        node_size=2000,
        edge_color=[
            "red" if G[u][v]["weight"] > 0 else "blue" for u, v in G.edges()
        ],
        width=[abs(G[u][v]["weight"]) * 2 for u, v in G.edges()],
        font_size=10,
    )
    plt.title("Network Graph of Correlations", fontsize=16)
    st.pyplot(plt)

plot_network_graph(correlation_matrix)
