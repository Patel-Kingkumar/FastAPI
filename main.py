from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import shutil

app = FastAPI()
    
#step - 1 Ensure uploads folder exist
UPLOAD_DIR = "uploads"

if os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
    
#step - 2 Stasic file set up
#url : http://127.0.0.1:8080/FILES/<filename>