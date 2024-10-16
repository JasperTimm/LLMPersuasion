import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Step 2: Load data from the debate table with weighted differences
query = """
    SELECT 
        llm_debate_type,
        debate.user_side,
        debate.initial_likert_score,
        debate.final_likert_score,
        ABS(debate.initial_likert_score - 4) AS weight_factor,  -- Calculate weight based on distance from 4
        CASE
            -- If the user is "FOR" and the final score is higher, move towards the user's side (negative difference)
            WHEN debate.user_side = 'FOR' AND debate.final_likert_score > debate.initial_likert_score THEN
                (debate.initial_likert_score - debate.final_likert_score) * ABS(debate.initial_likert_score - 4)
            -- If the user is "FOR" and the final score is lower, move against the user's side (positive difference)
            WHEN debate.user_side = 'FOR' AND debate.final_likert_score < debate.initial_likert_score THEN
                (debate.initial_likert_score - debate.final_likert_score) * ABS(debate.initial_likert_score - 4)
            -- If the user is "AGAINST" and the final score is higher, move against the user's side (positive difference)
            WHEN debate.user_side = 'AGAINST' AND debate.final_likert_score > debate.initial_likert_score THEN
                (debate.final_likert_score - debate.initial_likert_score) * ABS(debate.initial_likert_score - 4)
            -- If the user is "AGAINST" and the final score is lower, move towards the user's side (negative difference)
            WHEN debate.user_side = 'AGAINST' AND debate.final_likert_score < debate.initial_likert_score THEN
                (debate.final_likert_score - debate.initial_likert_score) * ABS(debate.initial_likert_score - 4)
            ELSE
                (debate.final_likert_score - debate.initial_likert_score) * ABS(debate.initial_likert_score - 4)
        END AS weighted_difference
    FROM debate
    WHERE initial_likert_score IS NOT NULL 
      AND final_likert_score IS NOT NULL
      AND debate.state = 'finished'
"""
df = pd.read_sql_query(query, conn)

# Step 3: Prepare Streamlit page title
st.title("Weighted Rating Difference Visualization for Each Debate Type")

# Step 4: Get unique debate types
debate_types = df['llm_debate_type'].unique()

# Step 5: Create a plot for each debate type
for debate_type in debate_types:
    # Filter data for the current debate type
    df_filtered = df[df['llm_debate_type'] == debate_type]
    
    # Count the number of debates for each weighted rating difference
    weighted_difference_counts = df_filtered['weighted_difference'].value_counts().sort_index()
    
    # Step 6: Plot the bar chart for the current debate type
    st.subheader(f"Debate Type: {debate_type}")
    
    fig, ax = plt.subplots()
    ax.bar(weighted_difference_counts.index, weighted_difference_counts.values, color='skyblue')
    
    ax.set_xlabel('Weighted Difference in Rating')
    ax.set_ylabel('Number of Debates')
    ax.set_title(f'Weighted Distribution of Rating Differences for {debate_type} Debates')
    
    # Set x-axis ticks based on the range of weighted rating differences (negative to positive)
    ax.set_xticks(weighted_difference_counts.index)  
    
    # Display the chart using Streamlit
    st.pyplot(fig)

# Step 7: Close the database connection
conn.close()
