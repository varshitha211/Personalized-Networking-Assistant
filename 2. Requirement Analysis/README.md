# Phase 2: Requirement Analysis

This folder contains the requirement analysis, technology stack selection, customer journey mapping, and system requirements for the **Personalized Networking Assistant – AI-Powered Professional Networking Platform**.

---

# 1. Technology Stack

The following technologies were selected for developing the Personalized Networking Assistant based on scalability, ease of development, and AI integration capabilities.

| Technology | Purpose |
|------------|---------|
| **HTML5** | Structure and layout of web pages |
| **CSS3** | Responsive styling and user interface |
| **JavaScript** | Client-side interactivity |
| **Python** | Backend programming language |
| **Flask** | Web framework for handling requests and routing |
| **SQLite** | Database for storing user information, interaction history, and feedback |
| **Git & GitHub** | Version control and project collaboration |

---

# 2. Customer Journey Map

The following customer journey illustrates how a typical user interacts with the application.

| Stage | User Activity | System Response |
|-------|---------------|----------------|
| Discover | User visits the platform | Home page is displayed |
| Register/Login | User creates an account or logs in | User authentication is completed |
| Profile Setup | User enters interests and career preferences | User profile is stored |
| AI Assistance | User requests networking recommendations | AI generates personalized conversation topics and suggestions |
| Event Analysis | User explores networking events | Relevant events are displayed |
| Fact Verification | User verifies information | Fact Checker returns validated results |
| History | User reviews previous interactions | Networking history is retrieved |
| Feedback | User submits feedback | Feedback is stored for future improvements |

---

# 3. Functional Requirements

The system shall allow users to:

- Register and log in securely.
- Create and update professional profiles.
- Generate AI-powered networking conversation topics.
- Analyze networking events.
- Verify information using the Fact Checker.
- Store networking interaction history.
- Submit feedback for continuous improvement.

---

# 4. Non-Functional Requirements

### Performance
- Generate responses with minimal delay.
- Handle multiple user requests efficiently.

### Reliability
- Ensure consistent AI recommendations.
- Maintain accurate user records.

### Security
- Secure user authentication.
- Protect sensitive user information.

### Usability
- Provide a simple and intuitive user interface.
- Ensure easy navigation across all modules.

### Scalability
- Support future feature additions and increased user traffic.

---

# 5. System Modules

The application consists of the following major modules:

- User Authentication
- Profile Management
- Topic Generator
- Event Analyzer
- Fact Checker
- History Logger
- Feedback Logger

---

# 6. Data Flow

```
User
   │
   ▼
Frontend Interface
   │
   ▼
Flask Backend
   │
   ├──────────────┐
   ▼              ▼
AI Modules     SQLite Database
   │              │
   └──────┬───────┘
          ▼
 Generated Response
          ▼
       User Interface
```

---

# 7. Expected Outcome

The Personalized Networking Assistant aims to simplify professional networking by providing AI-powered recommendations, personalized conversation support, networking event analysis, fact verification, and interaction history management. The system enables users to build stronger professional relationships while improving networking efficiency and confidence.
