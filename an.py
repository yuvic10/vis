import pandas as pd
import matplotlib.pyplot as plt

# נתונים לדוגמה
# יצירת DataFrame עם נתוני שכירות ומוצרים לדוגמה
data = {
    'year': [2017, 2017, 2018, 2018, 2019, 2019, 2020, 2020, 2021, 2021],
    'category': ['rent', 'products', 'rent', 'products', 'rent', 'products', 'rent', 'products', 'rent', 'products'],
    'price': [5000, 45000, 5300, 46000, 5300, 47000, 5300, 48000, 5300, 49000]
}

df = pd.DataFrame(data)

# יצירת גרף היסטוגרמה
plt.figure(figsize=(10, 6))

categories = df['category'].unique()
colors = ['blue', 'orange']

for category, color in zip(categories, colors):
    subset = df[df['category'] == category]
    plt.bar(subset['year'], subset['price'], color=color, alpha=0.6, label=category)

# עיצוב הגרף
plt.title('Comparison Between Rent and Product Prices Over Years', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Price', fontsize=12)
plt.legend(title='Category')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# הצגת הגרף
plt.show()
