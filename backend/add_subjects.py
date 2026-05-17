from database import SessionLocal
import models

def add_more_subjects():
    db = SessionLocal()
    try:
        new_subjects = [
            models.Subject(Subject_Code="GENMATH", Subject_Name="General Mathematics", Subject_Type="Core", Level_ID=11),
            models.Subject(Subject_Code="UCSP", Subject_Name="Understanding Culture, Society, and Politics", Subject_Type="Core", Level_ID=11),
            models.Subject(Subject_Code="PR1", Subject_Name="Practical Research 1", Subject_Type="Applied", Level_ID=11),
            models.Subject(Subject_Code="MIL", Subject_Name="Media and Information Literacy", Subject_Type="Core", Level_ID=12)
        ]
        
        for sub in new_subjects:
            # Check if it exists before adding
            exists = db.query(models.Subject).filter_by(Subject_Code=sub.Subject_Code).first()
            if not exists:
                db.add(sub)
                
        db.commit()
        print("✅ Official SHS Subjects successfully added to the Curriculum!")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_more_subjects()