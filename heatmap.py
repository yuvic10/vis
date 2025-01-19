import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# URLs של קבצי הנתונים
basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
salary_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/salary1.xlsx"
rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"

# טעינת הנתונים
@st.cache_data
def load_data():
    basket_df = pd.read_excel(basket_file_url, engine="openpyxl")
    salary_df = pd.read_excel(salary_file_url, engine="openpyxl")
    rent_df = pd.read_excel(rent_file_url, engine="openpyxl", sheet_name="Sheet2")
    fuel_df = pd.read_excel(fuel_file_url, engine="openpyxl")
    return basket_df, salary_df, rent_df, fuel_df

basket_df, salary_df, rent_df, fuel_df = load_data()

# הוספת עמודות שיעורי שינוי לכל קטגוריה
basket_df["basket_growth"] = basket_df["price for basic basket"].pct_change().fillna(0)
salary_df["salary_growth"] = salary_df["salary"].pct_change().fillna(0)
rent_df["rent_growth"] = rent_df["price for month"].pct_change().fillna(0)
fuel_df["fuel_growth"] = fuel_df["price per liter"].pct_change().fillna(0)

# מיזוג הנתונים לניתוח
merged_df = pd.DataFrame({
    "Year": basket_df["year"],
    "Basket Growth": basket_df["basket_growth"],
    "Salary Growth": salary_df["salary_growth"],
    "Rent Growth": rent_df["rent_growth"],
    "Fuel Growth": fuel_df["fuel_growth"]
}).set_index("Year")

# ממשק Streamlit
st.title("Correlation Analysis: Economic Indicators")
st.sidebar.title("Filters")

# בחירת שנים להצגה
start_year, end_year = st.sidebar.slider(
    "Select Year Range:",
    int(merged_df.index.min()),
    int(merged_df.index.max()),
    (int(merged_df.index.min()), int(merged_df.index.max()))
)

# סינון נתונים לפי שנים
filtered_df = merged_df.loc[start_year:end_year]

# חישוב קורלציות
correlation_matrix = filtered_df.corr()

# הצגת Heatmap
st.write("### Correlation Heatmap")
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", cbar=True)
st.pyplot(plt)

# הצגת נתונים בטבלה
st.write("### Filtered Data")
st.dataframe(filtered_df)

# הצגת גרף השוואתי
st.write("### Growth Rates Over Time")
plt.figure(figsize=(12, 6))
for column in filtered_df.columns:
    plt.plot(filtered_df.index, filtered_df[column], marker='o', label=column)
plt.title("Growth Rates Over Time")
plt.xlabel("Year")
plt.ylabel("Growth Rate (%)")
plt.legend()
plt.grid(True)
st.pyplot(plt)
