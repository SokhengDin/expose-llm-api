# expose-llm-api

Minimal FastAPI reverse proxy in front of a local `llama.cpp` server, protected by an API key.

## Usage

1. Drop a `.gguf` model file into `./models/` (update the filename in `docker-compose.yml` if it's not `model.gguf`).
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
