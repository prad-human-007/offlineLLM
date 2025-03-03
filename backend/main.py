from fastapi import FastAPI, Request, Depends, HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from ollama import chat, ChatResponse
from utils import RequestModel, get_ollama_response
from fastapi_jwt import JwtAccessBearer

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
        "password": "123",  # Store hashed passwords in production
        "position": "ceo"
    },
    "tony": {
        "password": "123",
        "position": "ceo"
    },
    "sam": {
        "password": "456",
        "position": "manager"
    }, 
    "rob": {
        "password": "789",
        "position": "employee"
    }
}

@app.post("/login")
async def login(user: UserLogin):
    if user.username not in fake_users_db or fake_users_db[user.username]["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # The error is here - in fastapi_jwt, the subject shouldn't be a string directly
    # Instead, we need to create a dict with the subject field
    access_token = jwt.create_access_token(subject={"username": user.username})
    return {"access_token": access_token}



@app.get("/")
async def get_message(token: str = Depends(jwt)):
    return {"message": "Hello"}

@app.post("/")
async def post_message(request: RequestModel, subject: str = Depends(jwt)): 
    username = subject['username']
    position = fake_users_db[username]['position']
    print("Request made by: ", username, "position: ", position) 
    messages = [{"role": message.role, "content": message.content} for message in request.messages]
    print("Input Message Length", len(messages))
    responseMsg = await get_ollama_response(messages=messages, position=position)
    return {"message": responseMsg}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)