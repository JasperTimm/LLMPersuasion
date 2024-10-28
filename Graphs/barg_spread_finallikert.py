import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Step 2: Load data into a DataFrame for Final Likert Scores
query = """
    SELECT final_likert_score
    FROM debate
    WHERE final_likert_score IS NOT NULL
    AND state = 'finished'
"""
df = pd.read_sql_query(query, conn)

# Function to group Likert scores
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

# Group the final Likert scores
df['Final_Likert_group'] = df['final_likert_score'].apply(group_likert)

# Step 3: Count the number of people in each Likert group for final scores
final_likert_counts = df['Final_Likert_group'].value_counts().sort_index()

# Step 4: Create a bar chart for final Likert scores
st.title("Final Likert Rating Distribution")

fig, ax = plt.subplots()
ax.bar(final_likert_counts.index, final_likert_counts.values, color='lightgreen')
ax.set_xlabel('Final Likert Rating Group')
ax.set_ylabel('Number of Participants')
ax.set_title('Final Likert Ratings Distribution (Grouped)')
plt.xticks(rotation=45)

# Display the plot in Streamlit
st.pyplot(fig)

# Close the connection
conn.close()
