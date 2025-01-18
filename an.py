import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

# Load the data
data = {
    "product": ["avocado", "rice", "eggs", "banana", "onion", "avocado", "rice", "eggs", "banana", "onion"],
    "year": [2015, 2015, 2015, 2015, 2015, 2016, 2016, 2016, 2016, 2016],
    "yearly_average_price": [6.73, 9.596, 23.233, 3.648, 3.414, 11.031, 9.568, 22.0, 5.597, 3.228],
}

df = pd.DataFrame(data)

# Streamlit app
st.title("Word Cloud for Years Based on Basket Cost")

# Select products for the basket
selected_products = st.multiselect("Select Products", options=df["product"].unique())

# Filter data based on selected products
filtered_data = df[df["product"].isin(selected_products)]

# Calculate total yearly cost for the selected products
yearly_cost = filtered_data.groupby("year")["yearly_average_price"].sum()

# Display total yearly cost
yearly_cost = yearly_cost.reset_index()

# Allow user to set a cost threshold
threshold = st.slider("Set Cost Threshold", min_value=0, max_value=int(yearly_cost["yearly_average_price"].max()), value=10)

# Filter years below the threshold
filtered_years = {str(row["year"]): row["yearly_average_price"] for _, row in yearly_cost.iterrows() if row["yearly_average_price"] <= threshold}

if filtered_years:
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(filtered_years)

    # Display the word cloud
    st.subheader("Word Cloud")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
else:
    st.warning("No years match the selected threshold.")
