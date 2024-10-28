
#rating diff from that group(1-7 for eg),mostly 0s and 1s/avg for that group
  
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Step 2: Load data from the debate table
query = """
    SELECT 
        llm_debate_type,
        initial_likert_score,
        final_likert_score,
        rating_difference,
        user_side
    FROM debate
    WHERE initial_likert_score IS NOT NULL AND final_likert_score IS NOT NULL 
    AND rating_difference IS NOT NULL
    AND debate.state = 'finished'
"""
df = pd.read_sql_query(query, conn)

# Step 3: Group initial ratings into four categories
def categorize_initial_rating(initial):
    if initial in [1, 7]:
        return 'group_1_7'
    elif initial in [2, 6]:
        return 'group_2_6'
    elif initial in [3, 5]:
        return 'group_3_5'
    else:
        return 'group_4'

df['rating_group'] = df['initial_likert_score'].apply(categorize_initial_rating)
group_means = df.groupby('rating_group')['rating_difference']
# Step 4: Calculate the mean rating difference for each group
group_means = df.groupby('rating_group')['rating_difference'].mean().reset_index()
group_means = group_means.rename(columns={'rating_difference': 'group_mean_diff'})
print(group_means)
# Merge the group means back to the original dataframe
df = df.merge(group_means, on='rating_group')

# Step 5: Normalize the rating difference by dividing by the group mean
df['normalized_diff'] = df['rating_difference'] / df['group_mean_diff']

# Step 6: Calculate the average normalized difference for each debate type
normalized_mean_df = df.groupby('llm_debate_type')['normalized_diff'].mean().reset_index()

# Step 7: Prepare Streamlit page title
st.title("Normalized Rating Difference by Debate Type (Division Normalization)")

# Step 8: Create a bar chart for each debate type
fig, ax = plt.subplots()
ax.bar(normalized_mean_df['llm_debate_type'], normalized_mean_df['normalized_diff'], color='skyblue')

ax.set_xlabel('Debate Type')
ax.set_ylabel('Normalized Mean of Rating Differences')
ax.set_title('Normalized Rating Difference for Each Debate Type')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Step 9: Display the chart using Streamlit
st.pyplot(fig)

# Step 10: Close the database connection
conn.close()