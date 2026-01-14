import logging


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s")
import os
import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    """Configure logging for the application"""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format=log_format,
        handlers=[
            # Console handler
            logging.StreamHandler(),
            # File handler with rotation
            RotatingFileHandler(
                "logs/email_cleaner.log",
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
        ]
    )
    
    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
