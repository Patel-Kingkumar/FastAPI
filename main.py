from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
    
#home route
# @app.get("/")
# def home():
#     return {"message": "Hello, World!"}

#about route
# @app.get("/about")
# def about():
#     return {"message": "This is a simple FastAPI application."}

#users route
# @app.get("/users")
# def users():
#     return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

#get by id route
# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     return {"id": user_id, "name": f"User {user_id}"}

#query params
# @app.get("/users1")
# def get_user(name: str = None):
#     return {"name": name}

# @app.post("/create-user")
# def create_user(name: str, age: int): it's like query paramas
#     return {"name": name, "age": age}

# def create_user(user: dict):
#     return {
#         "message": "User created successfully",
#         "data": user
#     }

# schema for user with nested schema
# class Address(BaseModel):
#     city: str
#     state: str
    
# class User(BaseModel):
#     name: str
#     age: int
#     address: Address

# @app.post("/create-user")
# def create_user(user: User):
#     return {
#         "message": "User created successfully",
#         "data": user
#     }

#CRUD operations with in-memory storage

todos = []

class Todo(BaseModel):
    id: int
    title: str
    completed: bool
    
@app.post("/todos")
def create_todo(todo: Todo):
    todos.append(todo)
    return {
        "message": "Todo created successfully",
        "data": todo
    }

@app.get("/todos")
def get_todos():
    return {
        "message": "Todos retrieved successfully",
        "data": todos
    }
    
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return {
                "message": "Todo retrieved successfully",
                "data": todo
            }
    return {"message": "Todo not found"}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, update_todo: Todo):
    for i, t in enumerate(todos):
        if t.id == todo_id:
            todos[i] = update_todo
            return {
                "message": "Todo updated successfully",
                "data": update_todo
            }
    return {"message": "Todo not found"}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, t in enumerate(todos):
        if t.id == todo_id:
            del todos[i]
            return {"message": "Todo deleted successfully"}
    return {"message": "Todo not found"}