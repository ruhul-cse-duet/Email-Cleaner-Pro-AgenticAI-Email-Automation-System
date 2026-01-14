from fastapi import Request


def verify_api_key(request: Request) -> bool:
    return True
