import sqlite3

conn = sqlite3.connect('bnhs_grades.db')
cursor = conn.cursor()

try:
    # 1. Nuke the broken table
    cursor.execute("DROP TABLE IF EXISTS SYSTEM_SETTING;")
    
    # 2. Rebuild it perfectly to match models.py
    cursor.execute("""
    CREATE TABLE SYSTEM_SETTING (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Current_School_Year VARCHAR(20),
        Current_Semester VARCHAR(10)
    );
    """)
    
    # 3. Inject the default term
    cursor.execute("INSERT INTO SYSTEM_SETTING (Current_School_Year, Current_Semester) VALUES ('2024-2025', '1st');")
    
    print("✅ SYSTEM_SETTING table successfully fixed and seeded!")
except Exception as e:
    print(f"Error: {e}")

conn.commit()
conn.close()