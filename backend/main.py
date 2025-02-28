from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

@app.get("/")
async def get_message():
    return {"message": "Hello"}

@app.post("/")
async def post_message(request: TextRequest):
    return {"message": "Hello " + request.text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)