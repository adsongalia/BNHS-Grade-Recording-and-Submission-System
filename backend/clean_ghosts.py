from database import SessionLocal
import models

db = SessionLocal()

print("Scanning for orphaned subjects...")

# 1. Get a list of all subjects that ACTUALLY exist right now
valid_subjects = [sub.Subject_Code for sub in db.query(models.Subject).all()]

# 2. Find all teacher assignments
all_assignments = db.query(models.TeacherAssignment).all()

# 3. Hunt down and delete the ghosts
deleted_count = 0
for assignment in all_assignments:
    if assignment.Subject_Code not in valid_subjects:
        db.delete(assignment)
        deleted_count += 1

db.commit()
print(f"✅ Successfully exorcised {deleted_count} ghost assignments from the database!")