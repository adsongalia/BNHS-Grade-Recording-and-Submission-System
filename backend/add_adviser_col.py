import sqlite3

conn = sqlite3.connect('bnhs_grades.db')
cursor = conn.cursor()

try:
    # Safely inject the new column into the existing SECTION table
    cursor.execute("ALTER TABLE SECTION ADD COLUMN Adviser_ID VARCHAR(50);")
    print("✅ Successfully upgraded SECTION table with Adviser_ID!")
except Exception as e:
    print(f"Note: {e} (The column might already exist).")

conn.commit()
conn.close()