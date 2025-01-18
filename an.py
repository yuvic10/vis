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

    # הצגת הנתונים
    st.write("### Data Preview")
    st.dataframe(data)

    # יצירת ממשק לבחירת מוצרים
    selected_products = st.multiselect("Select Products for Your Basket", options=data["product"].unique())

    if selected_products:
        # חישוב המחיר הכולל של הסל לאורך השנים
        basket_prices = data[data["product"].isin(selected_products)].groupby("year")["yearly average price"].sum()

        # הגדרת מקסימום דינמי עבור תקרת המחיר
        max_dynamic_price = int(basket_prices.max())

        # בחירת תקרת מחיר עם מקסימום דינמי
        max_price = st.slider("Set Maximum Basket Price", min_value=10, max_value=max_dynamic_price, value=50)

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

        # הצגת טבלה עם מחירי הסל
        st.subheader("Basket Prices by Year")
        st.write("The table below shows the total basket prices for each year.")
        st.table({"Year": basket_prices.index.tolist(), "Basket Price": basket_prices.values.tolist()})

    else:
        st.info("Please select products to see the analysis.")

except Exception as e:
    st.error(f"Failed to load or process the file: {e}")
