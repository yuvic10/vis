import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# כותרת האפליקציה
st.title("Shopping Basket Affordability by Year")
st.write("Select products for your basket and set a maximum price to filter the years.")

# העלאת קובץ ה-Excel
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    try:
        # קריאת נתונים מהקובץ
        data = pd.read_excel(uploaded_file, engine="openpyxl")

        # בדיקה שהעמודות הנדרשות קיימות
        if not all(col in data.columns for col in ["product", "year", "yearly average price"]):
            st.error("The file must contain 'product', 'year', and 'yearly average price' columns.")
        else:
            # המרת נתונים למבנה מתאים
            product_prices = {
                product: {
                    row["year"]: row["yearly average price"]
                    for _, row in data[data["product"] == product].iterrows()
                }
                for product in data["product"].unique()
            }

            # בחירת מוצרים לסל
            selected_products = st.multiselect("Select Products for Your Basket", options=list(product_prices.keys()))

            # חישוב המחיר הכולל של הסל לאורך השנים
            basket_prices = {year: 0 for year in data["year"].unique()}
            for product in selected_products:
                for year, price in product_prices[product].items():
                    basket_prices[year] += price

            # בחירת תקרת מחיר
            max_price = st.slider("Set Maximum Basket Price", min_value=int(data["yearly average price"].min()),
                                  max_value=int(data["yearly average price"].sum()), value=50)

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
            st.table({"Year": list(basket_prices.keys()), "Basket Price": list(basket_prices.values())})

    except Exception as e:
        st.error(f"Failed to load or process the file: {e}")
else:
    st.info("Please upload an Excel file to proceed.")
