import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the data
@st.cache_data
def load_data():
    basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
    rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
    fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"

    basket_df = pd.read_excel(basket_file_url, engine="openpyxl")
    rent_df = pd.read_excel(rent_file_url, engine="openpyxl", sheet_name="Sheet2")
    fuel_df = pd.read_excel(fuel_file_url, engine="openpyxl")

    basket_df["growth"] = basket_df["price for basic basket"].pct_change() * 100
    rent_df["growth"] = rent_df["price for month"].pct_change() * 100
    fuel_df["growth"] = fuel_df["price per liter"].pct_change() * 100

    growth_data = pd.DataFrame({
        "Basket Growth": basket_df["growth"],
        "Rent Growth": rent_df["growth"],
        "Fuel Growth": fuel_df["growth"]
    })

    return growth_data

growth_data = load_data()

# Compute correlations
correlation_matrix = growth_data.corr()

# Create Network Graph
st.title("Network Graph of Correlations")

edges = []
weights = []

for i in correlation_matrix.columns:
    for j in correlation_matrix.columns:
        if i != j:
            weight = abs(correlation_matrix.loc[i, j])
            if weight > 0.2:  # Include only strong correlations
                edges.append((i, j))
                weights.append(weight)

# Create Graph
G = nx.Graph()
for edge, weight in zip(edges, weights):
    G.add_edge(edge[0], edge[1], weight=weight)

# Plot Network Graph
pos = nx.spring_layout(G, seed=42)
fig, ax = plt.subplots(figsize=(8, 6))
nx.draw_networkx_nodes(G, pos, ax=ax, node_size=2000, node_color="skyblue")
nx.draw_networkx_edges(G, pos, ax=ax, width=[d["weight"] * 5 for _, _, d in G.edges(data=True)])
nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_color="black")
st.pyplot(fig)
