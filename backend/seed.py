from database import SessionLocal, engine
import models

def seed_database():
    # 0. Drop existing tables to start completely fresh, then rebuild them
    print("Resetting database...")
    models.Base.metadata.drop_all(bind=engine) 
    print("Building database tables...")
    models.Base.metadata.create_all(bind=engine) 

    db = SessionLocal()

    try:
        # 1. Add Levels, Tracks, Strands
        print("Adding Curriculum Data...")
        level11 = models.Level(Level_ID=11, Grade_Level="Grade11")
        track_acad = models.Track(Track_ID=1, Track_Name="Academic")
        strand_humss = models.Strand(Strand_ID=1, Strand_Name="HUMSS", Track_ID=1)
        
        db.add_all([level11, track_acad, strand_humss])
        db.commit()

        # 2. Add Principal
        print("Adding Principal...")
        principal = models.Principal(
            Lastname="Belgica", Firstname="Ramon", Middlename="B.",
            Person_Type="Principal", 
            Employee_ID="PRIN-001", 
            Employee_Type="Principal"
        )
        db.add(principal)
        db.commit()

        # 3. Add Teacher
        print("Adding Teacher...")
        teacher = models.Teacher(
            Lastname="Songalia", Firstname="Celsa", Middlename="D.",
            Person_Type="Teacher", 
            Employee_ID="TCH-001",
            Employee_Type="Teacher", 
            Teacher_ID="TCH-001", 
            Teacher_Type="Adviser"
        )
        db.add(teacher)
        db.commit()

        # 3.5 Add Teacher to Adviser Table
        adviser = models.Adviser(ATeacher_ID=teacher.Teacher_ID)
        db.add(adviser)
        db.commit()

        # 4. Add Subject & Section
        print("Adding Subjects and Sections...")
        subject = models.Subject(
            Subject_Code="EAPP", 
            Subject_Name="English for Academic and Professional Purposes", 
            Subject_Type="Core", 
            Level_ID=11
        )
        section = models.Section(
            Section_ID=1, 
            Section_Name="11-Makabayan", 
            ATeacher_ID=adviser.ATeacher_ID, 
            Strand_ID=1, 
            Level_ID=11
        )
        db.add_all([subject, section])
        db.commit()

        # 5. Assign Teacher to Subject/Section
        print("Creating Teacher Assignment...")
        assignment = models.TeacherAssignment(
            Teacher_ID=teacher.Teacher_ID, 
            Subject_Code="EAPP", 
            Section_ID=1, 
            Semester=1, 
            School_Year="2024-2025"
        )
        db.add(assignment)
        db.commit()

        # 6. Add Students
        print("Enrolling Students...")
        student1 = models.Student(
            Lastname="Dela Cruz", Firstname="Juan", Middlename="M.",
            Person_Type="Student", 
            LRN=111809130001, 
            Section_ID=1
        )
        student2 = models.Student(
            Lastname="Santos", Firstname="Maria", Middlename="C.",
            Person_Type="Student", 
            LRN=111809130002, 
            Section_ID=1
        )
        db.add_all([student1, student2])
        db.commit()

        print("\n✅ Database seeded successfully with BNHS-SHS dummy data!")

    except Exception as e:
        print(f"\n❌ An error occurred during seeding: {e}")
        db.rollback() 
    
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()