import httpx
from fastapi import APIRouter, Request, Response

router = APIRouter()


@router.api_route(
    "/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"]
)
async def proxy(path: str, request: Request):
    url = f"https://httpbin.org/{path}"
    headers = dict(request.headers)
    data = await request.body()
    try:
        # remove the original `host` header
        headers.pop("host")
    except KeyError:
        pass
    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method, url, headers=headers, content=data
        )
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=response.headers,
    )
