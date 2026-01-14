from app.db.session import SessionLocal
from app.db.crud import create_tenant


if __name__ == "__main__":
    db = SessionLocal()
    tenant = create_tenant(db, "default")
    print(f"Created tenant {tenant.id}")
