# expose-llm-api

Minimal FastAPI reverse proxy in front of a local `llama.cpp` server, protected by an API key.

## Usage

1. Drop a `.gguf` model file into `./models/` (update the filename in `docker-compose.yml` if it's not `model.gguf`). Make sure the model fits in your GPU's VRAM at your chosen quantization — if it doesn't, `llama-cpp` will fail to start with a CUDA out-of-memory error; lower `-ngl` in `docker-compose.yml` (fewer layers offloaded to GPU) or pick a smaller quant if that happens.
2. Copy the env file and set your own key:
   ```bash
   cp .env.example .env
   ```
3. Start everything:
   ```bash
   docker-compose up --build
   ```
4. Call it:
   ```bash
   curl http://localhost:8000/v1/chat/completions \
     -H "X-API-Key: change-me" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "local-model",
       "messages": [{"role": "user", "content": "Hello!"}]
     }'
   ```
