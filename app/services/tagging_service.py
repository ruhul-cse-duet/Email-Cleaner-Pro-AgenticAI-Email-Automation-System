from app.schemas.email_schema import EmailInbound


class TaggingService:
    def tag_and_archive(self, email: EmailInbound, tags: list[str]) -> None:
        return None
