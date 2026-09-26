import secrets

import httpx
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse

from app.config import settings

router = APIRouter()

_client = httpx.AsyncClient(
    base_url=settings.llama_server_url,
    timeout=settings.request_timeout,
    limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
)


async def aclose_client() -> None:
    await _client.aclose()


async def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if x_api_key is None or not secrets.compare_digest(x_api_key, settings.api_key):
        raise HTTPException(status_code=401, detail="Missing or invalid API key")


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.api_route(
    "/v1/{path:path}",
    methods=["GET", "POST"],
    dependencies=[Depends(verify_api_key)],
)
async def proxy(path: str, request: Request) -> StreamingResponse:
    upstream_request = _client.build_request(
        request.method,
        f"/v1/{path}",
        content=request.stream(),
        params=request.query_params,
        headers={"content-type": request.headers.get("content-type", "application/json")},
    )
    try:
        upstream = await _client.send(upstream_request, stream=True)
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="LLM backend unavailable")

    return StreamingResponse(
        upstream.aiter_raw(),
        status_code=upstream.status_code,
        media_type=upstream.headers.get("content-type"),
        background=BackgroundTask(upstream.aclose),
    )
