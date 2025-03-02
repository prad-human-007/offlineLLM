from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import requests
import httpx

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
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen2.5",
                "messages": [
                    {
                        "role": "user",
                        "content": request.text
                    }
                ],
                "stream": False
            }
        )
        data = response.json()
        try:
            message_content = data['message']['content']
            print("Response: ", message_content)
            return {'message': message_content}
        except KeyError:
            print("Error: Unexpected response structure", data)
            return {'error': 'Unexpected response structure'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)