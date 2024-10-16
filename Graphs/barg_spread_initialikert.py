import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Step 2: Load data into a DataFrame for Initial Likert Scores
query = """
    SELECT initial_likert_score
    FROM debate
    WHERE initial_likert_score IS NOT NULL
    AND state = 'finished'
"""
df = pd.read_sql_query(query, conn)

def group_likert(score):
    if score == 1 or score == 7:
        return '1-7'
    elif score == 2 or score == 6:
        return '2-6'
    elif score == 3 or score == 5:
        return '3-5'
    elif score == 4:
        return '4'
    else:
        return None  # Handle any other cases if needed

df['Likert_group'] = df['initial_likert_score'].apply(group_likert)

# Step 4: Count the number of people in each Likert group
likert_counts = df['Likert_group'].value_counts().sort_index()

# Step 5: Create a bar chart
st.title("Initial Likert Rating Distribution")

fig, ax = plt.subplots()
ax.bar(likert_counts.index, likert_counts.values, color='skyblue')
ax.set_xlabel('Initial Likert Rating Group')
ax.set_ylabel('Number of Participants')
ax.set_title('Initial Likert Ratings Distribution (Grouped)')
plt.xticks(rotation=45)

# Display the plot in Streamlit
st.pyplot(fig)
# print(count1,count2,count3,count4)
# Close the connection
conn.close()
