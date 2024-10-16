# import sqlite3
# import pandas as pd
# import matplotlib.pyplot as plt
# import streamlit as st

# # Step 1: Connect to the SQLite database
# db_path = 'debate_website_prod_latest.sqlite'
# conn = sqlite3.connect(db_path)

# # Step 2: Fetch the data with initial Likert scores
# query = """
#     SELECT debate.initial_likert_score AS initial_score
#     FROM debate
#     WHERE debate.initial_likert_score IS NOT NULL
# """
# df = pd.read_sql_query(query, conn)

# # Step 3: Apply the Likert score transformation (mod 7)
# df['mod_likert'] = abs(df['initial_score'] - 4)

# # Step 4: Count the frequency of each modded Likert score
# df_count = df['mod_likert'].value_counts().sort_index().reset_index()
# df_count.columns = ['mod_likert', 'count']

# # Step 5: Plotting the bar graph using Matplotlib
# st.title("Spread of Initial Opinions (Based on Modded Likert Scores)")

# plt.figure(figsize=(10, 6))
# plt.bar(df_count['mod_likert'], df_count['count'], color='purple')

# # Add labels and title
# plt.xlabel("Deviation from Neutral (Likert mod 7)")
# plt.ylabel("Count of Initial Opinions")
# plt.title("Spread of Initial Opinions Based on Modded Likert Scores (Neutral = 0)")

# # Display the plot in Streamlit
# st.pyplot(plt)

# # Close the database connection
# conn.close()
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)

# Step 2: Fetch the data with initial Likert scores
query = """
    SELECT debate.initial_likert_score AS initial_score
    FROM debate
    WHERE debate.initial_likert_score IS NOT NULL
"""
df = pd.read_sql_query(query, conn)

# Step 3: Separate scores into agreement and disagreement categories
df['deviation'] = df['initial_score'] - 4
df['category'] = df['deviation'].apply(lambda x: 'agreement' if x > 0 else 'disagreement')

# Step 4: Create a new column with absolute values for deviations
df['abs_deviation'] = abs(df['deviation'])

# Step 5: Count the frequency of each deviation level for agreement and disagreement
df_agree = df[df['category'] == 'agreement']['abs_deviation'].value_counts().sort_index().reset_index()
df_agree.columns = ['deviation', 'count']
df_agree['count'] = df_agree['count'] * -1  # Negative values for agreement (right side of the graph)

df_disagree = df[df['category'] == 'disagreement']['abs_deviation'].value_counts().sort_index().reset_index()
df_disagree.columns = ['deviation', 'count']

# Step 6: Merge the two datasets
df_combined = pd.merge(df_agree, df_disagree, on='deviation', how='outer', suffixes=('_agree', '_disagree')).fillna(0)

# Step 7: Plotting the bi-directional bar graph using Matplotlib
st.title("Spread of Initial Opinions (Bi-Directional)")

plt.figure(figsize=(10, 6))
plt.bar(df_combined['deviation'], df_combined['count_agree'], color='green', label='Agreement')
plt.bar(df_combined['deviation'], df_combined['count_disagree'], color='red', label='Disagreement')

# Add labels and title
plt.xlabel("Deviation from Neutral (Strength of Opinion)")
plt.ylabel("Count of Initial Opinions")
plt.title("Bi-Directional Spread of Initial Opinions")
plt.legend()

# Display the plot in Streamlit
st.pyplot(plt)

# Close the database connection
conn.close()
