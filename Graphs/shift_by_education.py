import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import re

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Step 2: Fetch the data from the relevant tables
query = """
    SELECT 
        debate.llm_debate_type AS debate_type,
        user_info.education_level AS education_level,
        debate.rating_difference AS rating_difference
    FROM debate
    JOIN user_info ON debate.user_id = user_info.user_id
    WHERE debate.initial_likert_score IS NOT NULL 
    AND debate.final_likert_score IS NOT NULL 
    AND user_info.education_level IS NOT NULL
    AND debate.state = 'finished'
"""
df = pd.read_sql_query(query, conn)

# Step 3: Group education levels into categories
def categorize_education(education):
    education = education.lower().strip()
    if re.search(r'some college', education):
        return 'Some college, no degree'
    elif re.search(r'high school|ged', education):
        return 'High school diploma'
    elif re.search(r'bachelor|associate|undergraduate', education):
        return "Bachelor's/Undergraduate/Associate"
    elif re.search(r'master|postgraduate', education):
        return "Master's/Postgraduate"
    elif re.search(r'phd|doctor', education):
        return 'PhD'
    else:
        return 'Other'

df['education_category'] = df['education_level'].apply(categorize_education)

# Step 4: Remove the "Other" category
df = df[df['education_category'] != 'Other']

# Step 5: Group data by debate type and education category, and calculate the average rating difference
df_avg = df.groupby(['debate_type', 'education_category'])['rating_difference'].mean().reset_index()

# Step 6: Set up the Streamlit title
st.title("Average Change in Rating by Education Level and Debate Type")

# Step 7: Plot the bar graph using Seaborn and Matplotlib
plt.figure(figsize=(12, 6))
sns.barplot(x='debate_type', y='rating_difference', hue='education_category', data=df_avg)

# Add labels and title
plt.xlabel("Debate Type")
plt.ylabel("Average Change in Rating")
plt.title("Average Change in Rating by Education Level for Each Debate Type")
plt.legend(title="Education Level", bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(plt)

# Close the database connection
conn.close()
