from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware # Add this import
from sqlalchemy.orm import Session
from datetime import date
import models, database
from pydantic import BaseModel
from typing import List, Optional
from security import get_current_user, get_password_hash, verify_password
import auth
import traceback
import sys

# --- SYSTEM SETTINGS: ACADEMIC TERM ---
class TermSettings(BaseModel):
    school_year: str
    semester: str

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="BNHS-SHS Grade System")

@app.get("/api/settings/term")
def get_system_term(db: Session = Depends(database.get_db)):
    setting = db.query(models.SystemSetting).first()
    if not setting:
        setting = models.SystemSetting(Current_School_Year="2024-2025", Current_Semester="1st")
        db.add(setting)
        db.commit()
    return {"school_year": setting.Current_School_Year, "semester": setting.Current_Semester}

@app.post("/api/settings/term")
def update_system_term(req: TermSettings, db: Session = Depends(database.get_db)):
    setting = db.query(models.SystemSetting).first()
    if not setting:
        setting = models.SystemSetting()
        db.add(setting)
    setting.Current_School_Year = req.school_year
    setting.Current_Semester = req.semester
    db.commit()
    return {"message": f"System updated to {req.semester} Sem, {req.school_year}!"}

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Allows your Vue app to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Modular Routers
app.include_router(auth.router)

# Organized logic blocks to easily extract to files later
teacher_router = APIRouter(prefix="/api/teacher", tags=["Teacher Module"])
principal_router = APIRouter(prefix="/api/principal", tags=["Principal Dashboard"])
curriculum_router = APIRouter(prefix="/api/curriculum", tags=["Curriculum"])

class GradeEntry(BaseModel):
    lrn: int
    q1: Optional[float] = None
    q2: Optional[float] = None
    q3: Optional[float] = None
    q4: Optional[float] = None

class SubmissionRequest(BaseModel):
    teacher_assignment_id: int
    grades: List[GradeEntry]

@teacher_router.get("/assignments")
def get_assignments(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    teacher = db.query(models.Teacher).filter(models.Teacher.Employee_ID == current_user["employee_id"]).first()
    if not teacher:
        raise HTTPException(status_code=403, detail="Not a teacher")
    
    assignments = db.query(models.TeacherAssignment).filter(models.TeacherAssignment.Teacher_ID == teacher.Teacher_ID).all()
    return assignments

@teacher_router.get("/{teacher_id}/profile")
def get_teacher_profile(teacher_id: str, db: Session = Depends(database.get_db)):
    # FIX: Check the master Employee table first, just like the Principal!
    user = None
    if hasattr(models, 'Employee'):
        user = db.query(models.Employee).filter_by(Employee_ID=teacher_id).first()
    if not user:
        user = db.query(models.Teacher).filter_by(Employee_ID=teacher_id).first()
        
    if user:
        return {"name": f"{getattr(user, 'Firstname', '')} {getattr(user, 'Lastname', '')}"}
    return {"name": "Unknown Teacher"}

@teacher_router.post("/submit-grades")
def submit_grades(req: SubmissionRequest, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    setting = db.query(models.SystemSetting).first()
    is_second_sem = setting and str(setting.Current_Semester) in ['2nd', '2']
    
    # Check if a submission already exists for this assignment
    existing_submission = db.query(models.Submission).filter_by(Teacher_Assignment_ID=req.teacher_assignment_id).first()
    
    assignment = db.query(models.TeacherAssignment).filter_by(Teacher_Assignment_ID=req.teacher_assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    if existing_submission:
        existing_submission.Date_Submitted = date.today()
        
        for grade in req.grades:
            record = db.query(models.GradeRecord).filter_by(Submission_ID=existing_submission.Submission_ID, LRN=grade.lrn).first()
            if record:
                if is_second_sem:
                    record.Quarter_3_Grade = grade.q1
                    record.Quarter_4_Grade = grade.q2
                    record.SecondSem_Average = (grade.q1 + grade.q2) / 2 if grade.q1 and grade.q2 else None
                else:
                    record.Quarter_1_Grade = grade.q1
                    record.Quarter_2_Grade = grade.q2
                    record.FirstSem_Average = (grade.q1 + grade.q2) / 2 if grade.q1 and grade.q2 else None
                
                # Clear previous approval status so principal can review new semester grades
                record.Date_Approved = None
                record.PEmployee_ID = None
            else:
                actual_q1 = None if is_second_sem else grade.q1
                actual_q2 = None if is_second_sem else grade.q2
                actual_q3 = grade.q1 if is_second_sem else None
                actual_q4 = grade.q2 if is_second_sem else None
                first_sem_avg = (actual_q1 + actual_q2) / 2 if actual_q1 and actual_q2 else None
                second_sem_avg = (actual_q3 + actual_q4) / 2 if actual_q3 and actual_q4 else None
                
                new_record = models.GradeRecord(
                    LRN=grade.lrn,
                    Submission_ID=existing_submission.Submission_ID,
                    Subject_Code=assignment.Subject_Code,
                    Quarter_1_Grade=actual_q1,
                    Quarter_2_Grade=actual_q2,
                    FirstSem_Average=first_sem_avg,
                    Quarter_3_Grade=actual_q3,
                    Quarter_4_Grade=actual_q4,
                    SecondSem_Average=second_sem_avg
                )
                db.add(new_record)
        
        db.commit()
        return {"message": "Grades updated and resubmitted successfully", "submission_id": existing_submission.Submission_ID}

    # 1. Create a new Submission batch
    new_submission = models.Submission(
        Date_Submitted=date.today(),
        Teacher_Assignment_ID=req.teacher_assignment_id
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    assignment = db.query(models.TeacherAssignment).filter_by(Teacher_Assignment_ID=req.teacher_assignment_id).first()

    # 2. Record Grades
    for grade in req.grades:
        actual_q1 = None if is_second_sem else grade.q1
        actual_q2 = None if is_second_sem else grade.q2
        actual_q3 = grade.q1 if is_second_sem else grade.q3
        actual_q4 = grade.q2 if is_second_sem else grade.q4
        
        first_sem_avg = (actual_q1 + actual_q2) / 2 if actual_q1 and actual_q2 else None
        second_sem_avg = (actual_q3 + actual_q4) / 2 if actual_q3 and actual_q4 else None

        new_record = models.GradeRecord(
            LRN=grade.lrn,
            Submission_ID=new_submission.Submission_ID,
            Subject_Code=assignment.Subject_Code,
            Quarter_1_Grade=actual_q1,
            Quarter_2_Grade=actual_q2,
            FirstSem_Average=first_sem_avg,
            Quarter_3_Grade=actual_q3,
            Quarter_4_Grade=actual_q4,
            SecondSem_Average=second_sem_avg
        )
        db.add(new_record)
    
    db.commit()
    return {"message": "Grades submitted successfully", "submission_id": new_submission.Submission_ID}

from sqlalchemy import String

from sqlalchemy import String
from datetime import date

# --- UPDATED SCHEMAS FOR STUDENT CRUD ---
class StudentCreate(BaseModel):
    lrn: int
    lastname: str
    firstname: str
    middlename: Optional[str] = None
    birth_date: Optional[date] = None
    sex: Optional[str] = None
    section_id: int

class StudentUpdate(BaseModel):
    lastname: Optional[str] = None
    firstname: Optional[str] = None
    middlename: Optional[str] = None
    birth_date: Optional[date] = None
    sex: Optional[str] = None
    section_id: Optional[int] = None

# --- UPDATED ENDPOINTS FOR STUDENT CRUD ---

@teacher_router.get("/students")
def get_students(search: Optional[str] = None, db: Session = Depends(database.get_db)):
    # Join Student with Section and Level to get the descriptive names
    query = db.query(
        models.Student, 
        models.Section.Section_Name, 
        models.Level.Grade_Level
    ).outerjoin(models.Section, models.Student.Section_ID == models.Section.Section_ID)\
     .outerjoin(models.Level, models.Section.Level_ID == models.Level.Level_ID)
    
    if search:
        search_term = f"%{search}%"
        if search.isdigit():
             # If searching numbers, strictly search the LRN
             query = query.filter(models.Student.LRN == int(search))
        else:
             # If searching text, search Lastname or Firstname
             query = query.filter(
                 models.Student.Lastname.ilike(search_term) | 
                 models.Student.Firstname.ilike(search_term)
             )
             
    results = query.all()
    
    # Format the combined data into a clean dictionary for Vue
    students_data = []
    for student, section_name, grade_level in results:
        students_data.append({
            "LRN": student.LRN,
            "Lastname": student.Lastname,
            "Firstname": student.Firstname,
            "Middlename": student.Middlename,
            "Birth_Date": student.Birth_Date.isoformat() if student.Birth_Date else None,
            "Sex": student.Sex,
            "Section_ID": student.Section_ID,
            "Section_Name": section_name or "Unassigned",
            "Grade_Level": grade_level or "N/A"
        })
        
    return students_data

@teacher_router.post("/students")
def create_student(student: StudentCreate, db: Session = Depends(database.get_db)):
    db_student = models.Student(
        LRN=student.lrn,
        Lastname=student.lastname,
        Firstname=student.firstname,
        Middlename=student.middlename,
        Birth_Date=student.birth_date,
        Sex=student.sex,
        Section_ID=student.section_id,
        Person_Type="Student"
    )
    db.add(db_student)
    try:
        db.commit()
        db.refresh(db_student)
        return {"message": "Student created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Student LRN already exists or invalid data.")

@teacher_router.put("/students/{lrn}")
def update_student(lrn: int, student_data: StudentUpdate, db: Session = Depends(database.get_db)):
    db_student = db.query(models.Student).filter(models.Student.LRN == lrn).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if student_data.lastname is not None: db_student.Lastname = student_data.lastname
    if student_data.firstname is not None: db_student.Firstname = student_data.firstname
    if student_data.middlename is not None: db_student.Middlename = student_data.middlename
    if student_data.birth_date is not None: db_student.Birth_Date = student_data.birth_date
    if student_data.sex is not None: db_student.Sex = student_data.sex
    if student_data.section_id is not None: db_student.Section_ID = student_data.section_id
    
    db.commit()
    return {"message": "Student updated successfully"}

@teacher_router.delete("/students/{lrn}")
def delete_student(lrn: int, db: Session = Depends(database.get_db)):
    db_student = db.query(models.Student).filter(models.Student.LRN == lrn).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}


# Business Rules Validators (To be called during data insertion/admin panels)
def validate_section_size(db: Session, section_id: int):
    count = db.query(models.Student).filter(models.Student.Section_ID == section_id).count()
    if count < 10 or count > 40:
        raise ValueError("A section must have between 10 and 40 students.") # [cite: 430]

def validate_teacher_load(db: Session, teacher_id: str):
    count = db.query(models.TeacherAssignment).filter(models.TeacherAssignment.Teacher_ID == teacher_id).count()
    if count < 2 or count > 6:
        raise ValueError("A teacher must have between 2 and 6 teaching loads.") # [cite: 431]
    
    unique_subjects = db.query(models.TeacherAssignment.Subject_Code).filter(models.TeacherAssignment.Teacher_ID == teacher_id).distinct().count()
    if unique_subjects < 1 or unique_subjects > 3:
        raise ValueError("A teacher must teach between 1 and 3 subjects.") # [cite: 432]

@teacher_router.get("/sections")
def get_sections(db: Session = Depends(database.get_db)):
    sections = db.query(models.Section).all()
    return [{"Section_ID": sec.Section_ID, "Section_Name": sec.Section_Name} for sec in sections]

# --- PRINCIPAL MANAGEMENT MODULE ---

class ApprovalRequest(BaseModel):
    submission_id: int
    principal_id: str

@principal_router.get("/submissions")
def get_submissions(db: Session = Depends(database.get_db)):
    submissions = db.query(models.Submission).all()
    setting = db.query(models.SystemSetting).first()
    is_second_sem = setting and str(setting.Current_Semester) in ['2nd', '2']
    results = []
    
    for sub in submissions:
        if sub.Date_Submitted == date(1970, 1, 1):
            continue # Skip returned submissions in principal dashboard
            
        assign = db.query(models.TeacherAssignment).filter_by(Teacher_Assignment_ID=sub.Teacher_Assignment_ID).first()
        if not assign: 
            continue # Skip broken orphan records
            
        subj = db.query(models.Subject).filter_by(Subject_Code=assign.Subject_Code).first()
        sec = db.query(models.Section).filter_by(Section_ID=assign.Section_ID).first()
        teacher = db.query(models.Teacher).filter_by(Teacher_ID=assign.Teacher_ID).first()
        
        record = db.query(models.GradeRecord).filter_by(Submission_ID=sub.Submission_ID).first()
        
        if is_second_sem:
            if not (record and record.Quarter_3_Grade is not None): continue
        else:
            if not (record and record.Quarter_1_Grade is not None): continue
            
        status = "Approved" if record and record.Date_Approved else "Pending"
        
        results.append({
            "Submission_ID": sub.Submission_ID,
            "Date_Submitted": sub.Date_Submitted.isoformat() if sub.Date_Submitted else "-",
            # SAFEGUARD: If a teacher/subject was deleted, print "Unknown" instead of crashing the whole server
            "Subject": subj.Subject_Name if subj else "Unknown Subject",
            "Section": sec.Section_Name if sec else "Unknown Section",
            "Teacher": f"{teacher.Lastname}, {teacher.Firstname}" if teacher else "Unknown Teacher",
            "Status": status
        })
    return results

@principal_router.post("/approve")
def approve_submission(req: ApprovalRequest, db: Session = Depends(database.get_db)):
    # 1. Verify Principal
    principal = db.query(models.Principal).filter(models.Principal.Employee_ID == req.principal_id).first()
    if not principal:
        raise HTTPException(status_code=404, detail="Principal not found.")

    # 2. Find all grade records tied to this submission batch and stamp them with approval
    records = db.query(models.GradeRecord).filter(models.GradeRecord.Submission_ID == req.submission_id).all()
    for record in records:
        record.PEmployee_ID = principal.PEmployee_ID
        record.Date_Approved = date.today()
    
    db.commit()
    return {"message": "Batch officially approved!"}

# --- PRINCIPAL: PROFILE MANAGEMENT ---
class PrincipalProfileUpdate(BaseModel):
    firstname: str
    lastname: str
    middlename: Optional[str] = None
    birth_date: Optional[date] = None
    sex: Optional[str] = None
    old_password: Optional[str] = None
    new_password: Optional[str] = None

@principal_router.get("/{emp_id}/profile")
def get_principal_profile(emp_id: str, db: Session = Depends(database.get_db)):
    # We stopped guessing! Python confirmed it is exactly 'Employee_ID'
    employee = db.query(models.Employee).filter(models.Employee.Employee_ID == emp_id).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Principal not found")
        
    # Dynamically grab the fields regardless of capitalization
    fname = getattr(employee, 'Firstname', getattr(employee, 'firstname', ''))
    lname = getattr(employee, 'Lastname', getattr(employee, 'lastname', ''))
    mname = getattr(employee, 'Middlename', getattr(employee, 'middlename', ''))
    bdate = getattr(employee, 'Birth_Date', getattr(employee, 'birth_date', None))
    sex = getattr(employee, 'Sex', getattr(employee, 'sex', 'M'))
    
    return {
        "name": f"{fname} {lname}".strip(),
        "firstname": fname,
        "lastname": lname,
        "middlename": mname,
        "birth_date": bdate,
        "sex": sex
    }

@principal_router.put("/{emp_id}/profile")
def update_principal_profile(emp_id: str, req: PrincipalProfileUpdate, db: Session = Depends(database.get_db)):
    try:
        employee = None
        if hasattr(models, 'Employee'):
            employee = db.query(models.Employee).filter(models.Employee.Employee_ID == emp_id).first()
        if not employee and hasattr(models, 'Principal'):
            employee = db.query(models.Principal).filter(models.Principal.Employee_ID == emp_id).first()
        
        if not employee:
            raise HTTPException(status_code=404, detail="Principal not found in database.")
            
        if req.new_password:
            if not req.old_password:
                raise HTTPException(status_code=400, detail="Old password is required to set a new password.")
                
            pass_col = getattr(employee, 'Password', getattr(employee, 'password', None))
            matched = False
            if pass_col:
                pass_str = str(pass_col).strip()
                old_pass = str(req.old_password).strip()[:72]
                if pass_str == old_pass:
                    matched = True
                else:
                    try:
                        if verify_password(old_pass, pass_str):
                            matched = True
                    except Exception as e:
                        print(f"\n[PRINCIPAL PWD VERIFY ERROR] {e}", file=sys.stderr)
                        traceback.print_exc()
                    
            if not matched:
                raise HTTPException(status_code=400, detail="Incorrect current password. Profile not updated.")
            new_hash = get_password_hash(str(req.new_password).strip()[:72])
            for attr in ['Password', 'password']:
                if hasattr(employee, attr): setattr(employee, attr, new_hash)
                    
        for attr in ['Firstname', 'firstname', 'first_name']:
            if hasattr(employee, attr): setattr(employee, attr, req.firstname)
        for attr in ['Lastname', 'lastname', 'last_name']:
            if hasattr(employee, attr): setattr(employee, attr, req.lastname)
        for attr in ['Middlename', 'middlename']:
            if hasattr(employee, attr): setattr(employee, attr, req.middlename)
        for attr in ['Birth_Date', 'birth_date']:
            if hasattr(employee, attr): setattr(employee, attr, req.birth_date)
        for attr in ['Sex', 'sex']:
            if hasattr(employee, attr): setattr(employee, attr, req.sex)
            
        db.commit()
        return {"message": "Profile updated successfully"}
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        print("\n[PRINCIPAL PROFILE UPDATE CRASH]", file=sys.stderr)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Python Crash: {str(e)}")

class TeacherCreate(BaseModel):
    employee_id: str
    firstname: str
    lastname: str
    middlename: Optional[str] = None
    birth_date: Optional[date] = None
    sex: Optional[str] = "M"
    role: str = "Subject Teacher"
    password: Optional[str] = "password123"

class TeacherUpdate(BaseModel):
    lastname: Optional[str] = None
    firstname: Optional[str] = None
    middlename: Optional[str] = None
    birth_date: Optional[date] = None
    sex: Optional[str] = None
    role: Optional[str] = None

# --- TEACHER DASHBOARD: SUBMISSION STATUS ---
@teacher_router.get("/my-submissions/{teacher_id}")
def get_my_submissions(teacher_id: str, db: Session = Depends(database.get_db)):
    # Find assignments for this teacher
    assignments = db.query(models.TeacherAssignment).filter(models.TeacherAssignment.Teacher_ID == teacher_id).all()
    assignment_ids = [a.Teacher_Assignment_ID for a in assignments]
    
    # Find submissions linked to those assignments
    submissions = db.query(models.Submission).filter(models.Submission.Teacher_Assignment_ID.in_(assignment_ids)).all()
    setting = db.query(models.SystemSetting).first()
    is_second_sem = setting and str(setting.Current_Semester) in ['2nd', '2']
    
    results = []
    for sub in submissions:
        assign = db.query(models.TeacherAssignment).filter_by(Teacher_Assignment_ID=sub.Teacher_Assignment_ID).first()
        subj = db.query(models.Subject).filter_by(Subject_Code=assign.Subject_Code).first()
        sec = db.query(models.Section).filter_by(Section_ID=assign.Section_ID).first()
        
        record = db.query(models.GradeRecord).filter_by(Submission_ID=sub.Submission_ID).first()
        
        if is_second_sem:
            if record and record.Quarter_3_Grade is not None:
                status = "Returned for Correction" if sub.Date_Submitted == date(1970, 1, 1) else ("Approved by Principal" if record.Date_Approved else "Pending Principal Approval")
            else:
                continue
        else:
            if record and record.Quarter_1_Grade is not None:
                status = "Returned for Correction" if sub.Date_Submitted == date(1970, 1, 1) else ("Approved by Principal" if record.Date_Approved else "Pending Principal Approval")
            else:
                continue
                
        date_str = "-" if sub.Date_Submitted == date(1970, 1, 1) else (sub.Date_Submitted.isoformat() if sub.Date_Submitted else "-")
        
        results.append({
            "Submission_ID": sub.Submission_ID,
            "Date_Submitted": date_str,
            "Class": f"{subj.Subject_Name} - {sec.Section_Name}",
            "Assignment_ID": sub.Teacher_Assignment_ID,
            "Status": status
        })
    return results

@teacher_router.delete("/submissions/{submission_id}")
def delete_teacher_submission(submission_id: int, db: Session = Depends(database.get_db)):
    sub = db.query(models.Submission).filter_by(Submission_ID=submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    db.query(models.GradeRecord).filter_by(Submission_ID=submission_id).delete()
    db.delete(sub)
    db.commit()
    return {"message": "Submission deleted successfully."}

# --- PRINCIPAL DASHBOARD: TEACHER CRUD ---
@principal_router.get("/teachers")
def get_all_teachers(db: Session = Depends(database.get_db)):
    return db.query(models.Teacher).all()

@principal_router.post("/teachers")
def create_teacher(t: TeacherCreate, db: Session = Depends(database.get_db)):
    try:
        new_teacher = models.Teacher(
            Employee_ID=t.employee_id,
            Teacher_ID=t.employee_id, # Syncing Employee ID and Teacher ID for simplicity
            Lastname=t.lastname,
            Firstname=t.firstname,
            Middlename=t.middlename,
            Birth_Date=t.birth_date,
            Sex=t.sex,
            Person_Type="Teacher",
            Employee_Type="Teacher",
            Teacher_Type=t.role,
            Password=get_password_hash(str(t.password).strip()[:72] if t.password else "password123")
        )
        db.add(new_teacher)
        db.commit()
        
        # If they are an adviser, add them to the Adviser table
        if t.role == 'Adviser':
            new_adviser = models.Adviser(ATeacher_ID=t.employee_id)
            db.add(new_adviser)
            db.commit()
            
        return {"message": "Teacher successfully added"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error adding teacher. ID might already exist.")

@principal_router.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: str, db: Session = Depends(database.get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.Teacher_ID == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Also remove from Adviser table if applicable
    adviser_record = db.query(models.Adviser).filter(models.Adviser.ATeacher_ID == teacher_id).first()
    if adviser_record:
        db.delete(adviser_record)
        
    db.delete(teacher)
    db.commit()
    return {"message": "Teacher deleted successfully"}

# --- NEW PRINCIPAL FEATURES: VIEW GRADES, REJECT, EDIT TEACHER ---

@principal_router.get("/submissions/{submission_id}/grades")
def get_submission_grades(submission_id: int, db: Session = Depends(database.get_db)):
    # Fetch all grade records tied to this specific batch
    records = db.query(models.GradeRecord).filter(models.GradeRecord.Submission_ID == submission_id).all()
    setting = db.query(models.SystemSetting).first()
    is_second_sem = setting and str(setting.Current_Semester) in ['2nd', '2']
    
    result = []
    for r in records:
        # SAFEGUARD: Look for the student, but don't crash if they were deleted!
        student = db.query(models.Student).filter(models.Student.LRN == r.LRN).first()
        
        if student:
            name = f"{student.Lastname}, {student.Firstname} {student.Middlename or ''}".strip()
        else:
            name = "Deleted Student"

        result.append({
            "LRN": r.LRN,
            "Name": name,
            "Q1": r.Quarter_3_Grade if is_second_sem else r.Quarter_1_Grade,
            "Q2": r.Quarter_4_Grade if is_second_sem else r.Quarter_2_Grade,
            "Final": r.SecondSem_Average if is_second_sem else r.FirstSem_Average
        })
    return result

import io
import csv
from fastapi.responses import StreamingResponse

@principal_router.get("/submissions/{submission_id}/export")
def export_submission_grades(submission_id: int, db: Session = Depends(database.get_db)):
    records = db.query(models.GradeRecord).filter(models.GradeRecord.Submission_ID == submission_id).all()
    setting = db.query(models.SystemSetting).first()
    is_second_sem = setting and str(setting.Current_Semester) in ['2nd', '2']
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["LRN", "Name", "Q1/Q3", "Q2/Q4", "Final Average"])
    
    for r in records:
        student = db.query(models.Student).filter(models.Student.LRN == r.LRN).first()
        name = f"{student.Lastname}, {student.Firstname} {student.Middlename or ''}".strip() if student else "Deleted Student"
        final = r.SecondSem_Average if is_second_sem else r.FirstSem_Average
        q1 = r.Quarter_3_Grade if is_second_sem else r.Quarter_1_Grade
        q2 = r.Quarter_4_Grade if is_second_sem else r.Quarter_2_Grade
        writer.writerow([r.LRN, name, q1, q2, final if final is not None else "-"])
        
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename=Batch_{submission_id}_Grades.csv"})

@principal_router.post("/reject")
def reject_submission(req: ApprovalRequest, db: Session = Depends(database.get_db)):
    # To reject, we mark it as returned by setting Date_Submitted to a special past date.
    # This unlocks the grade sheet for the teacher so they can fix and resubmit.
    submission = db.query(models.Submission).filter(models.Submission.Submission_ID == req.submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found.")
    
    submission.Date_Submitted = date(1970, 1, 1)
    
    db.commit()
    return {"message": "Batch rejected and returned to teacher."}

@principal_router.delete("/submissions/{submission_id}")
def delete_principal_submission(submission_id: int, db: Session = Depends(database.get_db)):
    sub = db.query(models.Submission).filter_by(Submission_ID=submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    db.query(models.GradeRecord).filter_by(Submission_ID=submission_id).delete()
    db.delete(sub)
    db.commit()
    return {"message": "Submission deleted successfully."}

@principal_router.put("/teachers/{teacher_id}")
def update_teacher(teacher_id: str, t: TeacherUpdate, db: Session = Depends(database.get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.Teacher_ID == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    if t.lastname is not None: teacher.Lastname = t.lastname
    if t.firstname is not None: teacher.Firstname = t.firstname
    if t.middlename is not None: teacher.Middlename = t.middlename
    if t.birth_date is not None: teacher.Birth_Date = t.birth_date
    if t.sex is not None: teacher.Sex = t.sex
    
    # Handle Role Change (Adding/Removing from Adviser table)
    if t.role and t.role != teacher.Teacher_Type:
        teacher.Teacher_Type = t.role
        adviser_record = db.query(models.Adviser).filter(models.Adviser.ATeacher_ID == teacher_id).first()
        
        if t.role == "Adviser" and not adviser_record:
            db.add(models.Adviser(ATeacher_ID=teacher_id))
        elif t.role == "Subject Teacher" and adviser_record:
            db.delete(adviser_record)
            
    db.commit()
    return {"message": "Teacher updated successfully"}

# --- NEW FEATURES: PASSWORDS & TEACHER CLASS SETUP ---

class AssignmentCreate(BaseModel):
    section_name: str
    subject_code: str = "EAPP" # Defaulting for this prototype
    level_id: int = 11

@teacher_router.post("/{teacher_id}/setup-class")
def setup_teacher_class(teacher_id: str, req: AssignmentCreate, db: Session = Depends(database.get_db)):
    # PDF Constraints (Max 6 loads, 3 subjects)
    current_assignments = db.query(models.TeacherAssignment).filter_by(Teacher_ID=teacher_id).all()
    if len(current_assignments) >= 6:
        raise HTTPException(status_code=400, detail="Constraint Failed: Max 6 teaching loads.")
    
    current_subjects = {a.Subject_Code for a in current_assignments}
    current_subjects.add(req.subject_code)
    if len(current_subjects) > 3:
         raise HTTPException(status_code=400, detail="Constraint Failed: Max 3 unique subjects.")

    sec = db.query(models.Section).filter(models.Section.Section_Name == req.section_name).first()
    if not sec:
        sec = models.Section(Section_Name=req.section_name, Level_ID=req.level_id, Strand_ID=1)
        db.add(sec)
        db.commit()
        db.refresh(sec)
    
    # Check if this EXACT assignment already exists
    assign = db.query(models.TeacherAssignment).filter_by(
        Teacher_ID=teacher_id, Subject_Code=req.subject_code, Section_ID=sec.Section_ID
    ).first()
    
    # THIS IS THE CRITICAL BLOCK THAT WAS BEING SKIPPED:
    if assign:
        raise HTTPException(status_code=400, detail="Duplicate Error: You already have this exact Subject and Section in your load!")
        
    setting = db.query(models.SystemSetting).first()
    active_sy = setting.Current_School_Year if setting else "2024-2025"
    active_sem = setting.Current_Semester if setting else 1

    new_assign = models.TeacherAssignment(
        Teacher_ID=teacher_id, Subject_Code=req.subject_code, Section_ID=sec.Section_ID,
        Semester=active_sem, School_Year=active_sy 
    )
    db.add(new_assign)
    db.commit()
        
    return {"message": "Class officially assigned to your load!"}

# --- NEW: DELETE TEACHING LOAD ---
@teacher_router.delete("/classes/{assignment_id}")
def delete_teacher_class(assignment_id: int, db: Session = Depends(database.get_db)):
    assign = db.query(models.TeacherAssignment).filter_by(Teacher_Assignment_ID=assignment_id).first()
    if not assign:
        raise HTTPException(status_code=404, detail="Class not found.")
    
    # Safeguard: Do not let them delete a class if grades are already submitted
    subs = db.query(models.Submission).filter_by(Teacher_Assignment_ID=assignment_id).first()
    if subs:
         raise HTTPException(status_code=400, detail="Cannot remove a class that already has official grade submissions.")
         
    db.delete(assign)
    db.commit()
    return {"message": "Class removed from load."}

@teacher_router.get("/{teacher_id}/classes")
def get_teacher_classes(teacher_id: str, db: Session = Depends(database.get_db)):
    # Fetch ONLY the classes assigned to the specific logged-in teacher
    assignments = db.query(models.TeacherAssignment).filter(models.TeacherAssignment.Teacher_ID == teacher_id).all()
    res = []
    for a in assignments:
        sec = db.query(models.Section).filter(models.Section.Section_ID == a.Section_ID).first()
        res.append({
            "assignment_id": a.Teacher_Assignment_ID,
            "section_id": a.Section_ID,
            "section_name": sec.Section_Name,
            "subject": a.Subject_Code
        })
    return res

@teacher_router.get("/classes/{assignment_id}/grades")
def get_class_grades(assignment_id: int, db: Session = Depends(database.get_db)):
    submission = db.query(models.Submission).filter_by(Teacher_Assignment_ID=assignment_id).first()
    if not submission:
        return []
        
    records = db.query(models.GradeRecord).filter_by(Submission_ID=submission.Submission_ID).all()
    setting = db.query(models.SystemSetting).first()
    is_second_sem = setting and str(setting.Current_Semester) in ['2nd', '2']
    
    res = []
    for r in records:
        if is_second_sem:
            res.append({"LRN": r.LRN, "Q1": r.Quarter_3_Grade, "Q2": r.Quarter_4_Grade})
        else:
            res.append({"LRN": r.LRN, "Q1": r.Quarter_1_Grade, "Q2": r.Quarter_2_Grade})
    return res

@principal_router.post("/archive-school-year")
def archive_school_year(db: Session = Depends(database.get_db)):
    setting = db.query(models.SystemSetting).first()
    if not setting: raise HTTPException(status_code=400, detail="System settings not found.")
        
    current_sy = setting.Current_School_Year
    students = db.query(models.Student).filter(models.Student.Section_ID != None).all()
    for student in students:
        exists = db.query(models.SchoolYear).filter_by(LRN=student.LRN, Section_ID=student.Section_ID, Academic_Year=current_sy).first()
        if not exists: db.add(models.SchoolYear(LRN=student.LRN, Section_ID=student.Section_ID, Academic_Year=current_sy))
        student.Section_ID = None
        
    try:
        parts = current_sy.split('-')
        if len(parts) == 2: setting.Current_School_Year = f"{int(parts[0])+1}-{int(parts[1])+1}"
    except: pass
        
    setting.Current_Semester = "1st"
    db.commit()
    return {"message": f"School year {current_sy} archived successfully! All students unassigned from sections, ready for the next year."}

# --- PRINCIPAL: CURRICULUM & SECTION MANAGEMENT ---

# --- CURRICULUM: SECTION MANAGEMENT ---
class SectionCreate(BaseModel):
    section_name: str
    level_id: int
    strand_id: int
    adviser_id: str = None  # NEW: Optional adviser ID

@principal_router.get("/sections")
def get_sections(db: Session = Depends(database.get_db)):
    sections = db.query(models.Section).all()
    result = []
    for sec in sections:
        adv_name = "Unassigned"
        # Look up the adviser's real name if an ID is attached
        if sec.Adviser_ID:
            adv = None
            if hasattr(models, 'Employee'):
                adv = db.query(models.Employee).filter_by(Employee_ID=sec.Adviser_ID).first()
            if not adv:
                adv = db.query(models.Teacher).filter_by(Employee_ID=sec.Adviser_ID).first()
            if adv:
                adv_name = f"{getattr(adv, 'Firstname', '')} {getattr(adv, 'Lastname', '')}"
                
        result.append({
            "Section_ID": sec.Section_ID,
            "Section_Name": sec.Section_Name,
            "Level_ID": sec.Level_ID,
            "Strand_ID": sec.Strand_ID,
            "Adviser_ID": sec.Adviser_ID,
            "Adviser_Name": adv_name
        })
    return result

@principal_router.post("/sections")
def create_section(req: SectionCreate, db: Session = Depends(database.get_db)):
    existing = db.query(models.Section).filter_by(Section_Name=req.section_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Section Name already exists.")
        
    # NEW RULE: Check if the teacher is already advising another section
    if req.adviser_id:
        existing_adv = db.query(models.Section).filter_by(Adviser_ID=req.adviser_id).first()
        if existing_adv:
            raise HTTPException(status_code=400, detail=f"Rule Violation: This teacher is already advising {existing_adv.Section_Name}!")
            
    new_sec = models.Section(
        Section_Name=req.section_name, 
        Level_ID=req.level_id, 
        Strand_ID=req.strand_id,
        Adviser_ID=req.adviser_id if req.adviser_id else None
    )
    db.add(new_sec)
    db.commit()
    return {"message": "Section created."}

# NEW ENDPOINT: Quick-assign an adviser to an existing section
@principal_router.put("/sections/{section_id}/assign-adviser")
def assign_section_adviser(section_id: int, payload: dict, db: Session = Depends(database.get_db)):
    sec = db.query(models.Section).filter_by(Section_ID=section_id).first()
    if not sec:
        raise HTTPException(status_code=404, detail="Section not found.")
    sec.Adviser_ID = payload.get("adviser_id")
    db.commit()
    return {"message": "Adviser assigned successfully!"}

# --- CURRICULUM: SUBJECT MANAGEMENT ---

from typing import Optional

class SubjectCreate(BaseModel):
    subject_code: str
    subject_name: str
    level_id: int
    subject_type: str = "Core"     # NEW: Core, Applied, or Specialized
    strand_id: Optional[int] = None

@principal_router.post("/subjects")
def create_subject(req: SubjectCreate, db: Session = Depends(database.get_db)):
    try:
        existing = db.query(models.Subject).filter_by(Subject_Code=req.subject_code).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"The subject code '{req.subject_code}' already exists!")
            
        new_subject = models.Subject(
            Subject_Code=req.subject_code,
            Subject_Name=req.subject_name,
            Level_ID=req.level_id,
            Subject_Type=req.subject_type,
            # Only save the strand if it's explicitly Specialized
            Strand_ID=req.strand_id if req.subject_type == "Specialized" else None 
        )
        db.add(new_subject)
        db.commit()
        return {"message": "Subject added successfully!"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

@principal_router.put("/subjects/{code}")
def update_subject(code: str, req: SubjectCreate, db: Session = Depends(database.get_db)):
    try:
        subject = db.query(models.Subject).filter_by(Subject_Code=code).first()
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found.")
            
        # Update the properties safely (Note: We do not change the code itself)
        subject.Subject_Name = req.subject_name
        subject.Level_ID = req.level_id
        subject.Subject_Type = req.subject_type
        subject.Strand_ID = req.strand_id if req.subject_type == "Specialized" else None
        
        db.commit()
        return {"message": "Subject updated successfully!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

@principal_router.delete("/subjects/{code}")
def delete_subject(code: str, db: Session = Depends(database.get_db)):
    subject = db.query(models.Subject).filter_by(Subject_Code=code).first()
    if subject:
        db.query(models.TeacherAssignment).filter_by(Subject_Code=code).delete()
        db.delete(subject)
        db.commit()
    return {"message": "Subject and all related class assignments deleted."}

@principal_router.delete("/sections/{section_id}")
def delete_section(section_id: int, db: Session = Depends(database.get_db)):
    sec = db.query(models.Section).filter_by(Section_ID=section_id).first()
    if sec:
        db.delete(sec)
        db.commit()
    return {"message": "Section deleted."}

# --- SHS STRAND MANAGEMENT ---
class StrandCreate(BaseModel):
    track_name: str
    strand_code: str
    strand_name: str

@curriculum_router.get("/strands")
def get_strands(db: Session = Depends(database.get_db)):
    strands = db.query(models.Strand).all()
    result = []
    for s in strands:
        track = db.query(models.Track).filter_by(Track_ID=s.Track_ID).first()
        result.append({
            "Strand_ID": s.Strand_ID,
            "Strand_Code": s.Strand_Code,
            "Strand_Name": s.Strand_Name,
            "Track_Name": track.Track_Name if track else "Unknown"
        })
    return result

@principal_router.post("/strands")
def create_strand(req: StrandCreate, db: Session = Depends(database.get_db)):
    try:
        track = db.query(models.Track).filter_by(Track_Name=req.track_name).first()
        if not track:
            track = models.Track(Track_Name=req.track_name)
            db.add(track)
            db.commit()
            db.refresh(track)
            
        existing = db.query(models.Strand).filter_by(Strand_Code=req.strand_code).first()
        if existing:
            raise HTTPException(status_code=400, detail="Strand Code already exists.")
            
        new_strand = models.Strand(
            Strand_Code=req.strand_code, 
            Strand_Name=req.strand_name, 
            Track_ID=track.Track_ID
        )
        db.add(new_strand)
        db.commit()
        return {"message": "Strand successfully added!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

@principal_router.delete("/strands/{strand_id}")
def delete_strand(strand_id: int, db: Session = Depends(database.get_db)):
    strand = db.query(models.Strand).filter_by(Strand_ID=strand_id).first()
    if strand:
        db.delete(strand)
        db.commit()
    return {"message": "Strand deleted."}

# --- PRINCIPAL: ANALYTICS DASHBOARD ---
@principal_router.get("/stats")
def get_principal_stats(db: Session = Depends(database.get_db)):
    total_teachers = db.query(models.Teacher).count()
    
    # NEW: Count students by Grade Level using a Join
    total_students = db.query(models.Student).count()
    g11_students = db.query(models.Student).join(models.Section).filter(models.Section.Level_ID == 11).count()
    g12_students = db.query(models.Student).join(models.Section).filter(models.Section.Level_ID == 12).count()
    
    total_sections = db.query(models.Section).count()
    
    active_subs = db.query(models.Submission).filter(models.Submission.Date_Submitted != date(1970, 1, 1)).all()
    total_subs = len(active_subs)
    
    approved_count = 0
    for sub in active_subs:
        rec = db.query(models.GradeRecord).filter_by(Submission_ID=sub.Submission_ID).first()
        if rec and rec.Date_Approved:
            approved_count += 1
            
    pending_count = total_subs - approved_count
    
    approval_rate = 0
    if total_subs > 0:
        approval_rate = round((approved_count / total_subs) * 100)

    return {
        "teachers": total_teachers,
        "students": {
            "total": total_students,
            "g11": g11_students,
            "g12": g12_students
        },
        "sections": total_sections,
        "submissions": {
            "total": total_subs,
            "approved": approved_count,
            "pending": pending_count,
            "rate": approval_rate
        }
    }

# --- CURRICULUM MANAGEMENT ---
@curriculum_router.get("/subjects")
def get_all_subjects(db: Session = Depends(database.get_db)):
    return db.query(models.Subject).all()

# --- ACADEMIC TERM ENGINE ---
class SettingsUpdate(BaseModel):
    school_year: str
    semester: int

@app.get("/api/settings")
def get_settings(db: Session = Depends(database.get_db)):
    # Get settings, or create default if it's the very first time running
    setting = db.query(models.SystemSetting).first()
    if not setting:
        setting = models.SystemSetting(Current_School_Year="2024-2025", Current_Semester=1)
        db.add(setting)
        db.commit()
        db.refresh(setting)
    return setting

@principal_router.put("/settings")
def update_settings(req: SettingsUpdate, db: Session = Depends(database.get_db)):
    setting = db.query(models.SystemSetting).first()
    setting.Current_School_Year = req.school_year
    setting.Current_Semester = req.semester
    db.commit()
    return {"message": "Academic Term successfully updated system-wide!"}

# --- CLASS ADVISER: REPORT CARD MODULE ---
@app.get("/api/adviser/report-cards/{section_id}")
def get_report_cards(section_id: int, db: Session = Depends(database.get_db)):
    students = db.query(models.Student).filter(models.Student.Section_ID == section_id).all()
    students.sort(key=lambda x: x.Lastname)
    
    # 1. Get a list of subjects that ACTUALLY exist in the curriculum right now
    active_subjects = [sub.Subject_Code for sub in db.query(models.Subject).all()]
    
    # 2. Get assignments, but ONLY keep them if the subject hasn't been deleted
    assignments = db.query(models.TeacherAssignment).filter(models.TeacherAssignment.Section_ID == section_id).all()
    subjects_list = sorted(list(set([a.Subject_Code for a in assignments if a.Subject_Code in active_subjects])))
    
    setting = db.query(models.SystemSetting).first()
    sy = setting.Current_School_Year if setting else "2024-2025"
    
    principal = db.query(models.Principal).first()
    principal_name = f"{principal.Firstname} {principal.Lastname}".strip() if principal else "Not Assigned"
    
    report = []
    for s in students:
        s_data = {"LRN": s.LRN, "Name": f"{s.Lastname}, {s.Firstname}", "Grades": {}, "Sem1_Avg": "-", "Sem2_Avg": "-"}
        
        sem1_total = 0
        sem1_count = 0
        sem2_total = 0
        sem2_count = 0
        
        for sub_code in subjects_list:
            s_data["Grades"][sub_code] = "Missing"
            
        for a in assignments:
            # Skip if this assignment is a ghost subject
            if a.Subject_Code not in active_subjects:
                continue
                
            sub = db.query(models.Submission).filter(models.Submission.Teacher_Assignment_ID == a.Teacher_Assignment_ID).first()
            if sub:
                rec = db.query(models.GradeRecord).filter(models.GradeRecord.Submission_ID == sub.Submission_ID, models.GradeRecord.LRN == s.LRN).first()
                if rec and rec.Date_Approved:
                    s_data["Grades"][a.Subject_Code] = {
                        "Q1": float(rec.Quarter_1_Grade) if rec.Quarter_1_Grade is not None else "-",
                        "Q2": float(rec.Quarter_2_Grade) if rec.Quarter_2_Grade is not None else "-",
                        "Sem1": float(rec.FirstSem_Average) if rec.FirstSem_Average is not None else "-",
                        "Q3": float(rec.Quarter_3_Grade) if rec.Quarter_3_Grade is not None else "-",
                        "Q4": float(rec.Quarter_4_Grade) if rec.Quarter_4_Grade is not None else "-",
                        "Sem2": float(rec.SecondSem_Average) if rec.SecondSem_Average is not None else "-"
                    }
                    if rec.FirstSem_Average is not None:
                        sem1_total += float(rec.FirstSem_Average)
                        sem1_count += 1
                    if rec.SecondSem_Average is not None:
                        sem2_total += float(rec.SecondSem_Average)
                        sem2_count += 1
                elif rec:
                    s_data["Grades"][a.Subject_Code] = "Pending"
        
        if sem1_count > 0:
            s_data["Sem1_Avg"] = round(sem1_total / sem1_count, 2)
        if sem2_count > 0:
            s_data["Sem2_Avg"] = round(sem2_total / sem2_count, 2)
            
        report.append(s_data)
        
    return {"school_year": sy, "principal_name": principal_name, "subjects": subjects_list, "report": report}

app.include_router(teacher_router)
app.include_router(principal_router)
app.include_router(curriculum_router)