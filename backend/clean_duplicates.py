from database import SessionLocal
import models

def clean():
    db = SessionLocal()
    print("🧹 Sweeping database for duplicate students...")
    
    all_students = db.query(models.Student).all()
    seen = set()
    dupe_count = 0
    
    for student in all_students:
        # Safely grab the names regardless of capitalization
        fname = getattr(student, 'Firstname', getattr(student, 'firstname', getattr(student, 'first_name', '')))
        lname = getattr(student, 'Lastname', getattr(student, 'lastname', getattr(student, 'last_name', '')))
        
        full_name = f"{fname} {lname}".strip()
        
        if full_name in seen:
            db.delete(student)
            dupe_count += 1
        else:
            seen.add(full_name)
            
    db.commit()
    db.close()
    print(f"✨ Success! Deleted {dupe_count} duplicate students.")

if __name__ == "__main__":
    clean()