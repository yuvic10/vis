import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# נתונים לדוגמה
years = list(range(2010, 2023))
categories = ['Fuel', 'Rent', 'Products']

# מחירים אמיתיים ומדומים לדוגמה
actual_prices = pd.DataFrame({
    'Year': years,
    'Fuel': np.random.randint(100, 200, len(years)),
    'Rent': np.random.randint(500, 800, len(years)),
    'Products': np.random.randint(50, 150, len(years))
})
wage_growth = np.linspace(1.02, 1.05, len(years))  # אחוזי עליית שכר לדוגמה

# יצירת מחירים מדומים בהתבסס על השכר
predicted_prices = actual_prices.copy()
for col in categories:
    predicted_prices[col] = predicted_prices[col].iloc[0] * np.cumprod(wage_growth)

# פונקציה לחישוב היחס בין המחירים
def calculate_difference(actual, predicted):
    return (actual - predicted) / predicted

# חישוב הפערים
differences = actual_prices.set_index('Year')[categories].subtract(
    predicted_prices.set_index('Year')[categories]
)
relative_differences = calculate_difference(actual_prices.set_index('Year'), 
                                            predicted_prices.set_index('Year'))

# ממשק Streamlit
st.title("Comparison Between Actual and Projected Prices")
st.sidebar.title("Settings")

# בחירת קטגוריה
selected_categories = st.sidebar.multiselect("Select Categories", categories, default=categories)
growth_rate = st.sidebar.slider("Set Wage Growth Rate (%)", 1, 10, 3) / 100
years_selected = st.sidebar.slider("Select Year Range", min_value=min(years), max_value=max(years), value=(min(years), max(years)))

# סינון נתונים לפי שנים נבחרות
filtered_actual = actual_prices[(actual_prices['Year'] >= years_selected[0]) & 
                                (actual_prices['Year'] <= years_selected[1])]
filtered_predicted = predicted_prices[(predicted_prices['Year'] >= years_selected[0]) & 
                                      (predicted_prices['Year'] <= years_selected[1])]
filtered_differences = relative_differences[(relative_differences.index >= years_selected[0]) & 
                                            (relative_differences.index <= years_selected[1])]

# הצגת מפה
st.subheader("Heatmap of Price Differences")
heatmap_data = filtered_differences[selected_categories]
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="RdYlGn", ax=ax, cbar_kws={'label': 'Difference'})
ax.set_title("Relative Price Differences (Actual vs Projected)")
st.pyplot(fig)

# הצגת גרף קווי (אם לחצו על שנה)
selected_year = st.sidebar.selectbox("Select Year to Drill Down", years)
if selected_year:
    st.subheader(f"Yearly Comparison for {selected_year}")
    yearly_data = pd.DataFrame({
        'Category': categories,
        'Actual': filtered_actual[filtered_actual['Year'] == selected_year][categories].values[0],
        'Projected': filtered_predicted[filtered_predicted['Year'] == selected_year][categories].values[0]
    }).set_index('Category')
    st.bar_chart(yearly_data)
