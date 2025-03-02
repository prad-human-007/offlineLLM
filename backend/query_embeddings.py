import ollama
from qdrant_client import QdrantClient

response = ollama.embed(
    model='granite-embedding:278m',
    input="list the contributors of the book"
)

vector = response['embeddings'][0]
print('Embeddings: ', vector[:10])

client = QdrantClient(url='http://localhost:6333')

search_result = client.query_points(
    collection_name='pdf_data',
    query=vector,
    with_payload=True,
    limit=5
).points


for result in search_result:
    print("Result : ", result.id)
    print("Result : ", result.payload)