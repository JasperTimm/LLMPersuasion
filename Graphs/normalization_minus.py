import sqlite3
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Step 2: Load data from the debate table
query = """
    SELECT 
        llm_debate_type,
        debate.initial_likert_score,
        debate.final_likert_score,
        debate.user_side
    FROM debate
    WHERE initial_likert_score IS NOT NULL 
    AND final_likert_score IS NOT NULL
    AND debate.state = 'finished'
"""
df = pd.read_sql_query(query, conn)

# Step 3: Define a function to calculate the weighted difference
def calculate_weighted_diff(row):
    initial = row['initial_likert_score']
    final = row['final_likert_score']
    side = row['user_side']
    
    # Calculate the absolute difference
    rating_diff = abs(final - initial)
    
    # Calculate weight based on the initial Likert score
    weight = abs(initial - 4)
    
    # Adjust for user-side: Positive if AI persuades toward its side, negative otherwise
    if (side == 'FOR' and final < initial) or (side == 'AGAINST' and final > initial):
        weighted_diff = rating_diff * weight
    else:
        weighted_diff = 0  # No change toward AI's side
    
    return weighted_diff

# Step 4: Apply the weighting function to the data
df['weighted_diff'] = df.apply(calculate_weighted_diff, axis=1)

# Step 5: Calculate the weighted mean for each debate type
weighted_mean_df = df.groupby('llm_debate_type').apply(
    lambda group: np.average(group['weighted_diff'], weights=abs(group['initial_likert_score'] - 4))
).reset_index(name='weighted_mean')

# Step 6: Prepare Streamlit page title
st.title("Weighted Rating Difference by Debate Type")

# Step 7: Create a bar chart for the weighted means
fig, ax = plt.subplots()
ax.bar(weighted_mean_df['llm_debate_type'], weighted_mean_df['weighted_mean'], color='skyblue')

ax.set_xlabel('Debate Type')
ax.set_ylabel('Weighted Mean of Rating Difference')
ax.set_title('Weighted Mean of Rating Difference for Each Debate Type')

# Rotate x labels if too long
ax.set_xticklabels(weighted_mean_df['llm_debate_type'], rotation=45, ha='right')

# Step 8: Display the chart using Streamlit
st.pyplot(fig)

# Step 9: Close the database connection
conn.close()
