import sqlite3

conn = sqlite3.connect('bnhs_grades.db')
cursor = conn.cursor()

try:
    # Safely inject the new column. Existing subjects will default to 'Core'
    cursor.execute("ALTER TABLE SUBJECT ADD COLUMN Subject_Type VARCHAR(20) DEFAULT 'Core';")
    print("✅ Successfully upgraded SUBJECT table with Subject_Type!")
except Exception as e:
    print(f"Note: {e}")

conn.commit()
conn.close()