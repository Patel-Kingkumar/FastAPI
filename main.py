from fastapi import FastAPI, Depends, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()
    
# def common_logic():
#     return {
#         "message": "Common logic execution"
#     }
    
# @app.get("/home")
# def home(data = Depends(common_logic)):
#     return data

# @app.get("/profile")
# def profile(data = Depends(common_logic)):
#     return data



def verify_token(token: str = Header(None)):
    if token != "mysecreattoken":
        raise HTTPException (
            status_code = 401,
            detail = "Unauthorized"
        )
    return {
        "user": "Authorized User"
    }
    
@app.get("/secure")
def secure(user = Depends(verify_token)): 
    return {
        "message": "Secure data access",
        "user": user
    }
    