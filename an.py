import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# נתונים לדוגמה
data = {
    'Year': [2015, 2015, 2015, 2016, 2016, 2016, 2017, 2017, 2017],
    'Price': [100, 200, 150, 110, 210, 160, 120, 220, 170],
    'Category': ['Fuel', 'Fuel', 'Fuel', 'Fuel', 'Fuel', 'Fuel', 'Fuel', 'Fuel', 'Fuel']
}
df = pd.DataFrame(data)

# יצירת גרף צפיפות לכל שנה
g = sns.FacetGrid(df, col="Year", col_wrap=4, height=3, aspect=1.5)
g.map(sns.kdeplot, "Price", fill=True, color="orange")
g.set_titles("{col_name}")
g.set_axis_labels("Price", "Density")
g.fig.suptitle("Price Distribution by Year", y=1.02)
plt.show()
