# import sqlite3

# # Connect to the SQLite database
# db_path = 'debate_website_prod_latest.sqlite'
# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()

# # Step 1: Create a new table with an additional debate type column
# cursor.execute("""
#     CREATE TABLE debate_summary_with_type (
#         id VARCHAR NOT NULL PRIMARY KEY,
#         user_side VARCHAR NOT NULL,
#         ai_side VARCHAR NOT NULL,
#         initial_likert_score INTEGER,
#         final_likert_score INTEGER,
#         difference_in_ratings INTEGER,
#         debate_type VARCHAR NOT NULL
#     )
# """)
# print("New table 'debate_summary_with_type' created successfully.")

# # Step 2: Insert data into the new table from the existing 'debate' table
# cursor.execute("""
#     INSERT INTO debate_summary_with_type (id, user_side, ai_side, initial_likert_score, final_likert_score, difference_in_ratings, debate_type)
#     SELECT 
#         debate.id, 
#         debate.user_side, 
#         debate.ai_side, 
#         debate.initial_likert_score, 
#         debate.final_likert_score, 
#         ABS(debate.initial_likert_score - debate.final_likert_score) AS difference_in_ratings,
#         debate.llm_debate_type AS debate_type
#     FROM debate
#     WHERE debate.initial_likert_score IS NOT NULL AND debate.final_likert_score IS NOT NULL
# """)
# print("Data inserted into 'debate_summary' with debate type included.")

# # Commit the changes and close the connection
# conn.commit()
# conn.close()

# print("New table 'debate_summary_with_type' created and populated successfully.")
import sqlite3

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Step 2: Create the updated debate_summary_with_type_and_gender table with an added gender column
cursor.execute("""
    CREATE TABLE IF NOT EXISTS debate_summary_with_type_and_gender AS
    SELECT 
        debate.id AS debate_id,
        debate.user_side,
        debate.ai_side,
        debate.initial_likert_score AS initial_rating,
        debate.final_likert_score AS final_rating,
        ABS(debate.initial_likert_score - debate.final_likert_score) AS rating_difference,
        debate.llm_debate_type AS debate_type,
        user_info.gender AS gender
    FROM debate
    JOIN user_info ON debate.user_id = user_info.user_id
""")

# Step 3: Commit the transaction and close the connection
conn.commit()
conn.close()

print("Table 'debate_summary_with_type_and_gender' created successfully with gender column.")
