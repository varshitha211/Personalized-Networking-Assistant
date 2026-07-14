# Phase 3: Project Design

This folder contains the system architecture, data model, module design, and overall design of the **Personalized Networking Assistant**.

---

# 1. System Architecture

The Personalized Networking Assistant follows a modular architecture consisting of a Streamlit frontend, a FastAPI backend, AI service modules, and a SQLite database.

```
                    +----------------------+
                    |      Streamlit UI    |
                    |      frontend/app.py |
                    +----------+-----------+
                               |
                               |
                               v
                    +----------------------+
                    |     FastAPI Backend  |
                    |    backend/main.py   |
                    +----------+-----------+
                               |
        +-----------+----------+-----------+-----------+-----------+
        |           |                      |           |           |
        v           v                      v           v           v
Event Analyzer Topic Generator Fact Checker History Logger Feedback Logger
 (DistilBERT)       (GPT-2)      (Wikipedia)     (SQLite)      (SQLite)
                               |
                               |
                               v
                    +----------------------+
                    |      SQLite DB       |
                    |    SQLAlchemy ORM    |
                    +----------------------+
```

---

# 2. Backend Design

The backend is implemented using **FastAPI** and follows a layered architecture.

```
backend/

├── main.py
├── database.py
├── models.py
├── schemas.py
├── services/
│   ├── event_analyzer.py
│   ├── topic_generator.py
│   ├── fact_checker.py
│   ├── history_logger.py
│   └── feedback_logger.py
└── routes/
    ├── sessions.py
    ├── starters.py
    ├── factcheck.py
    └── history.py
```

---

# 3. Frontend Design

The frontend is developed using **Streamlit**.

The application provides four major screens:

- Generate Starters
- Fact Check
- History
- Feedback History

The frontend communicates with the FastAPI backend through REST API endpoints.

---

# 4. AI Module Design

## Event Analyzer

Uses **DistilBERT** zero-shot classification to extract themes from the event description.

---

## Topic Generator

Uses **GPT-2** to generate context-aware networking conversation starters based on the extracted themes and user interests.

---

## Fact Checker

Uses the **Wikipedia API** to verify user queries and return summarized factual information.

---

## History Logger

Stores networking sessions and generated conversation starters in the SQLite database.

---

## Feedback Logger

Stores user feedback (thumbs up/down) for generated conversation starters.

---

# 5. Database Design

The application uses **SQLite** with **SQLAlchemy ORM**.

### Database Entities

- UserProfile
- EventContext
- NetworkingSession
- GeneratedStarter
- WikipediaFactCheck
- LogEntry

---

# 6. Entity Relationship

```
User Profile (1)
        |
        |
        |------< Networking Session (M) >------ Event Context
                      |
          -----------------------------
          |            |             |
          |            |             |
Generated Starter  Wikipedia Fact Check  Log Entry
```

---

# 7. API Design

The backend exposes REST APIs for:

- Conversation Starter Generation
- Feedback Submission
- Session Management
- Fact Checking
- History Retrieval

These APIs enable seamless communication between the Streamlit frontend and FastAPI backend.

---

# 8. Design Advantages

- Modular architecture
- Separation of frontend and backend
- AI services isolated into independent modules
- Easy maintenance and scalability
- Efficient database management using SQLAlchemy
- REST-based communication between components
