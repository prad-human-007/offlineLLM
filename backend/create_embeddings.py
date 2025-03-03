import os
import json
from PIL import Image
import ollama
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
import numpy as np
import re


# Define the directory containing the files
data_dir = './data'

# Initialize lists to hold the loaded data
images = []
md_content = ""
json_content = {}

# # Load images
# for file_name in os.listdir(data_dir):
#     if file_name.endswith('.png') or file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
#         image_path = os.path.join(data_dir, file_name)
#         images.append(Image.open(image_path))

# Load markdown file

with open('./data/ceo/ceo.md', 'r') as md_file:
    md_content = md_file.read()

# # Load JSON file
# json_file_path = os.path.join(data_dir, 'thinkpython_meta.json')
# if os.path.exists(json_file_path):
#     with open(json_file_path, 'r') as json_file:
#         json_content = json.load(json_file)

# Print loaded data for verification
# print(f"Loaded {len(images)} images.")
# print(f"Markdown content: {md_content[:100]}...")  # Print first 100 characters
# print(f"JSON content: {json_content}")


# Function to split text into chunks of specified length
def split_text_into_chunks(text, chunk_size, overlap):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size-overlap)]

def chunk_text(text, max_length=512, overlap=50):
    words = re.findall(r'\S+', text)  # Split text into words while keeping spaces
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        word_length = len(word) + 1  # +1 for the space after each word

        # If adding the word exceeds max_length
        if current_length + word_length > max_length:
            if current_chunk:  # Save the current chunk
                chunks.append(" ".join(current_chunk))

            # Start new chunk with overlap
            overlap_words = current_chunk[-overlap//2:] if current_chunk else []
            current_chunk = overlap_words + [word]
            current_length = sum(len(w) + 1 for w in current_chunk)

            # If a single word is larger than max_length, split it forcibly
            while len(word) > max_length:
                chunks.append(word[:max_length])  # Store first max_length chars
                word = word[max_length:]  # Keep the remaining part
                current_chunk = [word]  # Start a new chunk
                current_length = len(word) + 1

        else:
            current_chunk.append(word)
            current_length += word_length

    # Add the last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# Split markdown content into chunks of 512 characters
md_chunks = chunk_text(md_content)

# Print the number of chunks created for verification
print(f"Markdown content split into {len(md_chunks)} chunks.")
print("chunk 0", md_chunks[0])
print("chunk 1", md_chunks[1])

client = QdrantClient(url='http://localhost:6333')

# client.create_collection(
#     collection_name="pdf_data",
#     vectors_config=VectorParams(size=768, distance=Distance.DOT),
# )

md_chunks = md_chunks[:200]
for idx, chunk in enumerate(md_chunks):
    print("chunk length", len(chunk))
    # chunk = chunk[:512]
    
    response = ollama.embed(
        model='granite-embedding:278m',
        input=chunk
    )

    vector = response['embeddings'][0]
    print('VECTOR: ', vector[:10])
    # operation = client.upsert(
    #     collection_name='pdf_data',
    #     wait=True,
    #     points = [
    #         PointStruct(id=idx, vector=vector, payload={"text": chunk})
    #     ]
    # )
    # print(idx, " Upsert: ", operation)


