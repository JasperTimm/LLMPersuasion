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
        llm_debate_type, 
        ABS(initial_likert_score - final_likert_score) AS difference_in_ratings
    FROM debate
    WHERE initial_likert_score IS NOT NULL AND final_likert_score IS NOT NULL
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
    ax.set_xlabel('Difference in Rating (0 to 6)')
    ax.set_ylabel('Number of Debates')
    ax.set_title(f'Distribution of Rating Differences for {debate_type} Debates')
    ax.set_xticks(range(7))  # Set x-axis ticks for 0 to 6
    
    # Display the chart using Streamlit
    st.pyplot(fig)

# Step 7: Close the database connection
conn.close()
