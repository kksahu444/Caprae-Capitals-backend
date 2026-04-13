"""Celery configuration loaded from environment variables."""
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

broker_url = os.getenv("CELERY_BROKER_URL", f"{REDIS_URL}/0")
result_backend = os.getenv("CELERY_RESULT_BACKEND", f"{REDIS_URL}/1")
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True
