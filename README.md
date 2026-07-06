# Personalized Networking Assistant

AI-powered web application that generates smart, tailored conversation starters for professional/social networking events. Uses DistilBERT for theme extraction from event descriptions, GPT-2 for generating context-aware conversation prompts, and the Wikipedia API for fact-checking.

## Architecture

```
backend/             # FastAPI backend
  ├── main.py        # App entry point, startup/shutdown, CORS
  ├── database.py    # SQLAlchemy engine + session
  ├── models.py      # 6 ORM entities
  ├── schemas.py     # Pydantic request/response models
  ├── services/      # Business logic layer
  │   ├── event_analyzer.py   # DistilBERT zero-shot theme extraction
  │   ├── topic_generator.py  # GPT-2 conversation starter generation
  │   ├── fact_checker.py      # Wikipedia API integration
  │   ├── history_logger.py    # Session/starters persistence
  │   └── feedback_logger.py   # Thumbs up/down recording
  └── routes/        # FastAPI routers
      ├── sessions.py
      ├── starters.py
      ├── factcheck.py
      └── history.py
frontend/
  └── app.py         # Streamlit UI (4 screens)
tests/
  ├── conftest.py
  ├── test_event_analyzer.py
  ├── test_topic_generator.py
  ├── test_fact_checker.py
  └── test_routes.py
```

## Data Model (ER Diagram)

```
User Profile (1) ──< Networking Session (M) ──> (1) Event Context
                              │
                    ┌─────────┼─────────┐
                    │         │         │
               Generated   Wikipedia   Log Entry
               Starter     Fact Check

Entities:
- UserProfile: UserID (PK), BioText, currentEventCache
- EventContext: EventID (PK), EventDescription, AnalyzedThemes
- NetworkingSession: SessionID (PK), UserID (FK), EventID (FK), SessionTimestamp
- GeneratedStarter: StarterID (PK), SessionID (FK), StarterText, ContextPromptUsed, Feedback
- WikipediaFactCheck: FactCheckID (PK), SessionID (FK), VerifiedQueryText, VerificationStatus, WikipediaSourceURL
- LogEntry: LogID (PK), SessionID (FK, nullable), ActionType, PayloadJSON, Timestamp
```

## Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the backend** (Terminal 1):
   ```bash
   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Run the frontend** (Terminal 2):
   ```bash
   streamlit run frontend/app.py
   ```

5. Open the Streamlit URL (default: http://localhost:8501)

## Testing

```bash
pytest -v
```

To run specific test files:
```bash
pytest tests/test_event_analyzer.py -v
pytest tests/test_routes.py -v
```

## Usage

1. **Generate Starters** — Enter an event description + interests → get 3 AI-generated conversation starters with theme tags. Thumbs up/down each one.
2. **Fact Check** — Search any topic → get Wikipedia summary + source URL.
3. **History** — Browse all past sessions with their generated starters.
4. **Feedback History** — See all thumbs up/down ratings.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Root health check |
| GET | `/health` | Health check |
| POST | `/api/starters/generate` | Generate conversation starters |
| POST | `/api/starters/feedback` | Submit thumbs up/down |
| GET | `/api/starters/session/{id}` | Get starters for a session |
| GET | `/api/sessions/` | List all sessions |
| GET | `/api/sessions/{id}` | Get session details |
| GET | `/api/sessions/{id}/history` | Get session with starters |
| POST | `/api/factcheck/` | Verify a topic via Wikipedia |
| GET | `/api/factcheck/` | List all fact checks |
| GET | `/api/history/sessions` | Full session history |
| GET | `/api/history/feedback` | Feedback history |
| GET | `/api/history/logs` | Recent log entries |
