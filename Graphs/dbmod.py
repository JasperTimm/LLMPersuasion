import sqlite3
from datetime import datetime

# Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'  # Update with your actual database path
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Define the date threshold for deleting debates before 2024-10-13
date_threshold = '2024-10-13'

# Fetch all debate IDs where the timestamp is before the threshold
cursor.execute("""
    SELECT id FROM debate
    WHERE id IN (
        SELECT debate_id FROM debate_log
        WHERE timestamp < ?
    )
""", (date_threshold,))
debate_ids = cursor.fetchall()

# If no debates found, exit
if not debate_ids:
    print("No debates found before the specified date.")
else:
    # Convert debate_ids to a flat list
    debate_ids = [debate_id[0] for debate_id in debate_ids]

    # Delete from copy_paste_event, debate_log, debate_result, and debate tables
    cursor.execute("DELETE FROM copy_paste_event WHERE debate_id IN ({})".format(','.join('?'*len(debate_ids))), debate_ids)
    cursor.execute("DELETE FROM debate_log WHERE debate_id IN ({})".format(','.join('?'*len(debate_ids))), debate_ids)
    cursor.execute("DELETE FROM debate_result WHERE debate_id IN ({})".format(','.join('?'*len(debate_ids))), debate_ids)
    cursor.execute("DELETE FROM debate WHERE id IN ({})".format(','.join('?'*len(debate_ids))), debate_ids)

    # Commit the changes
    conn.commit()

    print(f"Deleted {len(debate_ids)} debates and associated records.")

# Close the connection
conn.close()

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


#-----------------------------------------------------------------------------------------------
import sqlite3

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Step 2: Create the "for_review" table with the topic description added
cursor.execute("""
    CREATE TABLE IF NOT EXISTS for_review AS
    SELECT 
        user.id AS user_id,
        user.username,
        user.participant_id,
        user.participant_status,
        debate.id AS debate_id,
        debate.user_side,
        debate.ai_side,
        debate.initial_likert_score,
        debate.final_likert_score,
        ABS(debate.initial_likert_score - debate.final_likert_score) AS rating_difference,
        debate.state,
        debate.initial_opinion,
        debate.user_responses,
        debate.llm_responses,
        debate.final_opinion,
        debate.final_likert_score,
        debate.inactive_time,
        debate_count,
        debate_result.review_reasons AS reason_for_review,
        topic.description AS topic_description
    FROM user
    JOIN debate ON user.id = debate.user_id
    LEFT JOIN debate_result ON debate.id = debate_result.debate_id
    LEFT JOIN topic ON debate.topic_id = topic.id  -- Join with topic table to get the description
    WHERE user.participant_status LIKE '%NEEDS_REVIEW%'
""")

# Step 3: Commit the transaction and close the connection
conn.commit()
conn.close()

print("Table 'for_review' created successfully with topic description added.")
