import streamlit as st
import pandas as pd
import plotly.express as px

# דוגמת נתונים
data = {
    "Year": [2018, 2019, 2020, 2021, 2022],
    "Category A": [30, 40, 50, 60, 70],
    "Category B": [20, 30, 40, 30, 20],
    "Category C": [50, 30, 10, 20, 10],
}
df = pd.DataFrame(data)

# רשימת האפליקציות לבחירה
apps = ["Pie Chart", "Bar Chart", "Line Chart"]
st.sidebar.title("Navigation")
selected_app = st.sidebar.radio("Choose an application:", apps)

# אפליקציה 1: Pie Chart
if selected_app == "Pie Chart":
    st.title("Pie Chart")
    year = st.selectbox("Select Year:", df["Year"])
    filtered_data = df[df["Year"] == year]
    pie_data = {
        "Category": ["Category A", "Category B", "Category C"],
        "Values": filtered_data.iloc[0, 1:].values,
    }
    pie_df = pd.DataFrame(pie_data)
    fig = px.pie(pie_df, names="Category", values="Values", title=f"Pie Chart for {year}")
    st.plotly_chart(fig)

# אפליקציה 2: Bar Chart
elif selected_app == "Bar Chart":
    st.title("Bar Chart")
    year = st.selectbox("Select Year:", df["Year"], key="bar_chart")
    filtered_data = df[df["Year"] == year]
    bar_data = {
        "Category": ["Category A", "Category B", "Category C"],
        "Values": filtered_data.iloc[0, 1:].values,
    }
    bar_df = pd.DataFrame(bar_data)
    fig = px.bar(bar_df, x="Category", y="Values", title=f"Bar Chart for {year}")
    st.plotly_chart(fig)

# אפליקציה 3: Line Chart
elif selected_app == "Line Chart":
    st.title("Line Chart")
    fig = px.line(df, x="Year", y=["Category A", "Category B", "Category C"], title="Line Chart Over Years")
    st.plotly_chart(fig)
