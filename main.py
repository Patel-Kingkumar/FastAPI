from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()
    
@app.post("/create-user", status_code=status.HTTP_201_CREATED)
def create_user():
    return {
        "message": "User Created",
    }
    
@app.get("/get-user")
def get_user():
    return {
        "status": status.HTTP_200_OK,
        "message": "User Retrieved",
    }
    
@app.get("/get-user/{user_id}")
def get_user_by_id(user_id: int):
    if user_id == 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
    return {
        "status": status.HTTP_200_OK,
        "message": "User with ID Retrieved",
    }