from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models, database
from security import verify_password, create_access_token, get_password_hash
import traceback
import sys

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    employee_id: str
    password: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(database.get_db)):
    employee = None
    if hasattr(models, 'Employee'):
        employee = db.query(models.Employee).filter(models.Employee.Employee_ID == request.employee_id).first()
        
    if not employee and hasattr(models, 'Teacher'):
        employee = db.query(models.Teacher).filter(models.Teacher.Employee_ID == request.employee_id).first()
        if employee:
            employee.Employee_Type = getattr(employee, 'Teacher_Type', "Teacher")
            
    if not employee and hasattr(models, 'Principal'):
        employee = db.query(models.Principal).filter(models.Principal.Employee_ID == request.employee_id).first()
        if employee:
            employee.Employee_Type = "Principal"
            
    if not employee:
        raise HTTPException(status_code=401, detail="Invalid Employee ID or Password")
        
    pass_col = getattr(employee, 'Password', getattr(employee, 'password', None))
    
    is_match = False
    if pass_col:
        pass_str = str(pass_col).strip()
        req_pass = str(request.password).strip()[:72]
        
        if pass_str == req_pass:
            is_match = True
        else:
            try:
                if verify_password(req_pass, pass_str):
                    is_match = True
            except Exception as e:
                print(f"\n[LOGIN VERIFY ERROR] {e}", file=sys.stderr)
                traceback.print_exc()
                
    if not is_match:
        raise HTTPException(status_code=401, detail="Invalid Employee ID or Password")
    
    role = getattr(employee, 'Employee_Type', getattr(employee, 'employee_type', 'Teacher'))
    
    access_token = create_access_token(
        data={"sub": employee.Employee_ID, "role": role}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": role,
        "employee_id": employee.Employee_ID
    }

@router.post("/change-password/{employee_id}")
def change_password(employee_id: str, req: PasswordChange, db: Session = Depends(database.get_db)):
    employee = None
    if hasattr(models, 'Employee'):
        employee = db.query(models.Employee).filter(models.Employee.Employee_ID == employee_id).first()
    if not employee and hasattr(models, 'Teacher'):
        employee = db.query(models.Teacher).filter(models.Teacher.Employee_ID == employee_id).first()
    if not employee and hasattr(models, 'Principal'):
        employee = db.query(models.Principal).filter(models.Principal.Employee_ID == employee_id).first()
        
    if not employee:
        raise HTTPException(status_code=404, detail="User not found.")
        
    pass_col = getattr(employee, 'Password', getattr(employee, 'password', None))
    is_match = False
    if pass_col:
        pass_str = str(pass_col).strip()
        old_pass = str(req.old_password).strip()[:72]
        if pass_str == old_pass:
            is_match = True
        else:
            try:
                if verify_password(old_pass, pass_str):
                    is_match = True
            except Exception as e:
                print(f"\n[CHANGE PWD VERIFY ERROR]: {e}", file=sys.stderr)
                traceback.print_exc()
                
    if not is_match:
        raise HTTPException(status_code=400, detail="Incorrect current password.")
        
    new_hash = get_password_hash(str(req.new_password).strip()[:72])
    for attr in ['Password', 'password']:
        if hasattr(employee, attr):
            setattr(employee, attr, new_hash)
            
    db.commit()
    return {"message": "Password successfully updated!"}