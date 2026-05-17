import sqlite3
import os

db_path = 'bnhs_grades.db'
print(f"Targeting database at: {os.path.abspath(db_path)}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # FORCE SQLite to ignore relationships temporarily so we can delete the tables
    cursor.execute("PRAGMA foreign_keys = OFF;")

    print("Sledhammering old Curriculum tables...")
    cursor.execute("DROP TABLE IF EXISTS SECTION;")
    cursor.execute("DROP TABLE IF EXISTS STRAND;")
    cursor.execute("DROP TABLE IF EXISTS TRACK;")

    conn.commit()
    conn.close()
    print("✅ SUCCESS! The old tables are permanently gone.")
    print("You may now restart your server to rebuild them.")

except Exception as e:
    print(f"❌ ERROR: {e}")
    print("Please make sure your Uvicorn server is completely shut down!")