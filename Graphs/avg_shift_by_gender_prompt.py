# import sqlite3
# import pandas as pd
# import streamlit as st
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Step 1: Connect to the SQLite database
# db_path = 'debate_website_prod_latest.sqlite'
# conn = sqlite3.connect(db_path)

# # Step 2: Query to join debate and user_info table and calculate the rating difference
# query = """
#     SELECT 
#         debate.llm_debate_type AS debate_type, 
#         user_info.gender AS gender, 
#                       CASE
#             -- If the user is "For" and the final score is higher or equal, move towards the user's side (make negative)
#             WHEN debate.user_side = 'FOR' AND debate.final_likert_score > debate.initial_likert_score THEN
#                 debate.final_likert_score - debate.initial_likert_score
#             -- If the user is "Against" and the final score is lower or equal, move towards the user's side (make negative)
#             WHEN debate.user_side = 'AGAINST' AND debate.final_likert_score < debate.initial_likert_score THEN
#                 debate.initial_likert_score - debate.final_likert_score
#             ELSE
#                 ABS(debate.final_likert_score - debate.initial_likert_score)
#         END AS rating_difference
#     FROM debate
#     JOIN user_info ON debate.user_id = user_info.user_id
#     WHERE debate.initial_likert_score IS NOT NULL 
#     AND debate.final_likert_score IS NOT NULL 
#     AND user_info.gender IN ('Male', 'Female')
# """
# df = pd.read_sql_query(query, conn)

# # Step 3: Calculate the average rating change grouped by debate type and gender
# df_avg = df.groupby(['debate_type', 'gender'])['rating_difference'].mean().reset_index()

# # Step 4: Plotting the bar graph using Seaborn and Matplotlib
# st.title("Average Change in Rating by Gender and Debate Type")

# # Set up the plot
# plt.figure(figsize=(10, 6))
# sns.barplot(x='debate_type', y='rating_difference', hue='gender', data=df_avg, palette={'Male': 'blue', 'Female': 'pink'})

# # Add labels and title
# plt.xlabel("Debate Type")
# plt.ylabel("Average Change in Rating")
# plt.title("Average Change in Rating by Gender for Each Debate Type")
# plt.legend(title="Gender")

# # Display the plot using Streamlit
# st.pyplot(plt)

# # Step 5: Close the database connection
# conn.close()



import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Step 2: Query to join debate and user table and calculate the rating difference
query = """
    SELECT 
        debate.llm_debate_type AS debate_type, 
        user_info.gender AS gender, 
                      CASE
            -- If the user is "For" and the final score is higher or equal, move towards the user's side (make negative)
            WHEN debate.user_side = 'FOR' AND debate.final_likert_score > debate.initial_likert_score THEN
                debate.final_likert_score - debate.initial_likert_score
            -- If the user is "Against" and the final score is lower or equal, move towards the user's side (make negative)
            WHEN debate.user_side = 'AGAINST' AND debate.final_likert_score < debate.initial_likert_score THEN
                debate.initial_likert_score - debate.final_likert_score
            ELSE
                ABS(debate.final_likert_score - debate.initial_likert_score)
        END AS rating_difference
    FROM debate
    JOIN user_info ON debate.user_id = user_info.user_id
    JOIN user ON user_info.user_id = user.id  -- Ensure to join the 'user' table for participant_service
    WHERE debate.initial_likert_score IS NOT NULL 
    AND debate.final_likert_score IS NOT NULL 
    AND user_info.gender IN ('Male', 'Female')
    AND debate.state = 'finished'
    AND user.participant_service = 'prolific'
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