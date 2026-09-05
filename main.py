# main.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from database import SessionLocal, Student
from etl_pipeline import run_etl
from sqlalchemy import func
import csv
import io
import os

# ==========================================
# CREATE FASTAPI APP
# ==========================================
app = FastAPI(
    title="Student Performance Analytics API",
    description="A Data Engineering project demonstrating ETL, SQL, and REST APIs",
    version="2.0.0"
)

# ==========================================
# ENABLE CORS (Taki frontend backend se baat kar sake)
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# MOUNT STATIC FILES (Frontend serve karne ke liye)
# ==========================================
app.mount("/static", StaticFiles(directory="static"), name="static")

# ==========================================
# PYDANTIC MODELS (For Data Validation)
# ==========================================
class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Student's full name")
    subject: str = Field(..., min_length=1, description="Subject name")
    marks: int = Field(..., ge=0, le=100, description="Marks between 0-100")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Karan",
                "subject": "Maths",
                "marks": 88
            }
        }

class StudentResponse(BaseModel):
    id: int
    name: str
    subject: str
    marks: int
    grade: str

# ==========================================
# STARTUP EVENT: Run ETL Pipeline automatically
# ==========================================
@app.on_event("startup")
def startup_event():
    # Check if database is empty
    db = SessionLocal()
    count = db.query(Student).count()
    db.close()
    
    if count == 0:
        print("Database empty. Running ETL pipeline...")
        run_etl()
    else:
        print(f"Database already has {count} records. Skipping ETL.")

# ==========================================
# ENDPOINT 0: Serve Frontend Dashboard
# ==========================================
@app.get("/home")
def serve_frontend():
    """
    Serve the frontend dashboard
    """
    return FileResponse("static/index.html")

# ==========================================
# ENDPOINT 1: Root / Health Check
# ==========================================
@app.get("/")
def read_root():
    return {
        "message": "Student Performance Analytics API",
        "version": "2.0.0",
        "dashboard": "/home",
        "docs": "/docs",
        "endpoints": [
            "/students",
            "/students/{name}",
            "/analytics/summary",
            "/analytics/top-performers",
            "/analytics/subject-average",
            "/export-csv"
        ]
    }

# ==========================================
# ENDPOINT 2: Get All Students (GET)
# ==========================================
@app.get("/students", response_model=list[StudentResponse])
def get_all_students():
    """
    Retrieve all student records from the SQL database
    """
    db = SessionLocal()
    results = db.query(Student).all()
    db.close()
    
    if not results:
        raise HTTPException(status_code=404, detail="No students found in database")
    
    return results

# ==========================================
# ENDPOINT 3: Get Student by Name (GET with Path Parameter)
# ==========================================
@app.get("/students/{name}")
def get_student_by_name(name: str):
    """
    Retrieve all subjects and marks for a specific student
    """
    db = SessionLocal()
    results = db.query(Student).filter(Student.name == name).all()
    db.close()
    
    if not results:
        raise HTTPException(status_code=404, detail=f"Student '{name}' not found")
    
    student_data = []
    for s in results:
        student_data.append({
            "subject": s.subject,
            "marks": s.marks,
            "grade": s.grade
        })
    
    return {
        "name": name,
        "total_subjects": len(student_data),
        "results": student_data
    }

# ==========================================
# ENDPOINT 4: Add New Student (POST with Data Validation)
# ==========================================
@app.post("/students", response_model=StudentResponse, status_code=201)
def add_student(student: StudentCreate):
    """
    Add a new student record with Pydantic data validation
    """
    db = SessionLocal()
    
    # Check for duplicate entry
    existing = db.query(Student).filter(
        Student.name == student.name,
        Student.subject == student.subject
    ).first()
    
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="Student already exists for this subject")
    
    # Calculate grade
    marks = student.marks
    if marks >= 90:
        grade = 'A'
    elif marks >= 80:
        grade = 'B'
    elif marks >= 70:
        grade = 'C'
    elif marks >= 60:
        grade = 'D'
    else:
        grade = 'F'
    
    # Create new student record
    new_student = Student(
        name=student.name,
        subject=student.subject,
        marks=marks,
        grade=grade
    )
    
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    db.close()
    
    return new_student

# ==========================================
# ENDPOINT 5: Analytics - Summary Statistics
# ==========================================
@app.get("/analytics/summary")
def get_summary():
    """
    Get overall summary statistics using SQL aggregations
    """
    db = SessionLocal()
    
    total_students = db.query(Student).count()
    avg_marks = db.query(func.avg(Student.marks)).scalar()
    max_marks = db.query(func.max(Student.marks)).scalar()
    min_marks = db.query(func.min(Student.marks)).scalar()
    
    # Grade distribution
    grade_distribution = db.query(Student.grade, func.count(Student.grade)).group_by(Student.grade).all()
    
    db.close()
    
    return {
        "total_records": total_students,
        "average_marks": round(avg_marks, 2) if avg_marks else 0,
        "maximum_marks": max_marks,
        "minimum_marks": min_marks,
        "grade_distribution": {grade: count for grade, count in grade_distribution}
    }

# ==========================================
# ENDPOINT 6: Analytics - Top Performers
# ==========================================
@app.get("/analytics/top-performers")
def get_top_performers(limit: int = Query(5, ge=1, le=20, description="Number of top performers to return")):
    """
    Get top performing students based on average marks
    """
    db = SessionLocal()
    
    # SQL Query: SELECT name, AVG(marks), COUNT(*) FROM students GROUP BY name ORDER BY AVG(marks) DESC
    results = db.query(
        Student.name,
        func.avg(Student.marks).label('avg_marks'),
        func.count(Student.id).label('total_subjects')
    ).group_by(Student.name).order_by(func.avg(Student.marks).desc()).limit(limit).all()
    
    db.close()
    
    top_performers = []
    for rank, (name, avg_marks, total_subjects) in enumerate(results, 1):
        top_performers.append({
            "rank": rank,
            "name": name,
            "average_marks": round(avg_marks, 2),
            "total_subjects": total_subjects
        })
    
    return {"top_performers": top_performers}

# ==========================================
# ENDPOINT 7: Analytics - Subject-wise Average
# ==========================================
@app.get("/analytics/subject-average")
def get_subject_averages():
    """
    Get average marks for each subject using SQL GROUP BY
    """
    db = SessionLocal()
    
    results = db.query(
        Student.subject,
        func.avg(Student.marks).label('avg_marks'),
        func.count(Student.id).label('student_count')
    ).group_by(Student.subject).all()
    
    db.close()
    
    subject_stats = []
    for subject, avg_marks, student_count in results:
        subject_stats.append({
            "subject": subject,
            "average_marks": round(avg_marks, 2),
            "total_students": student_count
        })
    
    return {"subject_statistics": subject_stats}

# ==========================================
# ENDPOINT 8: Export Data as CSV
# ==========================================
@app.get("/export-csv")
def export_csv():
    """
    Export all student data as CSV file
    """
    db = SessionLocal()
    results = db.query(Student).all()
    db.close()
    
    if not results:
        raise HTTPException(status_code=404, detail="No data to export")
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(["ID", "Name", "Subject", "Marks", "Grade"])
    
    # Write data
    for s in results:
        writer.writerow([s.id, s.name, s.subject, s.marks, s.grade])
    
    output.seek(0)
    
    # Return as downloadable file
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=students_data.csv"}
    )