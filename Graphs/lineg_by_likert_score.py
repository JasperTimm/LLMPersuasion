import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Step 2: Fetch the data with initial and final Likert scores
query = """
    SELECT 
        debate.llm_debate_type AS debate_type,
        debate.initial_likert_score AS initial_score,
        ABS(debate.initial_likert_score - debate.final_likert_score) AS rating_difference
    FROM debate
    WHERE debate.initial_likert_score IS NOT NULL 
    AND debate.final_likert_score IS NOT NULL
"""
df = pd.read_sql_query(query, conn)

# Step 3: Define the initial Likert scores we care about (e.g., 1, 2, 3, 4, etc.)
initial_scores = [1, 2, 3, 4]

# Step 4: Set up the Streamlit page title
st.title("Likelihood of Absolute Likert Score Change by Debate Type and Initial Likert Score")

# Step 5: Loop over each initial Likert score and create a separate line graph
for score in initial_scores:
    # Filter the data for the specific initial Likert score
    df_filtered = df[df['initial_score'] == score]

    # Calculate the total number of debates for each debate type and Likert score
    total_debates_by_type = df_filtered.groupby('debate_type')['rating_difference'].count().reset_index(name='total_debates')

    # Count the number of debates with each absolute Likert score change for each debate type
    df_count = df_filtered.groupby(['debate_type', 'rating_difference']).size().reset_index(name='count')

    # Merge the total debate counts to calculate percentage likelihood
    df_merged = pd.merge(df_count, total_debates_by_type, on='debate_type')

    # Calculate the percentage likelihood of each absolute Likert score change for each debate type
    df_merged['likelihood_percentage'] = (df_merged['count'] / df_merged['total_debates']) * 100

    # Step 6: Plot the line graph for the current initial Likert score
    st.subheader(f"Initial Likert Score: {score}")
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='rating_difference', y='likelihood_percentage', hue='debate_type', data=df_merged, marker="o")

    # Add labels and title for each graph
    plt.xlabel("Absolute Likert Score Change")
    plt.ylabel("Percentage Likelihood (%)")
    plt.title(f"Likelihood of Likert Score Change for Initial Score {score} by Debate Type")
    plt.legend(title="Debate Type", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Display the graph in Streamlit
    st.pyplot(plt)

# Close the database connection
conn.close()
