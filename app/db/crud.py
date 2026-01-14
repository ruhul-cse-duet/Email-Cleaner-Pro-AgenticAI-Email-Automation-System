from sqlalchemy.orm import Session

from app.db import models


def create_tenant(db: Session, name: str) -> models.Tenant:
    tenant = models.Tenant(name=name)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant
