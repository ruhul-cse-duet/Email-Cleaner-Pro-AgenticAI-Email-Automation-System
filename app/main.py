from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api.email_webhook import router as email_webhook_router
from app.api.admin import router as admin_router
from app.api.health import router as health_router
from app.utils.logger import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
setup_logging()


def create_app() -> FastAPI:
    app = FastAPI(
        title="EmailCleaner Pro",
        description="AI-powered email automation with agentic workflow",
        version="1.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health_router, tags=["health"])
    app.include_router(email_webhook_router, prefix="/api", tags=["email"])
    app.include_router(admin_router, prefix="/api/admin", tags=["admin"])
    
    return app


app = create_app()
