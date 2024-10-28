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
    WHERE initial_likert_score IS NOT NULL AND final_likert_score IS NOT NULL AND rating_difference IS NOT NULL
    AND debate.state = 'finished'
"""
df = pd.read_sql_query(query, conn)

# Step 3: Create rating groups
def assign_group(row):
    initial = row['initial_likert_score']
    if initial in [1, 7]:
        return 'group_1_7'
    elif initial in [2, 6]:
        return 'group_2_6'
    elif initial in [3, 5]:
        return 'group_3_5'
    elif initial == 4:
        return 'group_4'
    
df['rating_group'] = df.apply(assign_group, axis=1)

# Step 4: Display rating differences for each group for manual verification
for group in ['group_1_7', 'group_2_6', 'group_3_5', 'group_4']:
    st.write(f"Rating Differences for {group}:")
    st.write(df[df['rating_group'] == group][['llm_debate_type', 'rating_difference']])

# Step 5: Define a function to calculate normalized weighted mean for each group
def calculate_weighted_mean(group_df):
    return np.average(group_df['rating_difference'], weights=group_df['rating_difference'] / group_df['rating_difference'].mean())

# Step 6: Calculate the normalized weighted mean for each debate type by group
weighted_means_by_group = df.groupby(['llm_debate_type', 'rating_group']).apply(calculate_weighted_mean).reset_index(name='weighted_mean')

# Step 7: Plot separate graphs for each debate type
debate_types = weighted_means_by_group['llm_debate_type'].unique()

for debate_type in debate_types:
    df_filtered = weighted_means_by_group[weighted_means_by_group['llm_debate_type'] == debate_type]
    
    # Create bar chart for the debate type
    fig, ax = plt.subplots()
    ax.bar(df_filtered['rating_group'], df_filtered['weighted_mean'], color='skyblue')

    ax.set_xlabel('Rating Group')
    ax.set_ylabel('Normalized Average Change in Rating')
    ax.set_title(f'Normalized Average Change for Debate Type: {debate_type}')

    # Display the chart in Streamlit
    st.pyplot(fig)
    
    # Display rating differences for manual verification for this debate type
    st.write(f"Rating Differences for {debate_type} by Group:")
    for group in ['group_1_7', 'group_2_6', 'group_3_5', 'group_4']:
        group_data = df[(df['llm_debate_type'] == debate_type) & (df['rating_group'] == group)]
        st.write(f"{group}:")
        st.write(group_data[['rating_difference']])

# Step 8: Close the database connection
conn.close()

