"""
FastAPI application entry point for the Lead Generation Backend.
"""
from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.celery_utils import create_celery
from app.routers import scraper, companies, analytics, company_detail, enrichment
from app.db_motor import init_motor, create_indexes_async, close_motor
import logging

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    current_app = FastAPI(
        title="Lead Generation Backend",
        description=(
            "Async FastAPI service for lead generation, scraping, "
            "enrichment, and analytics — backed by Celery workers and MongoDB."
        ),
        version="1.0.0",
    )

    # CORS middleware for frontend integration
    current_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Restrict in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    current_app.state.celery_app = create_celery()

    # Include routers
    current_app.include_router(scraper.router)
    current_app.include_router(companies.router)
    current_app.include_router(analytics.router)
    current_app.include_router(company_detail.router)
    current_app.include_router(enrichment.router, prefix="/api/v1")

    return current_app


app = create_app()
celery: Any = getattr(app.state, "celery_app")


@app.on_event("startup")
async def startup_event():
    """Initialize Motor (async MongoDB) and create indexes on startup."""
    try:
        logger.info("Initializing Motor (async MongoDB) for FastAPI...")
        init_motor()
        await create_indexes_async()
        logger.info("✅ Motor initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Motor: {e}")
        logger.warning("Company search endpoints may not work without MongoDB")


@app.on_event("shutdown")
async def shutdown_event():
    """Close Motor connection on shutdown."""
    try:
        await close_motor()
        logger.info("Motor connection closed")
    except Exception as e:
        logger.error(f"Error closing Motor: {e}")


if __name__ == "__main__":
    uvicorn.run("app.main:app", port=9000, reload=True)
