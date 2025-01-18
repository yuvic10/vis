import streamlit as st
import matplotlib.pyplot as plt

# רשימת שנים ומספר מוצרים לכל שנה
years = list(range(2015, 2025))
products_per_year = [0] * len(years)  # התחל עם 0 מוצרים לכל שנה

# ממשק Streamlit
st.title("Puzzle Visualization for Shopping Basket Over Time")
st.write("Add products to the shopping basket for each year and watch the puzzle pieces darken.")

# בחירת שנה להוספת מוצרים
selected_year_index = st.slider("Select a year to add products", 0, len(years) - 1, 0)
selected_year = years[selected_year_index]

# הוספת מוצרים לשנה שנבחרה
products_to_add = st.number_input(
    f"Add products for {selected_year}", min_value=0, value=0, step=1
)
products_per_year[selected_year_index] += products_to_add

# חישוב מקסימום מוצרים לנורמליזציה של הצבעים
max_products = max(products_per_year)

# יצירת הפאזל
fig, ax = plt.subplots(figsize=(10, 2))  # התאמת הגודל ליחס אופקי

for i, year in enumerate(years):
    # חישוב הצבע על בסיס מספר המוצרים
    normalized_value = (
        products_per_year[i] / max_products if max_products > 0 else 0
    )
    color = (1 - normalized_value, normalized_value, 0)  # צבע משתנה מירוק לאדום

    # ציור ריבוע לכל שנה
    rect = plt.Rectangle((i, 0), 1, 1, color=color, ec="black")
    ax.add_patch(rect)

    # הוספת טקסט (שנה ומספר מוצרים)
    ax.text(
        i + 0.5,
        0.5,
        f"{year}\n{products_per_year[i]}",
        ha="center",
        va="center",
        fontsize=10,
        color="white",
    )

# התאמת הצירים
ax.set_xlim(0, len(years))
ax.set_ylim(0, 1)
ax.axis("off")  # הסתרת הצירים

# הצגת הפאזל
st.pyplot(fig)

# הצגת טבלה עם הנתונים
st.write("Products added per year:")
st.table({"Year": years, "Products": products_per_year})
