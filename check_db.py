import sqlite3
import os

db_path = 'D:/harxitflow/src/backend/base/harxitflow/harxitflow.db'
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = c.fetchall()
c.execute("PRAGMA integrity_check")
result = c.fetchone()
print(f"Integrity check: {result[0]}")

target_uuid = 'a09ef054-8376-4b40-8d24-6ad6e816ccc9'
c.execute(f"SELECT id, name FROM flow WHERE id='{target_uuid}'")
row = c.fetchone()
if row:
    print(f"Found flow: {row[0]} - {row[1]}")
else:
    print(f"Flow {target_uuid} not found in database.")

# Check for orphaned flows
c.execute("SELECT count(*) FROM flow WHERE folder_id IS NULL")
orphaned_count = c.fetchone()[0]
print(f"Orphaned flows (no folder_id): {orphaned_count}")

# Check for flows with invalid folder_id
c.execute("SELECT count(*) FROM flow WHERE folder_id NOT IN (SELECT id FROM folder) AND folder_id IS NOT NULL")
invalid_folder_count = c.fetchone()[0]
print(f"Flows with invalid folder_id: {invalid_folder_count}")

# Check for orphaned folders (no user_id)
c.execute("SELECT count(*) FROM folder WHERE user_id IS NULL")
orphaned_folders = c.fetchone()[0]
print(f"Orphaned folders (no user_id): {orphaned_folders}")

for t in tables:
    table_name = t[0]
    c.execute(f'SELECT count(*) FROM "{table_name}"')
    count = c.fetchone()[0]
    print(f"{table_name}: {count}")
conn.close()
