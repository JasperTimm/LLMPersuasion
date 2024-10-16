# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd
# import sqlite3
# import streamlit as st

# # Connect to the database
# db_path = 'debate_website_prod_latest.sqlite'
# conn = sqlite3.connect(db_path)

# # Query to get the rating differences for both 'argument' and 'argumentllm' debate types
# query = """
#     SELECT 
#         debate.llm_debate_type AS debate_type, 
#         ABS(debate.initial_likert_score - debate.final_likert_score) AS rating_difference
#     FROM debate
#     WHERE debate.initial_likert_score IS NOT NULL 
#     AND debate.final_likert_score IS NOT NULL
#     AND debate.llm_debate_type IN ('argument', 'argumentllm')
# """

# # Load the data into a pandas DataFrame
# df = pd.read_sql_query(query, conn)

# # Streamlit setup
# st.title("Distribution of Rating Change for Argument vs ArgumentLLM Debates")

# # Plotting side-by-side
# fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# # Plot 2: Histogram - Frequency of rating change
# sns.histplot(df[df['debate_type'] == 'argument'], x='rating_difference', color='blue', label='argument', kde=False, bins=10, alpha=0.6, ax=ax[0])
# sns.histplot(df[df['debate_type'] == 'argumentllm'], x='rating_difference', color='orange', label='argumentllm', kde=False, bins=10, alpha=0.6, ax=ax[0])

# ax[0].set_title("Histogram of Rating Change (Argument vs ArgumentLLM)")
# ax[0].set_xlabel("Rating Change (Initial - Final)")
# ax[0].set_ylabel("Frequency")
# ax[0].legend(title="Debate Type")

# # Plot 3: KDE - Kernel Density Estimation for rating change
# sns.kdeplot(df[df['debate_type'] == 'argument']['rating_difference'], color='blue', label='argument', ax=ax[1])
# sns.kdeplot(df[df['debate_type'] == 'argumentllm']['rating_difference'], color='orange', label='argumentllm', ax=ax[1])

# ax[1].set_title("KDE of Rating Change (Argument vs ArgumentLLM)")
# ax[1].set_xlabel("Rating Change (Initial - Final)")
# ax[1].set_ylabel("Density")
# ax[1].legend(title="Debate Type")

# # Display the plots in Streamlit
# st.pyplot(fig)

# # Close the connection
# conn.close()









# import streamlit as st
# import sqlite3
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Connect to the SQLite database
# db_path = 'debate_website_prod_latest.sqlite'
# conn = sqlite3.connect(db_path)

# # Query to get the rating differences by debate type
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

# # Streamlit title
# st.title("Rating Difference Distribution by Debate Type")

# # KDE Plot for Rating Difference
# plt.figure(figsize=(10, 6))

# # Plotting for 'argument' (Human-written)
# sns.kdeplot(
#     data=df[df['debate_type'] == 'argument'], 
#     x='rating_difference', 
#     fill=True, 
#     color='purple', 
#     label='Argument (Human-written)', 
#     alpha=0.6
# )

# # Plotting for 'argumentllm' (LLM-generated)
# sns.kdeplot(
#     data=df[df['debate_type'] == 'argumentllm'], 
#     x='rating_difference', 
#     fill=True, 
#     color='beige', 
#     label='ArgumentLLM (LLM-generated)', 
#     alpha=0.6
# )

# # Add labels and title
# plt.title("Rating Difference Distribution by Debate Type (KDE)")
# plt.xlabel("Absolute Rating Difference")
# plt.ylabel("Density")

# # Add legend
# plt.legend()

# # Display the KDE plot in Streamlit
# st.pyplot(plt)

# # Bar Plot for Rating Difference (absolute number of participants)
# df_count = df.groupby(['debate_type', 'rating_difference']).size().reset_index(name='count')

# # Plotting the bar plot for number of people by debate type
# plt.figure(figsize=(10, 6))
# sns.barplot(x='rating_difference', y='count', hue='debate_type', data=df_count, palette={'argument': 'purple', 'argumentllm': 'beige'})

# # Add labels and title
# plt.title("Number of People by Rating Difference and Debate Type (Bar Plot)")
# plt.xlabel("Absolute Rating Difference")
# plt.ylabel("Number of People")

# # Display the bar plot in Streamlit
# st.pyplot(plt)

# # Close the connection
# conn.close()




import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Query to get the rating differences by debate type
query = """
    SELECT 
        debate.llm_debate_type AS debate_type, 
        ABS(debate.initial_likert_score - debate.final_likert_score) AS rating_difference
    FROM debate
    WHERE debate.initial_likert_score IS NOT NULL 
    AND debate.final_likert_score IS NOT NULL
    AND debate.llm_debate_type IN ('argument', 'argumentllm')
"""
df = pd.read_sql_query(query, conn)

# Streamlit title
st.title("Rating Difference Distribution by Debate Type")

# KDE Plot for Rating Difference using absolute difference
plt.figure(figsize=(10, 6))

# Plotting for 'argument' (Human-written)
sns.kdeplot(
    data=df[df['debate_type'] == 'argument'], 
    x='rating_difference', 
    fill=True, 
    color='purple', 
    label='Argument (Human-written)', 
    alpha=0.6
)

# Plotting for 'argumentllm' (LLM-generated)
sns.kdeplot(
    data=df[df['debate_type'] == 'argumentllm'], 
    x='rating_difference', 
    fill=True, 
    color='beige', 
    label='ArgumentLLM (LLM-generated)', 
    alpha=0.6
)

# Add labels and title
plt.title("Rating Difference Distribution by Debate Type (KDE)")
plt.xlabel("Absolute Rating Difference")
plt.ylabel("Density")

# Add legend
plt.legend()

# Display the KDE plot in Streamlit
st.pyplot(plt)

# Bar Plot for Rating Difference (absolute number of participants)
df_count = df.groupby(['debate_type', 'rating_difference']).size().reset_index(name='count')

# Plotting the bar plot for number of people by debate type
plt.figure(figsize=(10, 6))
sns.barplot(x='rating_difference', y='count', hue='debate_type', data=df_count, palette={'argument': 'purple', 'argumentllm': 'beige'})

# Add labels and title
plt.title("Number of People by Rating Difference and Debate Type (Bar Plot)")
plt.xlabel("Absolute Rating Difference")
plt.ylabel("Number of People")

# Display the bar plot in Streamlit
st.pyplot(plt)

# Close the connection
conn.close()
