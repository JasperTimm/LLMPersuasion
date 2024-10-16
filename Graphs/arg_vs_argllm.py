# import sqlite3
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import streamlit as st

# # Connect to the SQLite database
# db_path = 'debate_website_prod_latest.sqlite'
# conn = sqlite3.connect(db_path)

# # Query to get the data for argument and argumentllm debate types
# query = """
#     SELECT 
#         debate.llm_debate_type AS debate_type, 
#         ABS(debate.initial_likert_score - debate.final_likert_score) AS rating_difference
#     FROM debate
#     WHERE debate.initial_likert_score IS NOT NULL 
#     AND debate.final_likert_score IS NOT NULL 
#     AND debate.llm_debate_type IN ('argument', 'argumentllm')
# """
# df = pd.read_sql_query(query, conn)
# conn.close()

# # Calculate the average change in rating for each debate type
# df_avg_change = df.groupby('debate_type')['rating_difference'].mean().reset_index()

# # Plotting the average change in rating for both debate types
# st.title("Average Change in Rating by Debate Type")

# # Plot 2: Average Change in Rating
# plt.figure(figsize=(10, 6))
# sns.barplot(x='debate_type', y='rating_difference', data=df_avg_change, palette='viridis')
# plt.xlabel("Debate Type")
# plt.ylabel("Average Rating Change")
# plt.title("Average Change in Rating for Argument vs ArgumentLLM Debates")
# st.pyplot(plt)

# # Plotting the distribution of rating changes
# st.title("Distribution of Rating Change by Debate Type")

# # Plot 3: Distribution of Rating Change
# plt.figure(figsize=(10, 6))
# sns.histplot(data=df, x='rating_difference', hue='debate_type', kde=True, palette='coolwarm')
# plt.xlabel("Rating Change (Initial - Final)")
# plt.ylabel("Frequency")
# plt.title("Distribution of Rating Change for Argument vs ArgumentLLM Debates")
# st.pyplot(plt)










# import sqlite3
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import streamlit as st

# # Connect to the SQLite database
# db_path = 'debate_website_prod_latest.sqlite'
# conn = sqlite3.connect(db_path)

# # Query to get the data for argument and argumentllm debate types, considering positive and negative rating differences
# query = """
#     SELECT 
#         debate.llm_debate_type AS debate_type, 
#         debate.user_side,
#         debate.initial_likert_score,
#         debate.final_likert_score,
#                CASE
#             -- If the user is "For" and the final score is higher or equal, move towards the user's side (make negative)
#             WHEN debate.user_side = 'FOR' AND debate.final_likert_score > debate.initial_likert_score THEN
#                 debate.initial_likert_score - debate.final_likert_score
#             -- If the user is "Against" and the final score is lower or equal, move towards the user's side (make negative)
#             WHEN debate.user_side = 'AGAINST' AND debate.final_likert_score < debate.initial_likert_score THEN
#                 debate.final_likert_score - debate.initial_likert_score
#             ELSE
#                 ABS(debate.final_likert_score - debate.initial_likert_score)
#         END AS rating_difference
#     FROM debate
#     WHERE debate.initial_likert_score IS NOT NULL 
#     AND debate.final_likert_score IS NOT NULL 
#     AND debate.llm_debate_type IN ('argument', 'argumentllm')
# """
# df = pd.read_sql_query(query, conn)
# conn.close()

# # Calculate the average change in rating for each debate type, including the negative rating differences
# df_avg_change = df.groupby('debate_type')['rating_difference'].mean().reset_index()

# # Plotting the average change in rating for both debate types
# st.title("Average Change in Rating by Debate Type")

# # Plot 2: Average Change in Rating
# plt.figure(figsize=(10, 6))
# sns.barplot(x='debate_type', y='rating_difference', data=df_avg_change, palette='viridis')
# plt.xlabel("Debate Type")
# plt.ylabel("Average Rating Change")
# plt.title("Average Change in Rating for Argument vs ArgumentLLM Debates")
# st.pyplot(plt)







import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Query to get the data for 'argument' and 'argumentllm' debate types, considering positive and negative rating differences
query = """
    SELECT 
        debate.llm_debate_type AS debate_type, 
        debate.user_side,
        debate.initial_likert_score,
        debate.final_likert_score,
        CASE
            -- If the user is "For" and the final score is higher or equal, move towards the user's side (make negative)
            WHEN debate.user_side = 'FOR' AND debate.final_likert_score > debate.initial_likert_score THEN
                debate.initial_likert_score - debate.final_likert_score
            -- If the user is "Against" and the final score is lower or equal, move towards the user's side (make negative)
            WHEN debate.user_side = 'AGAINST' AND debate.final_likert_score < debate.initial_likert_score THEN
                debate.final_likert_score - debate.initial_likert_score
            ELSE
                ABS(debate.final_likert_score - debate.initial_likert_score)
        END AS rating_difference
    FROM debate
    JOIN user_info ON debate.user_id = user_info.user_id
    JOIN user ON user_info.user_id = user.id  -- Join the 'user' table for participant_service
    WHERE debate.initial_likert_score IS NOT NULL 
    AND debate.final_likert_score IS NOT NULL 
    AND debate.llm_debate_type IN ('argument', 'argumentllm')
    AND debate.state = 'finished'
    AND user.participant_service = 'prolific'  -- Ensure to filter by 'participant_service'
"""

df = pd.read_sql_query(query, conn)
conn.close()

# Calculate the average change in rating for each debate type, including the negative rating differences
df_avg_change = df.groupby('debate_type')['rating_difference'].mean().reset_index()

# Plotting the average change in rating for both debate types
st.title("Average Change in Rating by Debate Type")

# Plot 2: Average Change in Rating
plt.figure(figsize=(10, 6))
sns.barplot(x='debate_type', y='rating_difference', data=df_avg_change, palette='viridis')
plt.xlabel("Debate Type")
plt.ylabel("Average Rating Change")
plt.title("Average Change in Rating for Argument vs ArgumentLLM Debates")
st.pyplot(plt)
