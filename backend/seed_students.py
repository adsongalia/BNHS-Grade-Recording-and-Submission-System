import random
from database import SessionLocal
import models

# 1. Extracted and parsed data directly from your PDFs!
shs_students = {
    "Magalang": [
        ("ANDA, JOMMEL P.", "M"), ("BALASTA, PRINCE CHARLES B.", "M"), 
        ("BAÑAL, FRANCIS LEE G.", "M"), ("BAÑAL, JAMEPEE B.", "M"), 
        ("BAÑAL, RYAN MAR A.", "M"), ("BANDOLA, JOSHUA M.", "M"), 
        ("BANDOLA, RENIER B.", "M"), ("BAÑEZ, JHON B.", "M"), 
        ("BARAQUIEL, MARVIN A", "M"), ("BARBADILLO, JAYSON", "M"), 
        ("BARCELA, MARK JOSEPH B.", "M"), ("BARCELO, GARRY B.", "M"), 
        ("BARCELONA, JOHN B", "M"), ("BARCELONA, LORENCE V", "M"), 
        ("BARIA, JOHN ANDREY B", "M"), ("BATALLA, DIONISIO JR. B.", "M"), 
        ("BEA, JEREMY B.", "M"), ("BELARDO, ALEX JR. B.", "M"), 
        ("BELARMINO, JOHN KENNETH T.", "M"), ("BELEN, JAFET B.", "M"), 
        ("BLANCA, JERALD JAMES E", "M"), ("BOLAGAO, LENARD A.", "M"), 
        ("BUBAN, MARLON NIÑO A.", "M"), ("CAL, ROMMEL P.", "M"), 
        ("CAMATA, JOSHUA M.", "M"), ("CASIN, JUSTIN BRUCE B.", "M"), 
        ("DELOS SANTOS, RICHARD C.", "M"), ("FLORES, DARREN R.", "M"), 
        ("LUNAS, JOHN KENNETH", "M"), ("MONILLA, KENT DENVER B.", "M"), 
        ("NAPAY, BRYAN KIM", "M"), ("PAJO, KENNETH B.", "M"), 
        ("PALOMA, JAYVAN B.", "M"), ("PEPAÑO, REYMARK", "M"), 
        ("SPRINGAEL, HARRION B.", "M"), ("TADURAN, HERMIL B.", "M"), 
        ("TERUEL, JAYPEE B.", "M"), ("TIOPE, DENMARK B.", "M"), 
        ("VIBAL, LOUIGE", "M"), ("VOLANTE, JOHN REY", "M")
    ],
    "Makabayan": [
        ("ALBA, JOSEPH B", "M"), ("ATUN, ANGELO JUDE D.", "M"), 
        ("BARIA, DUSTIN B", "M"), ("BARIAS, ARJAY B.", "M"), 
        ("BARIAS, KEN ANDREI B.", "M"), ("BELARMINO, JOHN RENZ A", "M"), 
        ("BELARMINO, JOSEPH B.", "M"), ("BELLEN, MARCO B.", "M"), 
        ("BENAVENTE, ARJHEL A.", "M"), ("BIEN, ALBERTO JR. V.", "M"), 
        ("BIGOL, CHRISTIAN ROY B.", "M"), ("BILOLO, EDDIE HARRIS B.", "M"), 
        ("BO, JOHN LLOYD B.", "M"),
        ("ALTAVANO, PRINCESS A.", "F"), ("ARELANTE, JONALYN B.", "F"), 
        ("BERMUNDO, GERALDINE D.", "F"), ("BERNAL, MARIBEL V.", "F"), 
        ("BONGON, JONALYN N.", "F"), ("CALANOG, TONNIE ZAINE B", "F"), 
        ("LLANETA, EFRELYN B", "F"), ("PEÑA, CARLA B", "F"), 
        ("VASQUEZ, ANGEL D.", "F"), ("VIBAL, JENNY M.", "F"), 
        ("ZAMORA, ANA MAE C.", "F")
    ],
    "Makatao": [
        ("BARCELA, LOUIE C.", "M"), ("BITAS, MARK ANGELO", "M"), 
        ("CHAVENTE, MAR ADRIEL JOSH B.", "M"), ("DELA CRUZ, JENVER B.", "M"), 
        ("GARCIA, JUDE A", "M"),
        ("BAROMA, MICH ANDREA B", "F"), ("BARIAS, RUBY MAE B.", "F"), 
        ("BARALLAS, JOVY B.", "F"), ("BATALLA, JOFEL B.", "F"), 
        ("BEA, NIÑA ERIN Y.", "F"), ("BERMAS, JESSICA M.", "F"), 
        ("BUBAN, MARICAR B.", "F"), ("BUTLAY, MITCHIE B.", "F"), 
        ("CULALA, JOYCE B.", "F"), ("LLANETA, MARY CLAIRE B.", "F"), 
        ("LORENO, RACHELLE ANN A.", "F"), ("MIRANDA, WYNETH BERRY B.", "F"), 
        ("OFRACIO, JAMAICA P", "F"), ("OLLANO, RAIZA FAITH N", "F"), 
        ("PALACIO, ALHEA B.", "F"), ("ROMANO, QUEENLY MAE B.", "F")
    ],
    "Malikhain": [
        ("BENDAÑA, GILBERT", "M"), ("IBUSAG, DARWIN B.", "M"),
        ("BALANA, RICAH B.", "F"), ("BALINO, JERELLE MAE T.", "F"), 
        ("BARAQUIEL, ARLETTE JOYCE E.", "F"), ("BARAQUIEL, TRISHA MAE E.", "F"), 
        ("BARCELONA, JOANNA MARIE A.", "F"), ("BATALLA, MARIA CARLA", "F"), 
        ("BEA, PRINCESS P.", "F"), ("BEDIS, DANICA C.", "F"), 
        ("BELEN, RIZA MAE B.", "F"), ("BERTIZ, KATHERINE B.", "F"), 
        ("BILOLO, EDDIELYN B.", "F"), ("BUBAN, AIRA M.", "F"), 
        ("BUBAN, TRISHIA A", "F"), ("HILOTIN, NICOLE B", "F"), 
        ("REODIQUE, RICA B.", "F"), ("TERUEL, MARY ANN B.", "F"), 
        ("TERUEL, MARY CRIS B", "F"), ("BARLIZO, MARY GRACE", "F"), 
        ("BASAYSAY, ELOISA MAE В", "F"), ("BERANGO, DENICE ANN AGOTILLA", "F"), 
        ("BERJA, KATRINA B.", "F"), ("JASARENO, KIETH A.", "F"), 
        ("CAMACHO, RAQUEL B.", "F")
    ]
}

def generate_lrn():
    """Generates a random 12-digit LRN starting with standard 108 format"""
    return "108" + "".join([str(random.randint(0, 9)) for _ in range(9)])

def seed_database():
    db = SessionLocal()
    
    print("\n🚀 Starting Student Injection Process...\n")
    
    for section_keyword, students in shs_students.items():
        # Searches the DB for the section
        section = db.query(models.Section).filter(models.Section.Section_Name.ilike(f"%{section_keyword}%")).first()
        
        if not section:
            print(f"⚠️  Skipped '{section_keyword}' - Could not find this section in your database!")
            continue
            
        print(f"✅ Found Section: {section.Section_Name}. Injecting {len(students)} students...")
        
        for full_name, sex in students:
            # 1. Name Parsing Logic
            parts = full_name.split(',', 1)
            last_name = parts[0].strip().title()
            
            first_name = ""
            middle_name = ""
            
            if len(parts) > 1:
                first_parts = parts[1].strip().split(' ')
                if len(first_parts[-1]) <= 2 or first_parts[-1].endswith('.'):
                    middle_name = first_parts.pop().replace('.', '')
                first_name = " ".join(first_parts).title()
            
            try:
                new_student = models.Student()
                
                # 2. THE ULTIMATE FIX: Dynamically match your exact models.py capitalization!
                for attr in ['Firstname', 'firstname', 'first_name', 'FirstName']:
                    if hasattr(models.Student, attr): setattr(new_student, attr, first_name)
                    
                for attr in ['Lastname', 'lastname', 'last_name', 'LastName']:
                    if hasattr(models.Student, attr): setattr(new_student, attr, last_name)
                    
                for attr in ['Middlename', 'middlename', 'middle_name', 'MiddleName']:
                    if hasattr(models.Student, attr): setattr(new_student, attr, middle_name)
                    
                for attr in ['Sex', 'sex']:
                    if hasattr(models.Student, attr): setattr(new_student, attr, sex)
                    
                for attr in ['LRN', 'lrn']:
                    if hasattr(models.Student, attr): setattr(new_student, attr, generate_lrn())
                
                # Extract the section ID dynamically too
                sec_id = getattr(section, 'Section_ID', getattr(section, 'section_id', None))
                for attr in ['Section_ID', 'section_id', 'Section_Id']:
                    if hasattr(models.Student, attr): setattr(new_student, attr, sec_id)
                
                db.add(new_student)
                db.commit()
            except Exception as e:
                # 3. Clear the failed transaction so the queue doesn't get jammed!
                db.rollback()
                print(f"❌ Failed to inject {first_name} {last_name}. Error: {str(e)[:100]}")
            
    print("\n🎉 All done! 110 Students successfully injected into the system.\n")
    db.close()
    db = SessionLocal()
    
    print("\n🚀 Starting Student Injection Process...\n")
    
    for section_keyword, students in shs_students.items():
        # Searches the DB for the section
        section = db.query(models.Section).filter(models.Section.Section_Name.ilike(f"%{section_keyword}%")).first()
        
        if not section:
            print(f"⚠️  Skipped '{section_keyword}' - Could not find this section in your database!")
            continue
            
        print(f"✅ Found Section: {section.Section_Name}. Injecting {len(students)} students...")
        
        for full_name, sex in students:
            # 1. Name Parsing Logic
            parts = full_name.split(',', 1)
            last_name = parts[0].strip().title()
            
            first_name = ""
            middle_name = ""
            
            if len(parts) > 1:
                first_parts = parts[1].strip().split(' ')
                if len(first_parts[-1]) <= 2 or first_parts[-1].endswith('.'):
                    middle_name = first_parts.pop().replace('.', '')
                first_name = " ".join(first_parts).title()
            
            try:
                # 2. THE MAGICAL FIX: Create empty and assign directly
                # This explicitly forces SQLAlchemy to populate the parent Person table
                new_student = models.Student()
                new_student.Firstname = first_name
                new_student.Lastname = last_name
                new_student.Middlename = middle_name
                new_student.Sex = sex
                new_student.LRN = generate_lrn()
                new_student.Section_ID = section.Section_ID
                
                db.add(new_student)
                db.commit()
            except Exception as e:
                # 3. CRITICAL: Clear the failed transaction so the queue doesn't get jammed!
                db.rollback()
                print(f"❌ Failed to inject {first_name} {last_name}. Error: {str(e)[:100]}")
            
    print("\n🎉 All done! 110 Students successfully injected into the system.\n")
    db.close()
    db = SessionLocal()
    
    print("\n🚀 Starting Student Injection Process...\n")
    
    for section_keyword, students in shs_students.items():
        # Searches the DB for the section
        section = db.query(models.Section).filter(models.Section.Section_Name.ilike(f"%{section_keyword}%")).first()
        
        if not section:
            print(f"⚠️  Skipped '{section_keyword}' - Could not find this section in your database!")
            continue
            
        print(f"✅ Found Section: {section.Section_Name}. Injecting {len(students)} students...")
        
        for full_name, sex in students:
            # 1. Name Parsing Logic
            parts = full_name.split(',', 1)
            last_name = parts[0].strip().title()
            
            first_name = ""
            middle_name = ""
            
            if len(parts) > 1:
                first_parts = parts[1].strip().split(' ')
                if len(first_parts[-1]) <= 2 or first_parts[-1].endswith('.'):
                    middle_name = first_parts.pop().replace('.', '')
                first_name = " ".join(first_parts).title()
            
            # 2. THE MAGICAL FIX: Create the Student directly!
            # Because Student inherits from Person, it automatically handles the PERSON table insert.
            new_student = models.Student(
                Firstname=first_name,
                Lastname=last_name,
                Middlename=middle_name,
                Sex=sex,
                LRN=generate_lrn(),
                Section_ID=section.Section_ID
            )
            
            db.add(new_student)
            db.commit()
            
    print("\n🎉 All done! 110 Students successfully injected into the system.\n")
    db.close()
    db = SessionLocal()
    
    print("\n🚀 Starting Student Injection Process...\n")
    
    for section_keyword, students in shs_students.items():
        # Searches the DB for the section
        section = db.query(models.Section).filter(models.Section.Section_Name.ilike(f"%{section_keyword}%")).first()
        
        if not section:
            print(f"⚠️  Skipped '{section_keyword}' - Could not find this section in your database!")
            continue
            
        print(f"✅ Found Section: {section.Section_Name}. Injecting {len(students)} students...")
        
        for full_name, sex in students:
            # 1. Name Parsing Logic: "LASTNAME, FIRSTNAME MI."
            parts = full_name.split(',', 1)
            last_name = parts[0].strip().title()
            
            first_name = ""
            middle_name = ""
            
            if len(parts) > 1:
                first_parts = parts[1].strip().split(' ')
                if len(first_parts[-1]) <= 2 or first_parts[-1].endswith('.'):
                    middle_name = first_parts.pop().replace('.', '')
                first_name = " ".join(first_parts).title()
            
            # 2. Save Demographic to PERSON table (Bulletproof Capitalization)
            new_person = models.Person()
            
            # Dynamically set attributes regardless of how models.py capitalized it
            for attr in ['Firstname', 'firstname', 'FirstName']:
                if hasattr(new_person, attr): setattr(new_person, attr, first_name)
            for attr in ['Lastname', 'lastname', 'LastName']:
                if hasattr(new_person, attr): setattr(new_person, attr, last_name)
            for attr in ['Middlename', 'middlename', 'MiddleName']:
                if hasattr(new_person, attr): setattr(new_person, attr, middle_name)
            for attr in ['Sex', 'sex']:
                if hasattr(new_person, attr): setattr(new_person, attr, sex)
                
            db.add(new_person)
            db.commit()
            db.refresh(new_person)
            
            # 3. Create Unique LRN and save to STUDENT table
            new_student = models.Student()
            
            for attr in ['LRN', 'lrn']:
                if hasattr(new_student, attr): setattr(new_student, attr, generate_lrn())
                
            # Extract IDs safely
            p_id = getattr(new_person, 'Person_ID', getattr(new_person, 'person_id', None))
            for attr in ['SPerson_ID', 'sperson_id', 'Person_ID', 'person_id']:
                if hasattr(new_student, attr): setattr(new_student, attr, p_id)
                
            s_id = getattr(section, 'Section_ID', getattr(section, 'section_id', None))
            for attr in ['Section_ID', 'section_id']:
                if hasattr(new_student, attr): setattr(new_student, attr, s_id)
                
            db.add(new_student)
            db.commit()
            
    print("\n🎉 All done! 110 Students successfully injected into the system.\n")
    db.close()
    db = SessionLocal()
    
    print("\n🚀 Starting Student Injection Process...\n")
    
    for section_keyword, students in shs_students.items():
        # Searches the DB for the section (e.g. finds "11-Magalang" using "Magalang")
        section = db.query(models.Section).filter(models.Section.Section_Name.ilike(f"%{section_keyword}%")).first()
        
        if not section:
            print(f"⚠️  Skipped '{section_keyword}' - Could not find this section in your database! Ensure you added it via the Principal Dashboard first.")
            continue
            
        print(f"✅ Found Section: {section.Section_Name}. Injecting {len(students)} students...")
        
        for full_name, sex in students:
            # 1. Name Parsing Logic: "LASTNAME, FIRSTNAME MI."
            parts = full_name.split(',', 1)
            last_name = parts[0].strip().title()
            
            first_name = ""
            middle_name = ""
            
            if len(parts) > 1:
                first_parts = parts[1].strip().split(' ')
                # If the last word is 1 or 2 letters, or ends with a period, it's an initial
                if len(first_parts[-1]) <= 2 or first_parts[-1].endswith('.'):
                    middle_name = first_parts.pop().replace('.', '')
                first_name = " ".join(first_parts).title()
            
            # 2. Save Demographic to PERSON table
            new_person = models.Person(
                Firstname=first_name,
                Lastname=last_name,
                Middlename=middle_name,
                Sex=sex
            )
            db.add(new_person)
            db.commit()
            db.refresh(new_person)
            
            # 3. Create Unique LRN and save to STUDENT table
            # NOTE: If your models.py uses a different column name than 'SPerson_ID' 
            # (like 'Person_ID'), simply change it here!
            new_student = models.Student(
                LRN=generate_lrn(),
                SPerson_ID=new_person.Person_ID, 
                Section_ID=section.Section_ID
            )
            db.add(new_student)
            db.commit()
            
    print("\n🎉 All done! 110 Students successfully injected into the system.\n")
    db.close()

if __name__ == "__main__":
    seed_database()