import plotly.express as px

# Combine data into a single DataFrame
combined_data = pd.DataFrame({
    "Year": basket_df["year"],
    "Basket": basket_df["basket_percentage"],
    "Rent": rent_df["rent_percentage"],
    "Fuel": fuel_df["fuel_percentage"]
})

# Streamlit UI
st.title("Ribbon Chart: Salary Percentage by Category Over Time")

# Select category
selected_category = st.selectbox("Choose a category:", ["Basket", "Rent", "Fuel"])

# Prepare data for selected category
selected_data = combined_data[["Year", selected_category]].rename(columns={selected_category: "Percentage"})

# Create Ribbon Chart
fig = px.area(
    selected_data,
    x="Year",
    y="Percentage",
    title=f"{selected_category} Percentage Over Time",
    labels={"Percentage": "Percentage of Salary (%)", "Year": "Year"},
    color_discrete_sequence=["teal"]
)

st.plotly_chart(fig)
