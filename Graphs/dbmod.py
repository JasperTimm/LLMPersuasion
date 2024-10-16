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
from datetime import datetime

# Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'  # Update with your actual database path
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Step 1: Identify participants who are not 'prolific' or have NULL in participant_service
cursor.execute("""
    SELECT user.id 
    FROM user
    WHERE user.participant_service IS NULL 
    OR user.participant_service != 'prolific'
""")
non_prolific_user_ids = cursor.fetchall()

# If no non-prolific users found, exit
if not non_prolific_user_ids:
    print("No non-prolific participants found.")
else:
    # Convert non_prolific_user_ids to a flat list
    non_prolific_user_ids = [user_id[0] for user_id in non_prolific_user_ids]

    # Step 2: Fetch all debate IDs associated with non-prolific users
    cursor.execute("""
        SELECT debate.id 
        FROM debate
        WHERE debate.user_id IN ({})
    """.format(','.join('?'*len(non_prolific_user_ids))), non_prolific_user_ids)
    debate_ids_to_delete = cursor.fetchall()

    # If no debates found, exit
    if not debate_ids_to_delete:
        print("No debates found for non-prolific participants.")
    else:
        # Convert debate_ids_to_delete to a flat list
        debate_ids_to_delete = [debate_id[0] for debate_id in debate_ids_to_delete]

        # Step 3: Delete from copy_paste_event, debate_log, debate_result, and debate tables
        cursor.execute("DELETE FROM copy_paste_event WHERE debate_id IN ({})".format(','.join('?'*len(debate_ids_to_delete))), debate_ids_to_delete)
        cursor.execute("DELETE FROM debate_log WHERE debate_id IN ({})".format(','.join('?'*len(debate_ids_to_delete))), debate_ids_to_delete)
        cursor.execute("DELETE FROM debate_result WHERE debate_id IN ({})".format(','.join('?'*len(debate_ids_to_delete))), debate_ids_to_delete)
        cursor.execute("DELETE FROM debate WHERE id IN ({})".format(','.join('?'*len(debate_ids_to_delete))), debate_ids_to_delete)

        # Step 4: Delete associated user_info records
        cursor.execute("DELETE FROM user_info WHERE user_id IN ({})".format(','.join('?'*len(non_prolific_user_ids))), non_prolific_user_ids)

        # Step 5: Delete associated user records
        cursor.execute("DELETE FROM user WHERE id IN ({})".format(','.join('?'*len(non_prolific_user_ids))), non_prolific_user_ids)

        # Commit the changes
        conn.commit()

        print(f"Deleted {len(debate_ids_to_delete)} debates, associated records, and user-related data for non-prolific participants.")

# Close the connection
conn.close()


import sqlite3

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS debate_summary_with_type_and_gender AS
    SELECT 
        debate.id AS debate_id,
        debate.user_side,
        debate.ai_side,
        debate.initial_likert_score AS initial_rating,
        debate.final_likert_score AS final_rating,
        CASE
            -- If the user is "For" and the final score is higher or equal, move towards the user's side (make negative)
            WHEN debate.user_side = 'FOR' AND debate.final_likert_score > debate.initial_likert_score THEN
                debate.initial_likert_score - debate.final_likert_score
            -- If the user is "Against" and the final score is lower or equal, move towards the user's side (make negative)
            WHEN debate.user_side = 'AGAINST' AND debate.final_likert_score < debate.initial_likert_score THEN
                debate.final_likert_score - debate.initial_likert_score
            ELSE
                ABS(debate.final_likert_score - debate.initial_likert_score)
        END AS rating_difference,
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
        CASE
            -- If the user is "For" and the final score is higher or equal, move towards the user's side (make negative)
            WHEN debate.user_side = 'FOR' AND debate.final_likert_score > debate.initial_likert_score THEN
                debate.initial_likert_score - debate.final_likert_score
            -- If the user is "Against" and the final score is lower or equal, move towards the user's side (make negative)
            WHEN debate.user_side = 'AGAINST' AND debate.final_likert_score < debate.initial_likert_score THEN
                debate.final_likert_score - debate.initial_likert_score
            ELSE
                ABS(debate.final_likert_score - debate.initial_likert_score)
        END AS rating_difference,
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
    LEFT JOIN topic ON debate.topic_id = topic.id
    WHERE user.participant_status LIKE '%NEEDS_REVIEW%'
""")
# Step 3: Commit the transaction and close the connection
conn.commit()
conn.close()

print("Table 'for_review' created successfully with topic description added.")

import sqlite3

# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Step 2: Add the "rating_difference" column to the debate table, if it doesn't exist already
cursor.execute("""
    ALTER TABLE debate ADD COLUMN rating_difference REAL
""")

# Step 3: Update the "rating_difference" column based on the user side and final Likert score
cursor.execute("""
    UPDATE debate
    SET rating_difference =         CASE
            -- If the user is "For" and the final score is higher or equal, move towards the user's side (make negative)
            WHEN debate.user_side = 'FOR' AND debate.final_likert_score > debate.initial_likert_score THEN
                debate.initial_likert_score - debate.final_likert_score
            -- If the user is "Against" and the final score is lower or equal, move towards the user's side (make negative)
            WHEN debate.user_side = 'AGAINST' AND debate.final_likert_score < debate.initial_likert_score THEN
                debate.final_likert_score - debate.initial_likert_score
            ELSE
                ABS(debate.final_likert_score - debate.initial_likert_score)
    END
    WHERE initial_likert_score IS NOT NULL 
    AND final_likert_score IS NOT NULL
""")

# Step 4: Commit the changes to the database
conn.commit()

# Step 5: Close the connection
conn.close()

print("rating_difference column added and populated successfully.")



# Step 1: Connect to the SQLite database
db_path = 'debate_website_prod_latest.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Step 2: Add the "gender" column to the debate table, if it doesn't exist already
cursor.execute("""
    ALTER TABLE debate ADD COLUMN gender VARCHAR(50)
""")

# Step 3: Update the "gender" column in the debate table by joining with the user_info table
cursor.execute("""
    UPDATE debate
    SET gender = (
        SELECT user_info.gender
        FROM user_info
        WHERE user_info.user_id = debate.user_id
    )
""")

# Step 4: Commit the changes to the database
conn.commit()

# Step 5: Close the connection
conn.close()

print("gender column added and populated successfully.")
