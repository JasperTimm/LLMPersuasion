import streamlit as st
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to the database and retrieve data
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Load the debate duration data, excluding control debates
query = """
SELECT ddc.* 
FROM debate_duration_categories ddc
JOIN debate d ON ddc.debate_id = d.id
WHERE ddc.llm_debate_type NOT IN ('argument', 'argumentllm')
AND d.rating_difference IS NOT NULL
AND d.state = 'finished'
"""
duration_df = pd.read_sql_query(query, conn)
conn.close()

# Visualization 1: Bar Chart of Average Rating Differences by Duration Category
st.title("Average Rating Difference by Debate Duration Category (Excluding Control Setups)")
avg_rating_diff = duration_df.groupby('duration_category')['rating_difference'].mean()
st.bar_chart(avg_rating_diff)

# Visualization 2: Line Chart of Debate Duration Distribution by Debate Type
st.title("Debate Duration Distribution by Debate Type (Excluding Control Setups)")
duration_by_type = duration_df.groupby(['llm_debate_type', 'duration_category']).size().unstack()
st.line_chart(duration_by_type)

# Visualization 3: Scatter Plot of Duration vs. Rating Difference
st.title("Duration vs. Rating Difference (Excluding Control Setups)")
fig, ax = plt.subplots()
sns.scatterplot(data=duration_df, x='duration', y='rating_difference', hue='duration_category', ax=ax)
plt.xlabel("Debate Duration (minutes)")
plt.ylabel("Rating Difference")
st.pyplot(fig)
