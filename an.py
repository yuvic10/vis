import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# URL של קובץ ה-Excel ב-GitHub
file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_products.xlsx"

# כותרת האפליקציה
st.title("Shopping Basket Affordability by Year")

try:
    # קריאת הנתונים מתוך הקובץ
    data = pd.read_excel(file_url, engine="openpyxl")

    # יצירת ממשק לבחירת מוצרים
    selected_products = st.multiselect("Select Products for Your Basket", options=data["product"].unique())

    if selected_products:
        # חישוב המחיר הכולל של הסל לאורך השנים
        basket_prices = data[data["product"].isin(selected_products)].groupby("year")["yearly average price"].sum()

        # הגדלת הערך המקסימלי עבור הסף ב-10%
        min_dynamic_price = int(basket_prices.min())
        max_dynamic_price = int(basket_prices.max() * 1.1)  # העלאה של 10%

        # בחירת תקרת מחיר עם טווח דינמי
        max_price = st.slider(
            "Set Maximum Basket Price",
            min_value=min_dynamic_price,
            max_value=max_dynamic_price,
            value=max_dynamic_price
        )

        # סינון שנים לפי תקרת המחיר
        filtered_years = {str(year): price for year, price in basket_prices.items() if price <= max_price}

        # בדיקה אם יש שנים להצגה
        if filtered_years:
            # יצירת ענן מילים
            wordcloud = WordCloud(
                width=800, height=400,
                background_color='white'
            ).generate_from_frequencies(filtered_years)

            # הצגת ענן המילים
            st.subheader("Years Where the Basket is Affordable")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
        else:
            st.warning("No years match the selected basket and price criteria.")

        # הצגת מחירי הסל לכל שנה מתחת לנתוני ענן המילים
        st.write("### Basket Prices by Year")
        st.table(basket_prices.reset_index().rename(columns={"year": "Year", "yearly average price": "Basket Price"}))
    else:
        st.info("Please select products to see the analysis.")

except Exception as e:
    st.error(f"Failed to load or process the file: {e}")
