# Phase 8: Project Demonstration

This folder contains the demonstration details of the **Personalized Networking Assistant**.

---

# 1. Project Demonstration

The Personalized Networking Assistant is an AI-powered web application that helps users prepare for professional and social networking events by generating personalized conversation starters, analyzing event themes, verifying facts, and maintaining networking history.

The application demonstrates the integration of modern AI models with a web-based architecture to provide an intelligent networking assistant.

---

# 2. Demonstration Objectives

The project demonstration focuses on:

- Showcasing AI-powered conversation starter generation.
- Demonstrating event theme extraction.
- Performing fact verification using Wikipedia.
- Displaying networking session history.
- Recording and displaying user feedback.
- Illustrating communication between the Streamlit frontend and FastAPI backend.

---

# 3. Demonstration Workflow

### Step 1 – Launch the Application

- Start the FastAPI backend.
- Launch the Streamlit frontend.

---

### Step 2 – Generate Conversation Starters

- Enter an event description.
- Enter user interests.
- Generate personalized conversation starters.

---

### Step 3 – Analyze Event

- The Event Analyzer extracts important themes from the event description using DistilBERT.

---

### Step 4 – AI Response Generation

- GPT-2 generates context-aware conversation starters based on the extracted themes and user interests.

---

### Step 5 – Fact Verification

- Enter a query in the Fact Checker.
- The application retrieves factual information using the Wikipedia API.

---

### Step 6 – Session History

- View previously generated networking sessions stored in the SQLite database.

---

### Step 7 – Feedback

- Submit thumbs up/down feedback for generated conversation starters.
- Feedback is stored for future analysis.

---

# 4. Technologies Demonstrated

| Component | Technology |
|-----------|------------|
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | SQLite |
| ORM | SQLAlchemy |
| Theme Extraction | DistilBERT |
| Conversation Generation | GPT-2 |
| Fact Verification | Wikipedia API |
| Testing | PyTest |

---

# 5. Project Repository

The complete source code, documentation, backend services, frontend application, and test modules are maintained in the GitHub repository.

---

# 6. Demo Video

The project demonstration video showcases:

- Application setup
- Conversation starter generation
- Event analysis
- Fact checking
- Networking history
- Feedback functionality

**Demo Video Link:**

https://drive.google.com/file/d/1YZjIPuurGmB0mSq4IIHh1iiU-HYLxext/view?usp=sharing

---

# 7. Conclusion

The Personalized Networking Assistant successfully demonstrates how AI can assist users in professional networking by combining event analysis, conversation generation, fact verification, and networking history into a single web application. The project showcases the practical use of FastAPI, Streamlit, DistilBERT, GPT-2, SQLAlchemy, and SQLite to build an intelligent networking assistant.
