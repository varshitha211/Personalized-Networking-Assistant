# Phase 4: Project Planning

This folder contains the project planning, implementation strategy, module breakdown, and development milestones for the **Personalized Networking Assistant**.

---

# 1. Project Objective

The objective of this project is to develop an AI-powered web application that assists users in professional and social networking by generating personalized conversation starters based on event descriptions and user interests. The application also provides fact-checking, networking session history, and feedback tracking through an intuitive web interface.

---

# 2. Development Methodology

The project was developed using a modular approach, where each major functionality was implemented as an independent service. This improves maintainability, scalability, and testing.

The development process included:

- Requirement Analysis
- System Design
- Backend Development
- Frontend Development
- AI Model Integration
- Database Integration
- Testing
- Documentation

---

# 3. Project Modules

## Backend

Developed using **FastAPI**.

Major components include:

- API Routing
- Database Configuration
- ORM Models
- Request & Response Schemas
- Business Logic Services

---

## AI Services

The AI layer consists of five independent services.

### Event Analyzer

- Extracts event themes using DistilBERT.

### Topic Generator

- Generates personalized conversation starters using GPT-2.

### Fact Checker

- Retrieves factual information using the Wikipedia API.

### History Logger

- Stores networking sessions and generated conversation starters.

### Feedback Logger

- Records user feedback for generated responses.

---

## Frontend

Developed using **Streamlit**.

Provides four major interfaces:

- Generate Starters
- Fact Check
- History
- Feedback History

---

## Database

Implemented using:

- SQLite
- SQLAlchemy ORM

The database stores:

- User Profiles
- Event Contexts
- Networking Sessions
- Generated Starters
- Fact Check Records
- Log Entries

---

# 4. Development Timeline

The project development was carried out in the following sequence:

1. Requirement Analysis
2. Architecture Design
3. Database Design
4. Backend API Development
5. AI Model Integration
6. Frontend Development
7. Testing
8. Documentation

---

# 5. Implementation Plan

The implementation followed these steps:

- Configure FastAPI backend.
- Create SQLite database using SQLAlchemy.
- Develop REST API endpoints.
- Integrate DistilBERT for event analysis.
- Integrate GPT-2 for conversation generation.
- Integrate Wikipedia API for fact checking.
- Develop Streamlit frontend.
- Connect frontend with backend APIs.
- Perform testing using PyTest.

---

# 6. Deliverables

The completed project includes:

- FastAPI Backend
- Streamlit Frontend
- SQLite Database
- AI-based Event Analyzer
- AI Conversation Starter Generator
- Wikipedia Fact Checker
- Networking History Module
- Feedback Management Module
- REST APIs
- Unit Tests
- Project Documentation

---

# 7. Expected Outcome

The Personalized Networking Assistant enables users to prepare for networking events more effectively by generating intelligent conversation starters, verifying information through Wikipedia, maintaining networking history, and providing a seamless AI-assisted networking experience.
