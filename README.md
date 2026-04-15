# 🚀 Lead Intelligence Backend API
---

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg) ![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688.svg) ![Celery](https://img.shields.io/badge/Task_Queue-Celery-37814A.svg) ![MongoDB](https://img.shields.io/badge/Database-MongoDB-47A248.svg) ![Redis](https://img.shields.io/badge/Broker-Redis-DC382D.svg) ![Crawlee](https://img.shields.io/badge/Scraping-Crawlee-FF9900.svg)

## 📚 Table of Contents
- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [About the Backend](#-about-the-backend)
- [Project Architecture](#️-project-architecture)
- [Features & Methodology](#️-features--methodology)
- [Pipeline](#-pipeline)
- [How to Run](#-how-to-run)
- [Academic Value & Insights](#-academic-value--insights)
- [Future Work](#-future-work)
- [Authors](#-authors)

📌 Overview
This project is an **Academic Project** implementing the backend for a sophisticated Lead Generation Scraping Tool. Designed to integrate seamlessly with a frontend dashboard, this asynchronous FastAPI and Celery architecture drives the extraction, processing, and management of high-value prospects.

🧠 Problem Statement
Modern data collection systems struggle with long-running scraping tasks, which are often:
- Synchronously blocking and slow
- Vulnerable to anti-bot measures
- Lacking robust data deduplication
- Difficult to scale across multiple locations simultaneously

👉 **Our goal:**
Build an automated, high-performance distributed backend that handles headless Google Maps scraping tasks safely, resolves anti-bot challenges gracefully, and returns clean, structured data for front-end analysis.

📚 About the Backend
This backend acts as the engine for the lead intelligence system. It offloads heavy web-scraping and data processing workloads to background task workers, avoiding API latency and offering a highly responsive service.

🔍 Key Ideas
- Uses **FastAPI** for high-performance, asynchronous REST endpoints.
- Relies on **Celery + Redis** to handle long-running, blocking background tasks.
- Facilitates database deduplication using **MongoDB** with both sync and async drivers.
- Completely decoupled from the frontend, ensuring pure service-oriented architecture.

⚡ Why it matters
- Prevents API timeouts when scraping large maps regions.
- Ensures duplicate business data is merged rather than duplicated using atomic inserts.
- Provides a clean Swagger UI for testing routes and launching bots immediately.

🏗️ Project Architecture

```text
lead-intelligence-backend/
│
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── routers/             # API Endpoints (companies, analytics, scraper)
│   ├── celery_tasks/        # Background scraping and enrichment tasks
│   ├── crawlers/            # Advanced Crawlee-based spiders
│   ├── db_mongo.py          # MongoDB configuration and sync adapters
│   ├── db_motor.py          # Asynchronous MongoDB configuration
│   └── utils/               # Configuration and helper scripts
│
├── docs/                    # Extensive planning and architecture designs
├── requirements.txt         # Project dependencies
└── README.md                # This file
```

⚙️ Features & Methodology

1️⃣ Google Maps Data Scraping
Robust scraping utilizing **Crawlee** with Playwright, featuring advanced anti-bot capabilities:
- Proxy rotation & custom user agent rotation
- Exponential backoff
- Rate limiting and CAPTCHA handling

2️⃣ Asynchronous Task Orchestration
Instead of single-threaded blocking requests, tasks are dispatched through the Celery Workflow Engine, using Redis as the message broker.

3️⃣ Intelligent Database Layer
Native dual-database support via MongoDB. 
- Motor (Async) for instantaneous FastAPI API endpoints.
- PyMongo (Sync) for Celery workers executing atomic operations (`$set`, `$setOnInsert`) to deduplicate leads flawlessly.

4️⃣ Modular & Clean Architecture
Separated concerns strictly categorizing API routers, database adaptors, bots, background tasks, and general utilities for high maintainability.

📊 Pipeline
API Request from Frontend 
        → FastAPI Endpoint Validates Input 
        → Celery Task Dispatched to Redis Broker 
        → Celery Worker Starts Headless Scraper 
        → Dual-Database Insertion (MongoDB) 
        → Task ID Tracked & Checked by Frontend

🚀 How to Run

🔹 1. Prerequisites
- Python 3.9+
- Redis Server
- MongoDB Database

🔹 2. Configure environment settings
Create a `.env` file in the root of the project to configure backend secrets:
```env
REDIS_URL="redis://localhost:6379/0"
CELERY_BROKER_URL="redis://localhost:6379/0"
CELERY_RESULT_BACKEND="redis://localhost:6379/0"
MONGO_URI="mongodb+srv://<auth_details_here>"
```

🔹 3. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

🔹 4. Start the Application
Start the FastAPI API:
```bash
uvicorn app.main:app --port 9000 --reload
```
API Documentation will run at: **http://127.0.0.1:9000/docs**

Start the Celery Background Workers (in a new terminal):
```bash
celery -A app.celery_tasks.tasks worker --loglevel=info -P solo
```

🧠 Academic Value & Insights
- **Distributed Computing:** Practical implementation of asynchronous task queues (Celery/Redis) complementing an event-driven framework (FastAPI).
- **Concurrency & Parallelism:** Leveraging asyncio for fast IO bound networking alongside decoupled PyMongo synchronous inserts.
- **Data Integrity:** Ensuring atomic operations under high concurrency to guarantee absolute uniqueness across the lead database.

📌 Future Work
- Integration of WebSocket connections for real-time live-update scraping streams directly to the frontend.
- Proxied and customized browser fingerprint generation.
- Expanded platform support (Yelp, LinkedIn Scrapers).

🎓 Authors
- Krishnkant Sahu
