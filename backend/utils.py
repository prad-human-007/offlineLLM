from pydantic import BaseModel
from typing import List
from ollama import chat, embed, ChatResponse
from qdrant_client import QdrantClient

class TextRequest(BaseModel):
    text: str

class Message(BaseModel):
    role: str
    content: str
    
class RequestModel(BaseModel):
    messages: List[Message]

print("Entered Utils")
client = QdrantClient(url='http://localhost:6333')

async def get_ollama_response(messages :List[Message], model="qwen2.5", embed_model='granite-embedding:278m'):
    try: 
        messages.append({'role': 'user', 'content': 'I want to query the embedding model to get relevent text in return from teh embeddding model. Give me a set of one or two questions based on teh previous chat which i can send to the embedding models to get the output return. be concise in answer and give only one or two questions.'})
        response: ChatResponse = chat(
            model=model,
            messages=messages
        )
        messages.pop()
        embeding_input = response.message.content
        print("Embeding Input response: ", embeding_input)
        
        response = embed(
            model=embed_model,
            input=embeding_input
        )
        vector = response["embeddings"][0]
        print('Embeddings: ', vector[:10])

        search_result = client.query_points(
            collection_name='pdf_data',
            query=vector,
            with_payload=True,
            limit=2
        ).points

        context = '\n'.join([f"Context {index + 1}:\n{result.payload['text']}\n" for index, result in enumerate(search_result)])
        print(f"Messages sent to model {messages[-1]}")
        messages[-1]["content"] += f"""The following is the context retrivied from the embedding model 
                                    you can use this to ans teh question if you want {context}"""
        print(f"Messages sent to model {messages[-1]}")

        response: ChatResponse = chat(
            model=model,
            messages=messages
        )

        return response.message.content
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error in get_olama_chat"
