import streamlit as st
import matplotlib.pyplot as plt

# נתונים לדוגמה
data = {
    "Year": years,
    "Minimum Wage": minimum_wage,
    "Expenses": expenses
}

df = pd.DataFrame(data)

# תצוגת Streamlit
st.title("Savings Distribution Per Year")
year = st.slider("Select Year", min_value=2010, max_value=2022, step=1)
selected_data = df[df["Year"] == year].iloc[0]

# יצירת גרף פאי
labels = ["Savings", "Expenses"]
sizes = [selected_data["Minimum Wage"] - selected_data["Expenses"], selected_data["Expenses"]]
colors = ["green", "red"]

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(fig)
