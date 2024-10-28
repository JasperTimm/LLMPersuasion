import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Step 2: Load data from the debate table
query = """
    SELECT 
        llm_debate_type,        CASE
            -- If the user is "For" and the final score is higher or equal, move towards the user's side (make negative)
            WHEN debate.user_side = 'FOR' AND debate.final_likert_score > debate.initial_likert_score THEN
                debate.initial_likert_score - debate.final_likert_score
            -- If the user is "Against" and the final score is lower or equal, move towards the user's side (make negative)
            WHEN debate.user_side = 'AGAINST' AND debate.final_likert_score < debate.initial_likert_score THEN
                debate.final_likert_score - debate.initial_likert_score
            ELSE
                ABS(debate.final_likert_score - debate.initial_likert_score)  -- Retain the sign for differences
        END AS difference_in_ratings
    FROM debate
    WHERE initial_likert_score IS NOT NULL AND final_likert_score IS NOT NULL
    AND debate.state = 'finished'
"""
df = pd.read_sql_query(query, conn)

# Step 3: Prepare Streamlit page title
st.title("Rating Difference Visualization for Each Debate Type")

# Step 4: Get unique debate types
debate_types = df['llm_debate_type'].unique()

# Step 5: Create a plot for each debate type
for debate_type in debate_types:
    # Filter data for the current debate type
    df_filtered = df[df['llm_debate_type'] == debate_type]
    
    # Count the number of debates for each rating difference
    rating_difference_counts = df_filtered['difference_in_ratings'].value_counts().sort_index()
    
    # Step 6: Plot the bar chart for the current debate type
    st.subheader(f"Debate Type: {debate_type}")
    
    fig, ax = plt.subplots()
    ax.bar(rating_difference_counts.index, rating_difference_counts.values, color='skyblue')
    
    ax.set_xlabel('Difference in Rating')
    ax.set_ylabel('Number of Debates')
    ax.set_title(f'Distribution of Rating Differences for {debate_type} Debates')
    
    # Set x-axis ticks based on the range of rating differences (negative to positive)
    ax.set_xticks(rating_difference_counts.index)  
    
    # Display the chart using Streamlit
    st.pyplot(fig)

# Step 7: Close the database connection
conn.close()