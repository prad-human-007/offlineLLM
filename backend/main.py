from fastapi import FastAPI, Request, Depends, HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from ollama import chat, ChatResponse
from utils import RequestModel, OllamaUser
from fastapi_jwt import JwtAccessBearer
from datetime import timedelta
import hashlib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jwt = JwtAccessBearer(secret_key="my_secret")

# User login model
class UserLogin(BaseModel):
    username: str
    password: str

# Fake user database (replace with real user validation)
fake_users_db = {
    "admin": {
        "password": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",  # Store hashed passwords in production
        "position": "ceo"
    },
    "tony": {
        "password": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
        "position": "ceo"
    },
    "sam": {
        "password": "b3a8e0e1f9ab1bfe3a36f231f676f78bb30a519d2b21e6c530c0eee8ebb4a5d0",
        "position": "manager"
    }, 
    "rob": {
        "password": "35a9e381b1a27567549b5f8a6f783c167ebf809f1c4d6a9e367240484d8ce281",
        "position": "employee"
    }
}



@app.post("/login")
async def login(user: UserLogin):
    user_password_hash = hashlib.sha256(user.password.encode()).hexdigest()
    if user.username not in fake_users_db or fake_users_db[user.username]["password"] != user_password_hash:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # The error is here - in fastapi_jwt, the subject shouldn't be a string directly
    # Instead, we need to create a dict with the subject field
    access_token = jwt.create_access_token(subject={"username": user.username}, expires_delta=timedelta(minutes=100))
    return {"access_token": access_token}



@app.get("/")
async def get_message(token: str = Depends(jwt)):
    return {"message": "Hello"}

@app.post("/")
async def post_message(request: RequestModel, subject: str = Depends(jwt)): 
    user = OllamaUser(username=subject['username'], position=fake_users_db[subject['username']]['position'])
    print("Request made by: ", user.username, "position: ", user.position) 
    messages = [{"role": message.role, "content": message.content} for message in request.messages]
    print("Input Message Length", len(messages))
    responseMsg = await user.get_ollama_response(messages=messages)
    return {"message": responseMsg}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)