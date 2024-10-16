import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Step 2: Query to join debate and user_info table and calculate the rating difference
query = """
    SELECT 
        debate.llm_debate_type AS debate_type, 
        debate.initial_likert_score AS initial_likert_score, 
        debate.final_likert_score AS final_likert_score,
        ABS(debate.final_likert_score - debate.initial_likert_score) AS absolute_change
    FROM debate
    WHERE debate.initial_likert_score IS NOT NULL 
    AND debate.final_likert_score IS NOT NULL 
    AND debate.state = 'finished'
    AND ABS(debate.final_likert_score - debate.initial_likert_score) >= 0  -- Exclude negative rating differences
"""
df = pd.read_sql_query(query, conn)

# Step 3: Group the initial Likert score into groups (1 & 7, 2 & 6, 3 & 5, 4)
def map_likert_group(row):
    if row['initial_likert_score'] in [1, 7]:
        return 'Group 1 (1 & 7)'
    elif row['initial_likert_score'] in [2, 6]:
        return 'Group 2 (2 & 6)'
    elif row['initial_likert_score'] in [3, 5]:
        return 'Group 3 (3 & 5)'
    else:
        return 'Group 4 (4)'  # Neutral (4)

# Apply the mapping to create a new column for the grouped Likert score
df['likert_group'] = df.apply(map_likert_group, axis=1)

# Step 4: Calculate the likelihood of each absolute change for each debate type and Likert group
df_count = df.groupby(['likert_group', 'debate_type', 'absolute_change']).size().reset_index(name='count')
df_total = df_count.groupby(['likert_group', 'debate_type'])['count'].transform('sum')
df_count['likelihood'] = df_count['count'] / df_total

# Step 5: Plotting the graphs
st.title("Likelihood of Change in Rating by Debate Type and Initial Likert Level")

# Set up the plot for each Likert group
groups = df['likert_group'].unique()
for group in groups:
    plt.figure(figsize=(12, 6))
    df_group = df_count[df_count['likert_group'] == group]
    
    # Plot multiple lines for different debate types
    sns.lineplot(data=df_group, x='absolute_change', y='likelihood', hue='debate_type', marker='o')

    # Add labels and title
    plt.xlabel("Absolute Likert Score Change")
    plt.ylabel("Likelihood of Change")
    plt.title(f"Likelihood of Change in Rating for {group}")
    plt.legend(title="Debate Type")
    
    # Display the plot using Streamlit
    st.pyplot(plt)

# Step 6: Close the database connection
conn.close()
