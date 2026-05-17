import sqlite3

conn = sqlite3.connect('bnhs_grades.db')
cursor = conn.cursor()

# 1. Add 2nd Semester Columns to the Grade Record
try:
    cursor.execute("ALTER TABLE GRADE_RECORD ADD COLUMN Quarter_3_Grade NUMERIC(5,2);")
    cursor.execute("ALTER TABLE GRADE_RECORD ADD COLUMN Quarter_4_Grade NUMERIC(5,2);")
    cursor.execute("ALTER TABLE GRADE_RECORD ADD COLUMN SecondSem_Average NUMERIC(5,2);")
except Exception as e: print(f"Note (Grades): {e}")

# 2. Add Academic Term Tracking to Teacher Assignments
try:
    cursor.execute("ALTER TABLE TEACHER_ASSIGNMENT ADD COLUMN School_Year VARCHAR(20) DEFAULT '2024-2025';")
    cursor.execute("ALTER TABLE TEACHER_ASSIGNMENT ADD COLUMN Semester VARCHAR(10) DEFAULT '1st';")
except Exception as e: print(f"Note (Assignments): {e}")

# 3. Create the Master System Settings Table
try:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS SYSTEM_SETTING (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Current_School_Year VARCHAR(20),
        Current_Semester VARCHAR(10)
    );
    """)
    # Insert the default starting term if it's empty
    cursor.execute("INSERT INTO SYSTEM_SETTING (Current_School_Year, Current_Semester) SELECT '2024-2025', '1st' WHERE NOT EXISTS (SELECT 1 FROM SYSTEM_SETTING);")
except Exception as e: print(f"Note (Settings): {e}")

conn.commit()
conn.close()
print("✅ Database successfully upgraded for Semesters and System Term!")