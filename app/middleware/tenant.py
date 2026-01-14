from fastapi import Request

from app.utils.config import settings


def get_tenant_id(request: Request) -> str | None:
    return request.headers.get(settings.tenant_header)
