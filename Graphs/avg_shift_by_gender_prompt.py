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
        user_info.gender AS gender, 
        ABS(debate.initial_likert_score - debate.final_likert_score) AS rating_difference
    FROM debate
    JOIN user_info ON debate.user_id = user_info.user_id
    WHERE debate.initial_likert_score IS NOT NULL 
    AND debate.final_likert_score IS NOT NULL 
    AND user_info.gender IN ('Male', 'Female')
"""
df = pd.read_sql_query(query, conn)

# Step 3: Calculate the average rating change grouped by debate type and gender
df_avg = df.groupby(['debate_type', 'gender'])['rating_difference'].mean().reset_index()

# Step 4: Plotting the bar graph using Seaborn and Matplotlib
st.title("Average Change in Rating by Gender and Debate Type")

# Set up the plot
plt.figure(figsize=(10, 6))
sns.barplot(x='debate_type', y='rating_difference', hue='gender', data=df_avg, palette={'Male': 'blue', 'Female': 'pink'})

# Add labels and title
plt.xlabel("Debate Type")
plt.ylabel("Average Change in Rating")
plt.title("Average Change in Rating by Gender for Each Debate Type")
plt.legend(title="Gender")

# Display the plot using Streamlit
st.pyplot(plt)

# Step 5: Close the database connection
conn.close()
