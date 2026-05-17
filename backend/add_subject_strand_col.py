import sqlite3

conn = sqlite3.connect('bnhs_grades.db')
cursor = conn.cursor()

try:
    # Safely inject the new column into the existing SUBJECT table
    cursor.execute("ALTER TABLE SUBJECT ADD COLUMN Strand_ID INTEGER;")
    print("✅ Successfully upgraded SUBJECT table with Strand_ID!")
except Exception as e:
    print(f"Note: {e} (The column might already exist).")

conn.commit()
conn.close()