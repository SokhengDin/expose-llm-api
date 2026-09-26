import httpx
from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response

from app.config import settings

router = APIRouter()

_client = httpx.AsyncClient(base_url=settings.llama_server_url, timeout=settings.request_timeout)


async def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if x_api_key is None or x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Missing or invalid API key")


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.api_route(
    "/v1/{path:path}",
    methods=["GET", "POST"],
    dependencies=[Depends(verify_api_key)],
)
async def proxy(path: str, request: Request) -> Response:
    body = await request.body()
    try:
        upstream = await _client.request(
            request.method,
            f"/v1/{path}",
            content=body,
            params=request.query_params,
            headers={"content-type": request.headers.get("content-type", "application/json")},
        )
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="LLM backend unavailable")

    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        media_type=upstream.headers.get("content-type"),
    )
