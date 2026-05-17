from database import SessionLocal
import models

def add_grade_12():
    db = SessionLocal()
    try:
        # 1. Check if Grade 12 already exists, if not, create it
        level12 = db.query(models.Level).filter_by(Level_ID=12).first()
        if not level12:
            level12 = models.Level(Level_ID=12, Grade_Level="Grade12")
            db.add(level12)
            db.commit()
            print("Added Grade 12 Level.")

        # 2. Get an existing Adviser to assign to the new section
        adviser = db.query(models.Adviser).first()
        
        # 3. Create a Grade 12 Section (e.g., 12-Rizal in the HUMSS strand)
        section12 = db.query(models.Section).filter_by(Section_Name="12-Rizal").first()
        if not section12:
            new_section = models.Section(
                Section_Name="12-Rizal", 
                ATeacher_ID=adviser.ATeacher_ID, 
                Strand_ID=1, # Reusing the HUMSS strand we made earlier
                Level_ID=12
            )
            db.add(new_section)
            db.commit()
            print("Added Section: 12-Rizal (Grade 12).")
            
        print("✅ Grade 12 successfully added to the database!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_grade_12()