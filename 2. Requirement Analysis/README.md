# Phase 2: Requirement Analysis

This folder contains the requirement analysis, technology selection, system requirements, and workflow for the **Personalized Networking Assistant**.

---

# 1. Project Overview

The Personalized Networking Assistant is an AI-powered web application that generates personalized conversation starters for professional and social networking events. The system analyzes event descriptions using DistilBERT, generates context-aware conversation starters using GPT-2, verifies information through the Wikipedia API, and stores networking sessions for future reference.

---

# 2. Technology Stack

The following technologies were selected for developing the application.

| Technology | Purpose |
|------------|---------|
| **Python** | Backend programming language |
| **FastAPI** | REST API development |
| **Streamlit** | Frontend user interface |
| **SQLAlchemy** | Database ORM |
| **SQLite** | Local database storage |
| **DistilBERT** | Event theme extraction |
| **GPT-2** | AI conversation starter generation |
| **Wikipedia API** | Fact verification |
| **PyTest** | Unit testing |
| **Git & GitHub** | Version control |

---

# 3. Functional Requirements

The system shall provide the following functionalities:

- Generate personalized conversation starters.
- Analyze networking event descriptions.
- Verify facts using Wikipedia.
- Store networking sessions.
- Record user feedback.
- Display previous networking history.
- Expose REST APIs for frontend communication.

---

# 4. Non-Functional Requirements

### Performance

- Generate AI responses efficiently.
- Support smooth interaction between frontend and backend.

### Reliability

- Store networking history consistently.
- Maintain accurate fact-checking results.

### Security

- Secure API communication.
- Maintain database integrity.

### Scalability

- Support additional AI models and future enhancements.

### Usability

- Provide a simple Streamlit interface.
- Easy navigation across application screens.

---

# 5. System Workflow

1. User enters an event description and personal interests.
2. DistilBERT extracts themes from the event description.
3. GPT-2 generates personalized conversation starters.
4. Generated starters are displayed in the Streamlit interface.
5. Users provide thumbs up/down feedback.
6. Sessions and feedback are stored in SQLite.
7. Users can review previous sessions and perform fact checking through the Wikipedia API.

---

# 6. Software Requirements

- Python
- FastAPI
- Streamlit
- SQLAlchemy
- SQLite
- DistilBERT
- GPT-2
- Wikipedia API
- PyTest
- Git
- GitHub

---

# 7. Hardware Requirements

## Minimum

- Intel Core i3 Processor
- 4 GB RAM
- 10 GB Free Storage
- Internet Connection

## Recommended

- Intel Core i5 or above
- 8 GB RAM
- SSD Storage
- Stable Internet Connection

---

# 8. Expected Outcome

The Personalized Networking Assistant enables users to prepare for networking events by generating context-aware conversation starters, verifying information through Wikipedia, storing networking sessions, and collecting feedback for continuous improvement.
