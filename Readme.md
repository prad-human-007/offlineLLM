# Offline RAG inplementation with user Autentication 

## Tech Stack  
- **Vite, React, Tailwind** (Frontend)  
- **FastAPI, Python** (backend for LLM API and Auth)  
- **Qdrant** (GPU-accelerated vector database)  
- **Ollama** (Run Embedding model & LLM Locally)  

## Running Qdrant on GPU  
To run Qdrant with GPU support using Docker:  

```bash
docker run --rm --gpus=all \
    -p 6333:6333 -p 6334:6334 \
    -e QDRANT__GPU__INDEXING=1 \
    qdrant/qdrant:gpu-nvidia-latest
```

Put Embeddings Data in Qdrant.
 - ceo
 - manager
 - employee

## Running Ollama for Embeddings & LLM  
Start the embedding model and LLM with:  

```bash
ollama run qwen2.5
```

## Running FastAPI for Querying the Model  
Start the FastAPI backend:  

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

used Marker library in python for pdf parsing [Marker Github](https://github.com/VikParuchuri/marker)

## Running the Vite Frontend  
To start the frontend in development mode:  

```bash
npm run dev
```

