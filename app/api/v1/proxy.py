import aiohttp
from fastapi import APIRouter, Request, Response

router = APIRouter()

async_client = aiohttp.ClientSession()


@router.api_route(
    "/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"]
)
async def proxy(path: str, request: Request):
    url = f"http://localhost:8080/{path}"
    headers = dict(request.headers)
    data = await request.body()
    try:
        # remove the original `host` header
        headers.pop("host")
    except KeyError:
        pass
    async with async_client.request(
        request.method, url, headers=headers, data=data
    ) as response:
        return Response(
            content=await response.content.read(),
            status_code=response.status,
            headers=response.headers,
        )
