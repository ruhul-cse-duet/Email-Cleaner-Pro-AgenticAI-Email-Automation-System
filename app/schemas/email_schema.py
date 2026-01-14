from pydantic import BaseModel


class EmailInbound(BaseModel):
    subject: str
    body: str
    from_address: str | None = None
    to_address: str | None = None
