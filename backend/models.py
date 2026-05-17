from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Date, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

class Person(Base):
    __tablename__ = "PERSON"
    Person_ID = Column(Integer, primary_key=True, index=True)
    Lastname = Column(String(50), nullable=False)
    Firstname = Column(String(50), nullable=False)
    Middlename = Column(String(50))
    Birth_Date = Column(Date)
    Sex = Column(String(1), CheckConstraint("Sex IN ('M', 'F')"))
    Age = Column(Integer) # Derived in application logic
    Person_Type = Column(String(10), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": Person_Type,
        "polymorphic_identity": "Person"
    }

class Employee(Person):
    __tablename__ = "EMPLOYEE"
    EPerson_ID = Column(Integer, ForeignKey("PERSON.Person_ID"), primary_key=True)
    Employee_ID = Column(String(20), unique=True, nullable=False)
    Employee_Type = Column(String(10), nullable=False)
    Password = Column(String(100), nullable=False, default="password123")

    __mapper_args__ = {"polymorphic_identity": "Employee"}

class Track(Base):
    __tablename__ = "TRACK"
    Track_ID = Column(Integer, primary_key=True, index=True)
    Track_Name = Column(String(50), unique=True, nullable=False)

class Strand(Base):
    __tablename__ = "STRAND"
    Strand_ID = Column(Integer, primary_key=True, index=True)
    Strand_Code = Column(String(15), unique=True, nullable=False) 
    Strand_Name = Column(String(100), nullable=False)             
    Track_ID = Column(Integer, ForeignKey("TRACK.Track_ID"))

class SystemSetting(Base):
    __tablename__ = "SYSTEM_SETTING"
    ID = Column(Integer, primary_key=True, index=True)
    Current_School_Year = Column(String(20), default="2024-2025")
    Current_Semester = Column(String(10), default="1st")
    
class Student(Person):
    __tablename__ = "STUDENT"
    SPerson_ID = Column(Integer, ForeignKey("PERSON.Person_ID"), primary_key=True)
    LRN = Column(Integer, unique=True, nullable=False)
    Section_ID = Column(Integer, ForeignKey("SECTION.Section_ID"))
    
    __mapper_args__ = {"polymorphic_identity": "Student"}

class Teacher(Employee):
    __tablename__ = "TEACHER"
    TEPerson_ID = Column(Integer, ForeignKey("EMPLOYEE.EPerson_ID"), primary_key=True)
    Teacher_ID = Column(String(20), unique=True, nullable=False)
    Teacher_Type = Column(String(15))

    __mapper_args__ = {"polymorphic_identity": "Teacher"}

class Adviser(Base):
    __tablename__ = "ADVISER"
    ATeacher_ID = Column(String(20), ForeignKey("TEACHER.Teacher_ID"), primary_key=True)

class Principal(Employee):
    __tablename__ = "PRINCIPAL"
    PEmployee_ID = Column(Integer, ForeignKey("EMPLOYEE.EPerson_ID"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "Principal"}

class Level(Base):
    __tablename__ = "LEVEL"
    Level_ID = Column(Integer, primary_key=True)
    Grade_Level = Column(String(10), CheckConstraint("Grade_Level IN ('Grade11', 'Grade12')"))

class Subject(Base):
    __tablename__ = "SUBJECT"
    Subject_Code = Column(String(20), primary_key=True, index=True)
    Subject_Name = Column(String(100), nullable=False)
    Level_ID = Column(Integer, nullable=False)
    Subject_Type = Column(String(20), default="Core")
    Strand_ID = Column(Integer, ForeignKey("STRAND.Strand_ID"), nullable=True)

class Section(Base):
    __tablename__ = "SECTION"
    Section_ID = Column(Integer, primary_key=True, index=True)
    Section_Name = Column(String(50), unique=True, nullable=False)
    Level_ID = Column(Integer, nullable=False)
    Strand_ID = Column(Integer, ForeignKey("STRAND.Strand_ID"))
    Adviser_ID = Column(String(50), nullable=True)

class SchoolYear(Base):
    __tablename__ = "SCHOOL_YEAR"
    LRN = Column(Integer, ForeignKey("STUDENT.LRN"), primary_key=True)
    Section_ID = Column(Integer, ForeignKey("SECTION.Section_ID"), primary_key=True)
    Academic_Year = Column(String(9))

class TeacherAssignment(Base):
    __tablename__ = "TEACHER_ASSIGNMENT"
    Teacher_Assignment_ID = Column(Integer, primary_key=True)
    Teacher_ID = Column(String(20), ForeignKey("TEACHER.Teacher_ID"))
    Subject_Code = Column(String(10), ForeignKey("SUBJECT.Subject_Code"))
    Section_ID = Column(Integer, ForeignKey("SECTION.Section_ID"))
    Semester = Column(Integer)
    School_Year = Column(String(9))

class Submission(Base):
    __tablename__ = "SUBMISSION"
    Submission_ID = Column(Integer, primary_key=True)
    Date_Submitted = Column(Date)
    Teacher_Assignment_ID = Column(Integer, ForeignKey("TEACHER_ASSIGNMENT.Teacher_Assignment_ID"))

class GradeRecord(Base):
    __tablename__ = "GRADE_RECORD"
    Record_ID = Column(Integer, primary_key=True)
    LRN = Column(Integer, ForeignKey("STUDENT.LRN"))
    PEmployee_ID = Column(Integer, ForeignKey("PRINCIPAL.PEmployee_ID"), nullable=True)
    Submission_ID = Column(Integer, ForeignKey("SUBMISSION.Submission_ID"))
    Subject_Code = Column(String(10), ForeignKey("SUBJECT.Subject_Code"))
    Quarter_1_Grade = Column(Numeric(5, 2))
    Quarter_2_Grade = Column(Numeric(5, 2))
    FirstSem_Average = Column(Numeric(5, 2)) # Derived
    Quarter_3_Grade = Column(Numeric(5, 2))
    Quarter_4_Grade = Column(Numeric(5, 2))
    SecondSem_Average = Column(Numeric(5, 2)) # Derived
    Date_Approved = Column(Date, nullable=True)