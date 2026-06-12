
# FastAPI Full Tutorial

## 1. What is FastAPI?
FastAPI is a modern Python web framework for building APIs quickly using Python type hints.

Features:
- Fast performance
- Automatic Swagger documentation
- Easy request validation
- Async support

---

## 2. Install FastAPI

```bash
pip install fastapi uvicorn
```

---

## 3. Create Your First API

Create a file named `main.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello FastAPI"}
```

Run server:

```bash
uvicorn main:app --reload
```

Open:
- http://127.0.0.1:8000
- Swagger Docs: http://127.0.0.1:8000/docs

---

## 4. Path Parameters

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

Example:
- `/users/10`

---

## 5. Query Parameters

```python
@app.get("/products/")
def get_products(limit: int = 10):
    return {"limit": limit}
```

Example:
- `/products/?limit=5`

---

## 6. Request Body with Pydantic

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

@app.post("/users/")
def create_user(user: User):
    return user
```

---

## 7. Response Model

```python
from pydantic import BaseModel

class UserResponse(BaseModel):
    name: str

@app.get("/profile/", response_model=UserResponse)
def profile():
    return {
        "name": "King",
        "password": "secret"
    }
```

Only `name` will be returned.

---

## 8. CRUD Example

```python
from fastapi import FastAPI

app = FastAPI()

items = []

@app.post("/items/")
def create_item(item: dict):
    items.append(item)
    return item

@app.get("/items/")
def get_items():
    return items

@app.put("/items/{index}")
def update_item(index: int, item: dict):
    items[index] = item
    return item

@app.delete("/items/{index}")
def delete_item(index: int):
    deleted = items.pop(index)
    return deleted
```

---

## 9. Async API

```python
@app.get("/async")
async def async_route():
    return {"message": "Async Route"}
```

---

## 10. Dependency Injection

```python
from fastapi import Depends

def common():
    return {"token": "abc123"}

@app.get("/secure")
def secure(data = Depends(common)):
    return data
```

---

## 11. Database with SQLAlchemy

Install:

```bash
pip install sqlalchemy
```

Example:

```python
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
```

---

## 12. FastAPI Folder Structure

```text
project/
│
├── main.py
├── routers/
├── models/
├── schemas/
├── database/
└── requirements.txt
```

---

## 13. JWT Authentication

Install:

```bash
pip install python-jose passlib bcrypt
```

Example:

```python
from jose import jwt

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"

data = {"sub": "admin"}

token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

print(token)
```

---

## 14. File Upload

```python
from fastapi import UploadFile, File

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return {"filename": file.filename}
```

---

## 15. Environment Variables

Install:

```bash
pip install python-dotenv
```

`.env`

```env
SECRET_KEY=abc123
```

Load:

```python
from dotenv import load_dotenv
import os

load_dotenv()

secret = os.getenv("SECRET_KEY")
```

---

## 16. Middleware

```python
@app.middleware("http")
async def log_requests(request, call_next):
    response = await call_next(request)
    return response
```

---

## 17. CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 18. APIRouter

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test():
    return {"message": "Router working"}
```

Main file:

```python
from routers.test import router

app.include_router(router)
```

---

## 19. Deployment

Run Production:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Deploy Platforms:
- Render
- Railway
- AWS
- DigitalOcean

---

## 20. Best Practices

- Use virtual environments
- Separate routers
- Use environment variables
- Validate data using Pydantic
- Use async where needed
- Write reusable services

---

## 21. FastAPI vs Flask

| Feature | FastAPI | Flask |
|---|---|---|
| Speed | Very Fast | Moderate |
| Validation | Built-in | Manual |
| Async | Native | Limited |
| Docs | Auto Generated | Extensions Needed |

---

## 22. Useful Commands

```bash
pip freeze > requirements.txt
```

```bash
uvicorn main:app --reload
```

```bash
python -m venv venv
```

Activate Virtual Environment:

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

---

## 23. Learning Roadmap

1. Basic Routes
2. Path & Query Parameters
3. Pydantic
4. CRUD APIs
5. Database
6. Authentication
7. Deployment
8. Docker
9. Testing
10. Microservices

---

## 24. Final Complete Example

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    name: str
    price: float

products = []

@app.post("/products")
def create_product(product: Product):
    products.append(product)
    return product

@app.get("/products")
def get_products():
    return products
```

Run:

```bash
uvicorn main:app --reload
```

