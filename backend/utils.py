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


async def get_ollama_response(messages :List[Message], position, model="qwen2.5", embed_model='granite-embedding:278m'):
    try: 
        # messages.append({'role': 'user', 'content': 'I want to query the embedding model to get relevent text in return from teh embeddding model. Give me a set of one or two questions based on teh previous chat which i can send to the embedding models to get the output return. be concise in answer and give only one or two questions.'})
        # response: ChatResponse = chat(
        #     model=model,
        #     messages=messages
        # )
        # messages.pop()
        # embedding_input = response.message.content
        # print("Embeding Input response: ", embedding_input)

        embedding_input = messages[-1]['content']
        
        response = embed(
            model=embed_model,
            input=embedding_input
        )
        vector = response["embeddings"][0]
        print('Embeddings: ', vector[:10])

        search_result = client.query_points(
            collection_name=position, #query collection based on the position
            query=vector,
            with_payload=True,
            limit=2
        ).points

        context = '\n'.join([f"Context {index + 1}:\n{result.payload['text']}\n" for index, result in enumerate(search_result)])
        print(f"Messages sent to model {messages[-1]}")
        messages[-1]["content"] += f"""Above is the user message. Be concise in answering the user message unless user tells otherwise. Below you have been provided a context retrived from the embedding model based on the user input. The context may or may not be required to answer user message. For user message like "Hello" you can reply as "hello". You can use this contextto answer if required or just reply to user message if context is not relavent. Context = {context} """
        print(f"Messages sent to model {messages[-1]}")

        response: ChatResponse = chat(
            model=model,
            messages=messages
        )

        messages[-1]["content"] = embedding_input

        return response.message.content
    
    except Exception as e:
        print(f"An error occurred in get_ollama_response: {e}")
        return "Error in get_olama_chat"
