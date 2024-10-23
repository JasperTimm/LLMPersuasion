import sqlite3
from datetime import datetime

# Connect to the SQLite database
db_path = 'debate_website_prod_latest1.sqlite'  # Update with your actual database path
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