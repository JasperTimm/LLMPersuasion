import sqlite3
import pandas as pd

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Step 2: Load data into a DataFrame for Initial and Final Likert Scores
query = """
    SELECT initial_likert_score, final_likert_score
    FROM debate
    WHERE initial_likert_score IS NOT NULL
    AND final_likert_score IS NOT NULL
    AND state = 'finished'
"""
df = pd.read_sql_query(query, conn)

# Step 3: Count the number of people for each Likert score (1 to 7) for initial and final ratings
initial_likert_counts = df['initial_likert_score'].value_counts().sort_index()
final_likert_counts = df['final_likert_score'].value_counts().sort_index()

# Step 4: Display the counts
print("Initial Likert Rating Counts:")
print(initial_likert_counts)

print("\nFinal Likert Rating Counts:")
print(final_likert_counts)

# Step 5: Close the connection
conn.close()
