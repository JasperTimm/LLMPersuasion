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
        CASE
            -- If the user is "For" and the final score is higher or equal, move towards the user's side (make negative)
            WHEN debate.user_side = 'FOR' AND debate.final_likert_score > debate.initial_likert_score THEN
                debate.final_likert_score - debate.initial_likert_score
            -- If the user is "Against" and the final score is lower or equal, move towards the user's side (make negative)
            WHEN debate.user_side = 'AGAINST' AND debate.final_likert_score < debate.initial_likert_score THEN
                debate.initial_likert_score - debate.final_likert_score
            ELSE
                ABS(debate.final_likert_score - debate.initial_likert_score)
        END AS rating_difference
    FROM debate
    WHERE debate.initial_likert_score IS NOT NULL 
    AND debate.final_likert_score IS NOT NULL 
    AND debate.state = 'finished'
    AND debate.rating_difference >= 0  -- Exclude negative rating differences
"""
df = pd.read_sql_query(query, conn)

# Step 3: Map the Likert scores to the desired groups (1&7, 2&6, 3&5)
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

# Step 4: Calculate the absolute Likert score change for each row
df['likert_change'] = abs(df['final_likert_score'] - df['initial_likert_score'])

# Step 5: Group by likert_group, likert_change and debate_type to calculate the likelihood of change (proportion of rating changes)
df_grouped = df.groupby(['likert_group', 'likert_change', 'debate_type']).size().reset_index(name='count')

# Step 6: Calculate total count per group and change for normalization (to get "likelihood")
df_total = df_grouped.groupby(['likert_group', 'likert_change'])['count'].sum().reset_index(name='total_count')
df_grouped = df_grouped.merge(df_total, on=['likert_group', 'likert_change'])
df_grouped['likelihood'] = df_grouped['count'] / df_grouped['total_count']

# Step 7: Plotting the graphs
st.title("Likelihood of Change in Likert Rating by Initial Likert Group and Debate Type")

# Set up the plot for each Likert group
groups = df_grouped['likert_group'].unique()

for group in groups:
    plt.figure(figsize=(10, 6))
    df_group = df_grouped[df_grouped['likert_group'] == group]
    
    # Plot a line for each debate type
    sns.lineplot(x='likert_change', y='likelihood', hue='debate_type', data=df_group, marker='o')
    
    # Add labels and title
    plt.title(f"Likelihood of Change for {group}")
    plt.xlabel("Absolute Likert Score Change")
    plt.ylabel("Likelihood of Change")
    plt.legend(title="Debate Type")
    
    # Display the plot using Streamlit
    st.pyplot(plt)

# Step 8: Close the database connection
conn.close()
