# import sqlite3
# import pandas as pd
# import numpy as np
# import streamlit as st
# import matplotlib.pyplot as plt

# # Step 1: Connect to the SQLite database
# db_path = 'debate_website_prod_latest.sqlite'
# conn = sqlite3.connect(db_path)

# # Step 2: Load data from the debate table
# query = """
#     SELECT 
#         llm_debate_type,
#         initial_likert_score,
#         final_likert_score,
#         rating_difference,
#         user_side
#     FROM debate
#     WHERE initial_likert_score IS NOT NULL AND final_likert_score IS NOT NULL AND rating_difference IS NOT NULL
#     AND debate.state = 'finished'
# """
# df = pd.read_sql_query(query, conn)

# # Step 3: Calculate the mean rating difference for each debate type
# mean_diff_by_debate_type = df.groupby('llm_debate_type')['rating_difference'].mean().reset_index()

# # Step 3: Define the function to calculate weighted difference using division normalization
# def calculate_weighted_diff_division(row):
#     initial = row['initial_likert_score']
#     final = row['final_likert_score']
#     side = row['user_side']
    
#     # Calculate the absolute difference
#     rating_diff = abs(final - initial)
    
#     # Normalize weight by dividing by mean_diff_by_debate_type
#     (change this code) weight = rating_diff/
    
#     # Adjust for user-side: Positive if AI persuades toward its side, negative otherwise
#     if (side == 'FOR' and final < initial) or (side == 'AGAINST' and final > initial):
#         weighted_diff = rating_diff * weight
#     else:
#         weighted_diff = 0  # No change toward AI's side
    
#     return weighted_diff

# # Step 4: Apply the function to calculate weighted differences
# df['weighted_diff'] = df.apply(calculate_weighted_diff_division, axis=1)

# # Step 5: Calculate the weighted mean for each debate type (normalized by division)
# weighted_mean_df = df.groupby('llm_debate_type').apply(
#     lambda group: np.average(group['weighted_diff'], weights=(abs(group['initial_likert_score'] - 4) / 3))
# ).reset_index(name='weighted_mean')

# # Step 6: Prepare Streamlit page title
# st.title("Weighted Rating Difference by Debate Type (Division Normalization)")

# # Step 7: Create a bar chart for each debate type
# fig, ax = plt.subplots()
# ax.bar(weighted_mean_df['llm_debate_type'], weighted_mean_df['weighted_mean'], color='skyblue')

# ax.set_xlabel('Debate Type')
# ax.set_ylabel('Weighted Mean of Rating Differences')
# ax.set_title('Weighted Rating Difference for Each Debate Type (Using Division Normalization)')

# # Rotate x-axis labels for better readability
# plt.xticks(rotation=45)

# # Step 8: Display the chart using Streamlit
# st.pyplot(fig)

# # Step 9: Close the database connection
# conn.close()
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Step 2: Load data from the debate table
query = """
    SELECT 
        llm_debate_type,
        initial_likert_score,
        final_likert_score,
        rating_difference,
        user_side
    FROM debate
    WHERE initial_likert_score IS NOT NULL AND final_likert_score IS NOT NULL 
    AND rating_difference IS NOT NULL
    AND debate.state = 'finished'
"""
df = pd.read_sql_query(query, conn)

# Step 3: Calculate the mean rating difference for each debate type
mean_diff_by_debate_type = df.groupby('llm_debate_type')['rating_difference'].mean().reset_index()
mean_diff_by_debate_type.columns = ['llm_debate_type', 'mean_diff']

# Step 4: Merge the mean differences with the original dataframe
df = df.merge(mean_diff_by_debate_type, on='llm_debate_type')

# Step 5: Define the function to calculate weighted difference using division normalization
def calculate_weighted_diff_division(row):
    initial = row['initial_likert_score']
    final = row['final_likert_score']
    side = row['user_side']
    
    # Calculate the absolute difference
    rating_diff = abs(final - initial)
    
    # Normalize weight by dividing rating difference by mean difference for that debate type
    if row['mean_diff'] != 0:  # Avoid division by zero
        weight = rating_diff / row['mean_diff']
    else:
        weight = 0
    weighted_diff = rating_diff * weight
    # Adjust for user-side: Positive if AI persuades toward its side, negative otherwise
    # if (side == 'FOR' and final < initial) or (side == 'AGAINST' and final > initial):
        
    # else:
    #     weighted_diff = 0  # No change toward AI's side
    
    return weighted_diff

# Step 6: Apply the function to calculate weighted differences
df['weighted_diff'] = df.apply(calculate_weighted_diff_division, axis=1)

# Step 7: Calculate the weighted mean for each debate type (normalized by division)
weighted_mean_df = df.groupby('llm_debate_type').apply(
    lambda group: np.average(group['weighted_diff'], weights=(abs(group['initial_likert_score'] - 4) / 3))
).reset_index(name='weighted_mean')

# Step 8: Prepare Streamlit page title
st.title("Weighted Rating Difference by Debate Type (Division Normalization)")

# Step 9: Create a bar chart for each debate type
fig, ax = plt.subplots()
ax.bar(weighted_mean_df['llm_debate_type'], weighted_mean_df['weighted_mean'], color='skyblue')

ax.set_xlabel('Debate Type')
ax.set_ylabel('Weighted Mean of Rating Differences')
ax.set_title('Weighted Rating Difference for Each Debate Type (Using Division Normalization)')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Step 10: Display the chart using Streamlit
st.pyplot(fig)

# Step 11: Close the database connection
conn.close()
