from typing import List

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.util.auth_util import decode_token


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, allowed_paths: List[str]):
        super().__init__(app)
        self.allowed_paths = allowed_paths

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.allowed_paths:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid token"},
            )

        token = auth_header.split(" ")[1]
        try:
            payload = decode_token(token)
            request.state.user = payload["sub"]
        except Exception:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired token"},
            )

        response = await call_next(request)
        return response
