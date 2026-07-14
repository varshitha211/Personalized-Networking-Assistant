# Phase 5: Project Development

This folder contains the implementation details of the **Personalized Networking Assistant**.

---

# 1. Project Overview

The Personalized Networking Assistant is an AI-powered web application that helps users prepare for professional and social networking events by generating personalized conversation starters. The application extracts themes from event descriptions using DistilBERT, generates context-aware conversation starters using GPT-2, verifies information through the Wikipedia API, and stores networking sessions for future reference.

---

# 2. Project Structure

```
Personalized-Networking-Assistant

├── backend
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── services
│   │   ├── event_analyzer.py
│   │   ├── topic_generator.py
│   │   ├── fact_checker.py
│   │   ├── history_logger.py
│   │   └── feedback_logger.py
│   └── routes
│       ├── sessions.py
│       ├── starters.py
│       ├── factcheck.py
│       └── history.py
│
├── frontend
│   └── app.py
│
├── tests
│   ├── conftest.py
│   ├── test_event_analyzer.py
│   ├── test_topic_generator.py
│   ├── test_fact_checker.py
│   └── test_routes.py
│
├── requirements.txt
└── README.md
```

---

# 3. Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Backend development |
| FastAPI | REST API framework |
| Streamlit | Frontend application |
| SQLAlchemy | ORM for database operations |
| SQLite | Database |
| DistilBERT | Theme extraction |
| GPT-2 | Conversation starter generation |
| Wikipedia API | Fact verification |
| PyTest | Unit testing |
| Git & GitHub | Version control |

---

# 4. Core Modules

## Event Analyzer

Analyzes event descriptions using DistilBERT zero-shot classification to identify relevant themes.

---

## Topic Generator

Generates AI-powered conversation starters using GPT-2 based on extracted themes and user interests.

---

## Fact Checker

Uses the Wikipedia API to retrieve verified information and source URLs.

---

## History Logger

Stores networking sessions and generated conversation starters for future reference.

---

## Feedback Logger

Stores thumbs up/down feedback provided by users for generated conversation starters.

---

# 5. Frontend Features

The Streamlit application provides four major screens:

- Generate Starters
- Fact Check
- History
- Feedback History

The frontend communicates with the FastAPI backend using REST APIs.

---

# 6. Backend APIs

The backend exposes APIs for:

- Conversation starter generation
- Feedback submission
- Session management
- Fact checking
- History retrieval

---

# 7. Setup Instructions

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the backend

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### Start the frontend

```bash
streamlit run frontend/app.py
```

---

# 8. Testing

The project includes unit tests for:

- Event Analyzer
- Topic Generator
- Fact Checker
- API Routes

Run all tests using:

```bash
pytest -v
```

---

# 9. Application Workflow

1. User enters an event description and personal interests.
2. DistilBERT extracts event themes.
3. GPT-2 generates personalized conversation starters.
4. User views generated starters in Streamlit.
5. User can submit thumbs up/down feedback.
6. Sessions and feedback are stored in SQLite.
7. Users can review previous sessions and perform fact checking through the Wikipedia API.
