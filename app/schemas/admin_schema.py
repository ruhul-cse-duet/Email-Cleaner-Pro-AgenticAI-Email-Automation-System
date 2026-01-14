from pydantic import BaseModel


class AdminStats(BaseModel):
    processed: int
    auto_replies: int
    tagged: int
    escalations: int
