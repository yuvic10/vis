import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# יצירת נתונים לדוגמה
np.random.seed(42)
years = list(range(2015, 2024))
wage = [5000 + i * 200 for i in range(len(years))]  # שכר מינימום
prices = {
    "Fuel": [200 + np.random.randint(5, 15) * i for i in range(len(years))],
    "Rent": [1000 + np.random.randint(20, 50) * i for i in range(len(years))],
    "Groceries": [500 + np.random.randint(10, 20) * i for i in range(len(years))],
}
data = pd.DataFrame({"Year": years, "Wage": wage, **prices})

# כותרת האפליקציה
st.title("Real vs. Simulated Prices Based on Wage Growth")

# בחירת קטגוריה להצגה
category = st.selectbox("Choose a category to analyze:", ["Fuel", "Rent", "Groceries", "All"])

# בחירת קצב עליית שכר
wage_growth_rate = st.slider("Select annual wage growth rate (%):", min_value=1, max_value=10, value=3)

# חישוב מחירים מדומים
simulated_prices = {}
for key in prices.keys():
    simulated_prices[key] = [
        prices[key][0] * (1 + wage_growth_rate / 100) ** i for i in range(len(years))
    ]
simulated_df = pd.DataFrame({"Year": years, **simulated_prices})

# פלטפורמת תצוגה
fig, ax = plt.subplots(figsize=(10, 6))

if category == "All":
    for cat in prices.keys():
        ax.plot(data["Year"], data[cat], label=f"Real {cat} Prices", linestyle="--")
        ax.plot(
            simulated_df["Year"],
            simulated_df[cat],
            label=f"Simulated {cat} Prices",
            linestyle="-",
        )
else:
    ax.plot(data["Year"], data[category], label=f"Real {category} Prices", linestyle="--")
    ax.plot(
        simulated_df["Year"],
        simulated_df[category],
        label=f"Simulated {category} Prices",
        linestyle="-",
    )

# הוספת צבעים להמחשת פערים
for i in range(len(years)):
    if category == "All":
        for cat in prices.keys():
            real = data.loc[i, cat]
            sim = simulated_df.loc[i, cat]
            if sim > real:
                ax.fill_between(
                    [data.loc[i, "Year"], data.loc[i, "Year"] + 1],
                    [real, real],
                    [sim, sim],
                    color="green",
                    alpha=0.2,
                )
            else:
                ax.fill_between(
                    [data.loc[i, "Year"], data.loc[i, "Year"] + 1],
                    [sim, sim],
                    [real, real],
                    color="red",
                    alpha=0.2,
                )
    else:
        real = data.loc[i, category]
        sim = simulated_df.loc[i, category]
        if sim > real:
            ax.fill_between(
                [data.loc[i, "Year"], data.loc[i, "Year"] + 1],
                [real, real],
                [sim, sim],
                color="green",
                alpha=0.2,
            )
        else:
            ax.fill_between(
                [data.loc[i, "Year"], data.loc[i, "Year"] + 1],
                [sim, sim],
                [real, real],
                color="red",
                alpha=0.2,
            )

ax.set_title("Real vs. Simulated Prices")
ax.set_xlabel("Year")
ax.set_ylabel("Price (NIS)")
ax.legend()

st.pyplot(fig)

# אנימציה
if st.button("Animate Prices Over Time"):
    progress_bar = st.progress(0)
    for i in range(len(years)):
        fig, ax = plt.subplots(figsize=(10, 6))
        if category == "All":
            for cat in prices.keys():
                ax.plot(years[: i + 1], data[cat][: i + 1], label=f"Real {cat} Prices", linestyle="--")
                ax.plot(
                    years[: i + 1],
                    simulated_df[cat][: i + 1],
                    label=f"Simulated {cat} Prices",
                    linestyle="-",
                )
        else:
            ax.plot(years[: i + 1], data[category][: i + 1], label=f"Real {category} Prices", linestyle="--")
            ax.plot(
                years[: i + 1],
                simulated_df[category][: i + 1],
                label=f"Simulated {category} Prices",
                linestyle="-",
            )
        ax.set_title("Real vs. Simulated Prices")
        ax.set_xlabel("Year")
        ax.set_ylabel("Price (NIS)")
        ax.legend()
        st.pyplot(fig)
        progress_bar.progress((i + 1) / len(years))
        time.sleep(0.5)
