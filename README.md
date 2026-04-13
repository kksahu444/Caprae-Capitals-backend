# Caprae Capital: AI-Readiness Pre-Screening Challenge

Welcome to the **Caprae Capital Partners** Full Stack Developer Interview Pre-Work repository. This project is a submission for the Lead Generation Scraping Tool assessment (August 2025 Revised Handbook).

## Project Overview

This project enhances the core lead generation scraping capabilities, drawing inspiration from [SaaSQuatch Leads](https://www.saasquatchleads.com/) to build a robust, scalable, and intelligent scraping architecture. We chose to focus on **Quality First** mixed with **Technical Sophistication**, building a system capable of bypassing anti-bot measures, seamlessly discovering prospects via Google Maps, and persisting them intelligently in a database, ready for AI orchestration.

### Key Features

- **Google Maps Data Scraping**: Robust scraping utilizing **Crawlee** with Playwright, complete with advanced anti-bot measures (proxy rotation, custom user agent rotation, rate limiting, and CAPTCHA detection with exponential backoff).
- **Asynchronous FastAPI Backend**: Built on top of FastAPI to provide high-performance asynchronous endpoints for lead management, analytics, and triggering scraper tasks.
- **Celery Workflow Engine**: Background asynchronous task execution for long-running scrape operations, utilizing Redis as the message broker.
- **Intelligent Database Architecture**: Native dual-database support. It uses MongoDB internally via Motor (async for FastAPI) and PyMongo (sync for Celery tasks), featuring atomic operations (`$set`, `$setOnInsert`) to deduplicate businesses robustly. 
- **Modular and Clean Architecture**: Restructured for maximum maintainability. Separated concerns strictly across routers, asynchronous tasks, database models, parsers, and bots.

## Setup Instructions

### 1. Prerequisites
- Python 3.9+ (Tested with 3.14 compatible configurations)
- Redis Server (acting as Celery Broker)
- MongoDB Database

### 2. Environment Variables
Create a `.env` file in the root of the directory (see `.env.example`):
```env
REDIS_URL="redis://localhost:6379/0"
CELERY_BROKER_URL="redis://localhost:6379/0"
CELERY_RESULT_BACKEND="redis://localhost:6379/0"
MONGO_URI="mongodb+srv://..."
```

### 3. Installation
Install the core dependencies:
```bash
pip install -r requirements.txt
```

*(Note: Playwright and Selenium may require their own respective browser installations. e.g., `playwright install chromium` if you intend to run the Playwright scrapers).*

### 4. Running the Application

**Start the FastAPI Server:**
```bash
uvicorn app.main:app --port 9000 --reload
```
The API documentation will be available at `http://127.0.0.1:9000/docs`.

**Start the Celery Worker (In a separate terminal):**
```bash
celery -A app.celery_tasks.tasks worker --loglevel=info -P solo
```

## Challenge Requirements Addressed

- **Business Use Case Understanding**: Designed explicitly to serve high-impact data prioritizing contact extraction and integration-ready format structure.
- **Technical Sophistication**: Leverages Celery for background orchestration and Crawlee/Playwright for reliable data extraction against dynamic SPAs and anti-bot environments. Uses proper exponential backoff heuristics.
- **Scalability**: All blocking operations are pushed to Celery queues with rate-limiting applied. The core APIs are built exclusively utilizing asynchronous drivers.

## Repository Structure Overview
```
.
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── routers/             # API Endpoints (companies, analytics, scraper)
│   ├── celery_tasks/        # Background scraping and enrichment tasks
│   ├── crawlers/            # Advanced Crawlee-based spiders
│   ├── db_mongo.py          # MongoDB configuration and sync adapters
│   ├── db_motor.py          # Asynchronous MongoDB configuration
│   └── utils/               # Configuration and helper scripts
├── docs/                    # Extensive planning and architecture designs
├── requirements.txt         # Project dependencies
└── README.md                # This file
```
