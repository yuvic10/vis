import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Example data
data = {
    'Year': [2000, 2005, 2010, 2015, 2020],
    'Minimum Wage': [3000, 3500, 4000, 4500, 5000],
    'Cost of Living': [2800, 3600, 4200, 4800, 5500]
}
df = pd.DataFrame(data)

# Calculate the difference (savings or deficit)
df['Difference (NIS)'] = df['Minimum Wage'] - df['Cost of Living']

# Title of the application
st.title("Minimum Wage vs. Cost of Living")

# Create a line plot to compare minimum wage and cost of living
fig, ax = plt.subplots()
ax.plot(df['Year'], df['Minimum Wage'], label='Minimum Wage', color='blue')
ax.plot(df['Year'], df['Cost of Living'], label='Cost of Living', color='red')

# Highlight positive and negative differences
ax.fill_between(df['Year'], df['Minimum Wage'], df['Cost of Living'], 
                where=(df['Minimum Wage'] < df['Cost of Living']), color='pink', alpha=0.3, label='Deficit')
ax.fill_between(df['Year'], df['Minimum Wage'], df['Cost of Living'], 
                where=(df['Minimum Wage'] >= df['Cost of Living']), color='lightgreen', alpha=0.3, label='Savings')

# Add titles and labels
ax.set_title("Comparison of Minimum Wage and Cost of Living Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("NIS")
ax.legend()

# Display the graph
st.pyplot(fig)

# Display the data as a table
st.dataframe(df)

# Add a metric widget for year-specific analysis
year = st.selectbox('Select a Year:', df['Year'])
selected_year = df[df['Year'] == year]
st.metric(label=f"Difference in {year}", value=f"{selected_year['Difference (NIS)'].values[0]} NIS")
