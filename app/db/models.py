from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True)
    subject = Column(String(500))
    body = Column(Text)
    intent = Column(String(100))
    action = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
