from fastapi import Depends, Request
from app.core.settings import settings

from typing import Annotated


async def check_admin(req: Request) -> bool:
    if auth_header := req.headers.get("Authorization"):
        _, token = auth_header.split(' ')
        return token == settings.admin_token


AdminDep = Annotated[bool, Depends(check_admin)]
