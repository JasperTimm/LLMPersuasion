import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Step 2: Query the data for final Likert score
query = """
    SELECT 
        debate.final_likert_score AS final_rating,
        ABS(debate.final_likert_score - 4) AS rating_difference
    FROM debate
    WHERE debate.final_likert_score IS NOT NULL
"""

# Step 3: Fetch data into a DataFrame
df = pd.read_sql_query(query, conn)

# Step 4: Group by final Likert score (mod 7) and count the number of people
df['rating_difference_mod'] = df['rating_difference'] % 7

# Step 5: Plotting the bi-directional bar graph for final Likert score
st.title("Final Likert Rating Distribution")

# Create bi-directional bars
plt.figure(figsize=(10, 6))
sns.barplot(x='rating_difference_mod', y='final_rating', data=df, palette="coolwarm", orient='h')

# Add titles and labels
plt.xlabel("Absolute Difference from Neutral (4)")
plt.ylabel("Final Likert Rating")
plt.title("Final Likert Rating Distribution with Absolute Difference from Neutral (4)")

# Show the plot using Streamlit
st.pyplot(plt)

# Step 6: Close the connection
conn.close()
