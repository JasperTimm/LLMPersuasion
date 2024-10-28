# import pandas as pd
# import sqlite3

# # Connect to the database
# db_path = 'debate_website_prod_latest.sqlite'
# conn = sqlite3.connect(db_path)

# # Step 1: Get debate logs with initial and final timestamps for each debate
# query_logs = """
#     SELECT 
#         debate_id, 
#         MIN(timestamp) AS start_time, 
#         MAX(timestamp) AS end_time 
#     FROM debate_log
#     GROUP BY debate_id
# """
# logs_df = pd.read_sql_query(query_logs, conn)

# # Step 2: Merge with debate details and rating differences
# query_debate_details = """
#     SELECT 
#         debate.id AS debate_id, 
#         debate.llm_debate_type, 
#         debate.rating_difference
#     FROM debate
# """
# debate_df = pd.read_sql_query(query_debate_details, conn)

# # Merge logs with debate details
# df = pd.merge(logs_df, debate_df, on='debate_id')

# # Step 3: Calculate duration in minutes (or seconds if more precise data is needed)
# df['duration'] = (pd.to_datetime(df['end_time']) - pd.to_datetime(df['start_time'])).dt.total_seconds() / 60

# # Step 4: Define time intervals based on percentiles to categorize debate durations
# percentiles = df['duration'].quantile([0.2, 0.4, 0.6, 0.8]).tolist()
# intervals = [0] + percentiles + [df['duration'].max()]

# # Categorize each debate into one of the five time intervals
# df['duration_category'] = pd.cut(df['duration'], bins=intervals, labels=["Very Short", "Short", "Medium", "Long", "Very Long"])

# # Close the connection
# conn.close()

# # Display the categorized DataFrame
# df[['debate_id', 'llm_debate_type', 'rating_difference', 'duration', 'duration_category']]
import streamlit as st
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to the database and retrieve data
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Load the debate duration data
query = """SELECT * 
            FROM debate_duration_categories
            WHERE rating_difference IS NOT NULL
            AND debate_state = 'finished'

"""
duration_df = pd.read_sql_query(query, conn)
conn.close()

# Visualization 1: Bar Chart of Average Rating Differences by Duration Category
st.title("Average Rating Difference by Debate Duration Category")
avg_rating_diff = duration_df.groupby('duration_category')['rating_difference'].mean()
st.bar_chart(avg_rating_diff)

# Visualization 2: Line Chart of Debate Duration Distribution by Debate Type
st.title("Debate Duration Distribution by Debate Type")
duration_by_type = duration_df.groupby(['llm_debate_type', 'duration_category']).size().unstack()
st.line_chart(duration_by_type)

# Visualization 3: Scatter Plot of Duration vs. Rating Difference
st.title("Duration vs. Rating Difference")
fig, ax = plt.subplots()
sns.scatterplot(data=duration_df, x='duration', y='rating_difference', hue='duration_category', ax=ax)
plt.xlabel("Debate Duration (minutes)")
plt.ylabel("Rating Difference")
st.pyplot(fig)
