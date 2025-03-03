from parse import get_chunks_from_filename
from ollama import chat, embed, ChatResponse, EmbedResponse
from pydantic import BaseModel
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
import os
import json

class TextChunks(BaseModel):
    chunks: List[str]

def get_md_filenames(directory):
    md_filenames = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_filenames.append(os.path.join(root, file))
    return md_filenames


def get_embedddings_from_dir(dir, embed_model='granite-embedding:278m'):
    filenames = get_md_filenames(dir)
    chunks = []
    for filename in filenames:
        chunks.extend(get_chunks_from_filename(filename=filename))
    
    embeddings = []

    for chunk in chunks:
        print(f'Creating Embedding for data' , chunk['data'])
        # chunk_data = chunk['data'].splitlines()
        response = chat(
            model='qwen2.5',
            messages=[
                {
                    "role": "user",
                    "content": f"convert this into chunks of max size 512 using common sense. I want to the embedding model. All the text provided should be included no words to be omited or altered. Only if there are tables then you can convert each table row into single line sentence which is readable.  This is the text:  {chunk['data']}"
                }
            ],
            format=TextChunks.model_json_schema()
        )
        json_data = json.loads(response.message.content)
        # print("JSON DATA: ", json_data)
        print("\n")
        print("Server Embed Res: ", type(json_data), json_data['chunks'])

        for data in json_data['chunks']:
            response = embed(
                model=embed_model,
                input=data
            )
            vector = response["embeddings"][0]
            embeddings.append({"vector": vector, "data": chunk['data']})
    
    return embeddings


def create_collection(name: str, embeddings=[], vector_size=768):
    client = QdrantClient(url='http://localhost:6333')

    if(not client.collection_exists(name)):
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.DOT),
        )

    point_struct = [ PointStruct(id=idx, vector=embedding['vector'], payload={"text": embedding['data']}) for idx, embedding in enumerate(embeddings)]

    operation = client.upsert(
        collection_name=name,
        wait=True,
        points = point_struct
    )
    print(" Upsert: ", operation)

if __name__ == "__main__":

    employee_embeddings = get_embedddings_from_dir('./data/employee')
    manager_embeddings = employee_embeddings + get_embedddings_from_dir('./data/manager')
    ceo_embeddings = manager_embeddings + get_embedddings_from_dir('./data/ceo')

    len(employee_embeddings)

    create_collection('ceo', ceo_embeddings)
    create_collection('manager', manager_embeddings)
    create_collection('employee', embeddings=employee_embeddings)


