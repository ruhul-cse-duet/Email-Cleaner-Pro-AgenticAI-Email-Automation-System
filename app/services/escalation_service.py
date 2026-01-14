from app.schemas.email_schema import EmailInbound


class EscalationService:
    def notify_human(self, email: EmailInbound, summary: str) -> None:
        return None
