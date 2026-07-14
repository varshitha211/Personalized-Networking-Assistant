# Phase 7: Project Documentation

This folder contains the technical documentation for the **Personalized Networking Assistant** project.

---

# 1. Project Summary

The Personalized Networking Assistant is an AI-powered web application that assists users in preparing for professional and social networking events. The application analyzes event descriptions, generates personalized conversation starters, verifies factual information, and maintains networking history for future reference.

The system combines modern AI models with a lightweight web architecture to provide an interactive networking assistant.

---

# 2. Project Features

The application provides the following features:

- AI-powered conversation starter generation
- Event theme extraction
- Fact checking using Wikipedia
- Networking session history
- Feedback collection
- REST API-based backend
- Interactive Streamlit user interface

---

# 3. System Architecture

The application consists of four major components:

- Streamlit Frontend
- FastAPI Backend
- AI Service Layer
- SQLite Database

The frontend communicates with the backend through REST APIs, while the backend processes requests using dedicated AI service modules and stores data using SQLAlchemy with SQLite.

---

# 4. Technologies Used

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Frontend | Streamlit |
| Database | SQLite |
| ORM | SQLAlchemy |
| AI Models | DistilBERT, GPT-2 |
| Fact Verification | Wikipedia API |
| Testing | PyTest |
| Version Control | Git & GitHub |

---

# 5. Project Modules

The application is divided into the following modules:

- Event Analyzer
- Topic Generator
- Fact Checker
- History Logger
- Feedback Logger

Each module performs a dedicated task and communicates with the backend through well-defined interfaces.

---

# 6. Folder Structure

```
backend/
frontend/
tests/
requirements.txt
README.md
```

---

# 7. Installation

### Install the required dependencies

```bash
pip install -r requirements.txt
```

### Start the backend server

```bash
python -m uvicorn backend.main:app --reload
```

### Launch the frontend

```bash
streamlit run frontend/app.py
```

---

# 8. Documentation Outcome

The project documentation provides a complete overview of the application architecture, implementation, technologies, modules, and deployment process. It serves as a reference for understanding, maintaining, and extending the Personalized Networking Assistant.
