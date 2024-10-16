# import sqlite3
# import pandas as pd
# import streamlit as st
# import matplotlib.pyplot as plt

# # Step 1: Connect to the SQLite database
# db_path = 'debate_website_prod_latest.sqlite'
# conn = sqlite3.connect(db_path)

# # Step 2: Load data into a DataFrame
# query = """
#     SELECT 
#         llm_debate_type, 
#         ABS(initial_likert_score - final_likert_score) AS difference_in_ratings
#     FROM debate
#     WHERE initial_likert_score IS NOT NULL AND final_likert_score IS NOT NULL
# """
# df = pd.read_sql_query(query, conn)

# # Step 3: Group by debate type and calculate average difference in ratings
# avg_diff_by_debate_type = df.groupby('llm_debate_type')['difference_in_ratings'].mean().reset_index()

# # Step 4: Create a bar chart using Streamlit and Matplotlib
# st.title("Average Difference in Ratings by Debate Type")

# fig, ax = plt.subplots()
# ax.bar(avg_diff_by_debate_type['llm_debate_type'], avg_diff_by_debate_type['difference_in_ratings'], color='skyblue')
# ax.set_xlabel('Debate Type')
# ax.set_ylabel('Average Difference in Ratings')
# ax.set_title('Average Difference in Ratings by Debate Type')
# plt.xticks(rotation=45)

# # Display the plot in Streamlit
# st.pyplot(fig)

# # Close the connection
# conn.close()

import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Step 2: Load data into a DataFrame
query = """
    SELECT 
        llm_debate_type, 
        ABS(initial_likert_score - final_likert_score) AS difference_in_ratings
    FROM debate
    WHERE initial_likert_score IS NOT NULL 
        AND final_likert_score IS NOT NULL
        AND state = 'finished' 
"""
df = pd.read_sql_query(query, conn)

# Step 3: Group by debate type and calculate average difference in ratings
avg_diff_by_debate_type = df.groupby('llm_debate_type')['difference_in_ratings'].mean().reset_index()

# Step 4: Create a bar chart using Streamlit and Matplotlib
st.title("Average Difference in Ratings by Debate Type")

fig, ax = plt.subplots()
ax.bar(avg_diff_by_debate_type['llm_debate_type'], avg_diff_by_debate_type['difference_in_ratings'], color='skyblue')
ax.set_xlabel('Debate Type')
ax.set_ylabel('Average Difference in Ratings')
ax.set_title('Average Difference in Ratings by Debate Type')
plt.xticks(rotation=45)

# Display the plot in Streamlit
st.pyplot(fig)

# Close the connection
conn.close()
