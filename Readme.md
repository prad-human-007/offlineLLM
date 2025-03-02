
# Marker for creating embedding 

# Qdrant for running db on GPU
# `--gpus=all` flag says to Docker that we want to use GPUs.
# `-e QDRANT__GPU__INDEXING=1` flag says to Qdrant that we want to use GPUs for indexing.
docker run \
	--rm \
	--gpus=all \
	-p 6333:6333 \
	-p 6334:6334 \
	-e QDRANT__GPU__INDEXING=1 \
	qdrant/qdrant:gpu-nvidia-latest

# Ollama for Embedding model and LLM. 
ollama run qwen2.5

# FastAPI for quering the model 
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
# Vite Frontend
npm run dev