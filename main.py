from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()
    
@app.middleware("http")
async def my_middleware(req: Request, call_next):
    print("Request Received")
    
    responce = await call_next(req)
    
    print("Responce Send")
    
    return responce