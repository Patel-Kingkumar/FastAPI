# =========================================================
# IMPORTS
# =========================================================

# FastAPI imports
from fastapi import FastAPI, Depends, HTTPException

# Pydantic model for request validation
from pydantic import BaseModel

# SQLAlchemy database imports
from sqlalchemy import create_engine, Column, Integer, String

# SQLAlchemy ORM imports
from sqlalchemy.orm import sessionmaker, declarative_base, Session


# =========================================================
# CREATE FASTAPI APP
# =========================================================

app = FastAPI()


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

# SQLite database path
DATABASE_URL = "sqlite:///./student.db"

# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create database session
sessionLocal = sessionmaker(bind=engine)

# Base class for database models
Base = declarative_base()


# =========================================================
# PYDANTIC MODEL
# =========================================================

# Used for request body validation
class StudentCreate(BaseModel):

    sname: str
    sage: int
    semail: str


# =========================================================
# SQLALCHEMY MODEL
# =========================================================

# Database table model
class Student(Base):

    # Table name
    __tablename__ = "student"

    # Student ID
    sid = Column(Integer, primary_key=True, index=True)

    # Student Name
    sname = Column(String)

    # Student Age
    sage = Column(Integer)

    # Student Email
    semail = Column(String)


# =========================================================
# CREATE DATABASE TABLE
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# DATABASE CONNECTION DEPENDENCY
# =========================================================

def get_db():

    # Create database session
    db = sessionLocal()

    try:

        # Send database session
        yield db

    finally:

        # Close database session
        db.close()


# =========================================================
# HOME API
# =========================================================

@app.get("/", tags=["Student"])
def home():

    return {
        "message": "Student Database Connected Successfully"
    }


# =========================================================
# CREATE STUDENT API
# =========================================================

@app.post("/student", tags=["Student"])
def create_student(

    # Request body
    student: StudentCreate,

    # Database session
    db: Session = Depends(get_db)
):

    # Create SQLAlchemy object
    new_student = Student(

        sname=student.sname,
        sage=student.sage,
        semail=student.semail
    )

    # Add into database
    db.add(new_student)

    # Save changes
    db.commit()

    # Refresh latest data
    db.refresh(new_student)

    return {
        "message": "Student Created Successfully",
        "data": {
            "sid": new_student.sid,
            "sname": new_student.sname,
            "sage": new_student.sage,
            "semail": new_student.semail
        }
    }


# =========================================================
# GET ALL STUDENTS API
# =========================================================

@app.get("/student", tags=["Student"])
def get_students(

    db: Session = Depends(get_db)
):

    # Fetch all students
    students = db.query(Student).all()

    return {
        "message": "Students Retrieved Successfully",
        "total_students": len(students),
        "data": students
    }


# =========================================================
# GET STUDENT BY ID API
# =========================================================

@app.get("/student/{sid}", tags=["Student"])
def get_student_by_id(

    sid: int,

    db: Session = Depends(get_db)
):

    # Find student by ID
    student = db.query(Student).filter(
        Student.sid == sid
    ).first()

    # Check student exists or not
    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student Not Found"
        )

    return {
        "message": "Student Found Successfully",
        "data": student
    }


# =========================================================
# DELETE STUDENT API
# =========================================================

@app.delete("/student/{sid}", tags=["Student"])
def delete_student(

    sid: int,

    db: Session = Depends(get_db)
):

    # Find student by ID
    student = db.query(Student).filter(
        Student.sid == sid
    ).first()

    # Check student exists or not
    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student Not Found"
        )

    # Delete student
    db.delete(student)

    # Save changes
    db.commit()

    return {
        "message": "Student Deleted Successfully"
    }


# =========================================================
# UPDATE STUDENT API
# =========================================================

@app.put("/student/{sid}", tags=["Student"])
def update_student(

    sid: int,

    # Request body
    student: StudentCreate,

    # Database session
    db: Session = Depends(get_db)
):

    # Find existing student
    old_student = db.query(Student).filter(
        Student.sid == sid
    ).first()

    # Check student exists or not
    if not old_student:

        raise HTTPException(
            status_code=404,
            detail="Student Not Found"
        )

    # Update student data
    old_student.sname = student.sname
    old_student.sage = student.sage
    old_student.semail = student.semail

    # Save updated changes
    db.commit()

    # Refresh latest data
    db.refresh(old_student)

    return {
        "message": "Student Updated Successfully",
        "data": {
            "sid": old_student.sid,
            "sname": old_student.sname,
            "sage": old_student.sage,
            "semail": old_student.semail
        }
    }

