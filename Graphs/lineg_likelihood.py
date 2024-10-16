import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Step 2: Fetch the data from the relevant tables
query = """
    SELECT 
        debate.llm_debate_type AS debate_type,
        ABS(debate.initial_likert_score - debate.final_likert_score) AS rating_difference
    FROM debate
    WHERE debate.initial_likert_score IS NOT NULL 
    AND debate.final_likert_score IS NOT NULL
"""
df = pd.read_sql_query(query, conn)

# Step 3: Calculate the total number of debates for each debate type
total_debates_by_type = df.groupby('debate_type')['rating_difference'].count().reset_index(name='total_debates')

# Step 4: Count the number of debates with each absolute Likert score change for each debate type
df_count = df.groupby(['debate_type', 'rating_difference']).size().reset_index(name='count')

# Step 5: Merge the total debate counts to calculate percentage likelihood
df_merged = pd.merge(df_count, total_debates_by_type, on='debate_type')

# Step 6: Calculate the percentage likelihood of each absolute Likert score change for each debate type
df_merged['likelihood_percentage'] = (df_merged['count'] / df_merged['total_debates']) * 100

# Step 7: Plot the line graph
st.title("Likelihood of Absolute Likert Score Change by Debate Type")

plt.figure(figsize=(10, 6))
sns.lineplot(x='rating_difference', y='likelihood_percentage', hue='debate_type', data=df_merged, marker="o")

# Add labels and title
plt.xlabel("Absolute Likert Score Change")
plt.ylabel("Percentage Likelihood (%)")
plt.title("Likelihood of Absolute Likert Score Change by Debate Type")
plt.legend(title="Debate Type", bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(plt)

# Close the database connection
conn.close()
