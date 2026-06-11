from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

app = FastAPI()

#custom exception handler
# class UserNotFoundException(Exception):
#     def __init__(self, name: str):
#         self.name = name
        
# @app.get("/user/{name}")
# def get_name(name: str):
#     if name != "King":
#         raise UserNotFoundException
#     return {
#         "name": name
#     }

#built-in exception handler
# @app.get("/user/{user_id}")
# def get_user_by_id(user_id: int):
#     if user_id != 1:
#         raise HTTPException(
#             status_code=404,
#             detail="User Not Found"
#         )
#     return {
#         "message": "User Retrieved"
#     }
    
        