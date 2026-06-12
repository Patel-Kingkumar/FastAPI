# =========================================================
# IMPORTS
# =========================================================

# SQLAlchemy database tools
from sqlalchemy import create_engine, Column, Integer, String

# SQLAlchemy ORM features
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# FastAPI features
from fastapi import FastAPI, Depends, HTTPException


# =========================================================
# CREATE FASTAPI APP
# =========================================================

# Create FastAPI application
app = FastAPI()


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

# SQLite database file
# test.db file will be created automatically
DATABASE_URL = "sqlite:///./test.db"

# Create database engine
# check_same_thread=False is required for SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create session maker
# Session is used to communicate with database
sessionLocal = sessionmaker(bind=engine)

# Base class for creating database tables
Base = declarative_base()


# =========================================================
# DATABASE MODEL / TABLE
# =========================================================

# Create Todo table
class Todo(Base):

    # Table name inside database
    __tablename__ = "todos"

    # ID column
    # Integer -> number
    # primary_key=True -> unique ID
    # index=True -> faster searching
    id = Column(Integer, primary_key=True, index=True)

    # Todo title column
    title = Column(String)

    # Todo completed status
    # Currently storing string values:
    # "True" or "False"
    completed = Column(String)


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

# Create all tables in database
# If test.db does not exist, it will create it
Base.metadata.create_all(bind=engine)


# =========================================================
# DATABASE CONNECTION DEPENDENCY
# =========================================================

# This function creates database session
def get_db():

    # Create database connection
    db = sessionLocal()

    try:

        # Send database connection to API
        yield db

    finally:

        # Close database connection after request
        db.close()


# =========================================================
# HOME API
# =========================================================

@app.get("/")
def home(db: Session = Depends(get_db)):

    # Simple test route
    return {
        "message": "DB Connected"
    }


# =========================================================
# CREATE TODO API
# =========================================================

@app.post("/todos")
def create_todo(

    # Title coming from user
    title: str,

    # Database dependency
    db: Session = Depends(get_db)
):

    # Create Todo object
    todo = Todo(

        # Save title
        title=title,

        # Default completed value
        completed="False"
    )

    # Add data into database
    db.add(todo)

    # Save permanently
    db.commit()

    # Refresh object to get latest data
    # like auto-generated ID
    db.refresh(todo)

    # Return response
    return {
        "message": "Todo Created",
        "data": {
            "id": todo.id,
            "title": todo.title,
            "completed": todo.completed
        }
    }


# =========================================================
# GET ALL TODOS API
# =========================================================

@app.get("/todos")
def get_todos(

    # Database dependency
    db: Session = Depends(get_db)
):

    # Get all todos from database
    todos = db.query(Todo).all()

    # Return all todos
    return {
        "Total": len(todos),
        "data": todos
    }


# =========================================================
# GET TODO BY ID API
# =========================================================

@app.get("/todos/{todo_id}")
def get_todo_(

    # URL parameter
    todo_id: int,

    # Database dependency
    db: Session = Depends(get_db)
):

    # Find todo using ID
    todo = db.query(Todo).filter(
        Todo.id == todo_id
    ).first()

    # If todo not found
    if not todo:

        # Return error
        raise HTTPException(
            status_code=404,
            detail="Todo Not Found"
        )

    # Return todo data
    return todo


# =========================================================
# UPDATE TODO API
# =========================================================

@app.put("/todos/{todo_id}")
def update_todo(

    # URL parameter
    todo_id: int,

    # New title from user
    title: str,

    # Database dependency
    db: Session = Depends(get_db)
):

    # Find todo by ID
    todo = db.query(Todo).filter(
        Todo.id == todo_id
    ).first()

    # If todo not found
    if not todo:

        # Return error
        raise HTTPException(
            status_code=404,
            detail="Todo Not Found"
        )

    # Update title
    todo.title = title

    # Save changes
    db.commit()

    # Refresh updated data
    db.refresh(todo)

    # Return updated data
    return {
        "message": "Todo Updated",
        "data": todo
    }


# =========================================================
# DELETE TODO API
# =========================================================

@app.delete("/todos/{todo_id}")
def delete_todo(

    # URL parameter
    todo_id: int,

    # Database dependency
    db: Session = Depends(get_db)
):

    # Find todo by ID
    todo = db.query(Todo).filter(
        Todo.id == todo_id
    ).first()

    # If todo not found
    if not todo:

        # Return error
        raise HTTPException(
            status_code=404,
            detail="Todo Not Found"
        )

    # Delete todo
    db.delete(todo)

    # Save changes
    db.commit()

    # Return success message
    return {
        "message": "Todo Deleted"
    }

