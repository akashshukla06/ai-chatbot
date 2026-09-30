# PROJECT SYNOPSIS

---

## 1. Cover Page

* **Project Title:** ABES Student Support AI Portal
* **Student Name:** Akash Shukla
* **Roll Number / Student ID:** AK0001
* **Branch / Department:** Department of Computer Science and Engineering
* **Semester & Section:** 5th Semester (3rd Year) / Section: CSE-12
* **College Name:** ABES Engineering College, Ghaziabad
* **Project Guide Name:** [Faculty Guide Name / Department Mentor]
* **Academic Year:** 2026 – 2027

---

## 2. Project Title

**ABES Student Support AI Portal**  
*(An Intelligent Student Academic ERP Assistant with Semantic Retrieval and Live Database Integration)*

---

## 3. Introduction

In technical colleges like ABES Engineering College, students face daily difficulties in tracking their academic records and accessing official institutional information. Core academic details such as subject-wise attendance percentages, registered course lists, upcoming internal examinations (Pre-University Examinations - PUE), and college notices are typically scattered across physical notice boards, separate ERP portals, and periodic PDF circulars.

The **ABES Student Support AI Portal** is a unified web-based application developed during a 4-day B.Tech 3rd-year mini project. It integrates live student academic enterprise resource data from a **MySQL** database with a local natural language processing (NLP) model powered by **Hugging Face Sentence Transformers (`all-MiniLM-L6-v2`)**. The portal provides students with an interactive dashboard to monitor their attendance and exam dates in real time, while offering an integrated AI chatbot that delivers verified answers to college-related queries with zero hallucination.

---

## 4. Problem Statement

Students and college administrators at technical institutions face multiple operational inefficiencies:
1. **Scattered Academic Data:** Students lack a single responsive portal where they can check their subject-wise attendance, registered subjects, and exam schedules simultaneously.
2. **Repetitive Administrative Overhead:** Administrative desks, faculty mentors, and departmental coordinators spend significant daily hours manually addressing repetitive student queries regarding fee structures, placement statistics, and hostel regulations.
3. **Factual Hallucinations in Public AI:** Standard public conversational tools (such as standalone ChatGPT) have no secure access to real-time institutional databases or official college circulars, leading to incorrect or fabricated responses when queried by students.

---

## 5. Objectives

* **To develop a simple and user-friendly web portal** for ABES students to access their academic telemetry and college guidelines.
* **To automate the existing manual query process** for institutional information such as fees, courses, placements, and hostel facilities.
* **To reduce manual effort and errors** by eliminating factual AI hallucinations through direct SQL queries for student data and verified knowledge base retrieval for college policies.
* **To store and manage academic data efficiently** in an ACID-compliant MySQL database with secure Bcrypt password encryption and JSON Web Token (JWT) authentication.
* **To generate useful reports and dashboard cards** displaying live subject-wise attendance calculations, threshold alerts for the mandatory 75% AKTU attendance rule, and upcoming exam schedules.

---

## 6. Proposed Solution

The proposed project solves the identified problems through a centralized client-server web architecture featuring a dual-pipeline query router:
* **Personalized Student Dashboard:** After logging in with their Student ID (`AK0001`) and password, students access an interactive single-page dashboard featuring live cards for Attendance, Registered Subjects, Examination Schedule, and Official Notices.
* **Dual-Pipeline AI Chatbot:** An intelligent query handler embedded in the dashboard automatically categorizes incoming queries:
  * **Personal Academic Queries:** Questions like *"What is my attendance?"* or *"When is my DAA exam?"* trigger secure, parameterized SQL queries that fetch the authenticated student's real records directly from MySQL.
  * **Institutional Information Queries:** Questions like *"What is the fee structure for B.Tech?"* or *"What is the highest placement package?"* are processed through the `all-MiniLM-L6-v2` semantic vector search engine over verified college FAQs.
* **Target Users:** ABES Engineering College undergraduate students, faculty mentors, and portal administrators.
* **Expected Benefits:** Instantaneous query resolution in under 200 ms, zero fabricated data, 100% verified source citations, and reduced front-desk administrative load.

---

## 7. Scope of the Project

### Items Inside Current Scope:
* **User Authentication:** Role-based authentication (Student and Admin) with Bcrypt password hashing and JWT token management.
* **Academic Telemetry:** Tracking subject-wise attendance for 5th-semester CSE subjects (DBMS, Compiler Design, DAA, Data Analytics, DBMS Lab), overall percentage calculation, and 75% eligibility warning indicators.
* **Examination Management:** Display of upcoming PUE exam dates, reporting times, and allocated exam halls.
* **Semantic Knowledge Retrieval:** Vector-based search over 40+ official ABES FAQs covering branch intake, tuition fees, placement records, anti-ragging policies, and scholarships.
* **Bilingual Support:** Handling student inquiries in standard English as well as conversational Hinglish phrasing.

### Items Outside Current Scope:
* Online payment gateway integration for semester fee submission.
* Real-time automated biometric / facial recognition attendance scanning.
* Native mobile applications for iOS and Android devices.

---

## 8. Methodology / Working

The project workflow follows a structured four-stage processing pipeline:

```
[INPUT]  ➔  [PROCESSING]  ➔  [DATABASE / MODEL]  ➔  [OUTPUT]
```

### Detailed Workflow:
1. **INPUT:** The user enters credentials on the login screen or submits a natural language question via the dashboard chat window.
2. **PROCESSING:**
   * The FastAPI backend validates authentication headers using signed JWT tokens.
   * The query router inspects the question for personal keywords (*my attendance*, *mera exam*, *my subjects*).
3. **DATABASE / MODEL RETRIEVAL:**
   * **Path A (Live Database):** For personal student queries, parameterized SQL executes against MySQL:
     $$\text{Attendance \%} = \left(\frac{\text{Attended Classes}}{\text{Total Held Classes}}\right) \times 100$$
   * **Path B (Semantic Search):** For general queries, the input string is converted into a 384-dimensional dense vector using `all-MiniLM-L6-v2`, and **Cosine Similarity** is computed against the verified knowledge base:
     $$\text{Cosine Similarity} = \frac{\vec{A} \cdot \vec{B}}{\|\vec{A}\| \|\vec{B}\|}$$
     If similarity score $\ge 0.40$, the verified official response is retrieved. For complex general queries, the system uses Google Gemini with grounded prompt templates.
4. **OUTPUT:** Structured JSON responses are returned to the client and rendered dynamically on the web dashboard without requiring a page reload.

---

## 9. Technologies Used

| Category | Technology |
| :--- | :--- |
| **Programming Language** | Python 3.11+ |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla ES6) |
| **Backend** | FastAPI (ASGI Framework) with Uvicorn Server |
| **Database** | MySQL 8.0 (PyMySQL Connector) |
| **Machine Learning / NLP** | Sentence-Transformers (`all-MiniLM-L6-v2`), PyTorch, Scikit-learn |
| **LLM Integration** | Google GenAI SDK (Gemini 2.5 Flash) |
| **Security & Auth** | Bcrypt (Password Hashing) & PyJWT (Token Authentication) |
| **IDE** | Visual Studio Code |
| **Version Control** | Git & GitHub |

---

## 10. Modules

### Module 1 – Authentication / User Management (`backend/auth.py`)
Handles student and administrator sign-in, verifies salted Bcrypt password hashes against database records, and generates cryptographically signed JWT access tokens with role-based access control.

### Module 2 – Data Management (`backend/database.py`)
Manages MySQL connection pooling and maintains relational schema tables including `students`, `subjects`, `student_subjects`, `attendance`, `exams`, `notices`, and `chat_history` with foreign-key referential integrity.

### Module 3 – Main Processing / Core Functionality (`backend/main.py`)
Provides RESTful API endpoints (`/student/profile`, `/student/attendance`, `/student/exams`, `/student/notices`, `/chat`) to serve live academic metrics and process user inquiries asynchronously.

### Module 4 – Prediction / Analysis / Semantic Search (`backend/chatbot_service.py`)
Encodes questions into 384-dimensional dense vector embeddings, performs cosine similarity matching over pre-computed knowledge base arrays (`.npy`), normalizes bilingual Hinglish queries, and routes student-specific intents to live SQL handlers.

### Module 5 – Reports / Dashboard (`frontend/dashboard.html`, `dashboard.js`)
Renders an interactive student portal featuring academic stat cards, modal dialogues for detailed subject attendance breakdowns, exam timetables with countdown indicators, and an embedded conversational assistant.

---

## 11. Expected Outcome

* **Instant Academic Visibility:** Students can retrieve their live 5th-semester attendance status and PUE examination timetables in less than 200 ms.
* **Elimination of Hallucinations:** Because personal academic metrics are fetched directly from MySQL tables, zero false information is produced.
* **Automated Inquiry Handling:** High-frequency student inquiries regarding fee structures, placement records, and campus facilities are resolved automatically 24x7.
* **Cryptographic Data Protection:** Passwords are fully protected against database extraction using one-way salted Bcrypt hashing.

---

## 12. Future Scope

1. **Mobile Application:** Developing dedicated cross-platform mobile apps using Flutter or React Native.
2. **Automated Notifications:** Integrating automated SMS and WhatsApp alerts for attendance shortages below the 75% AKTU threshold.
3. **Cloud Deployment:** Deploying the FastAPI application and MySQL database to AWS / Google Cloud Platform for multi-college scalability.
4. **Advanced Predictive Analytics:** Applying machine learning regression models to predict semester end-term marks based on continuous internal evaluation (CIE) and attendance trends.
5. **Voice-Enabled Assistant:** Adding real-time speech-to-text and voice responses using Web Speech APIs.

---

## 13. References

1. **FastAPI Official Documentation:** Tiangolo, S., *FastAPI Web Framework*, https://fastapi.tiangolo.com/
2. **Sentence-BERT Research Paper:** Reimers, N., & Gurevych, I. (2019), *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*, EMNLP-IJCNLP. https://arxiv.org/abs/1908.10084
3. **Bcrypt Password Cryptography:** Provos, N., & Mazières, D. (1999), *A Future-Adaptable Password Scheme*, USENIX Annual Technical Conference.
4. **JSON Web Token Specification (RFC 7519):** Internet Engineering Task Force (IETF), https://datatracker.ietf.org/doc/html/rfc7519
5. **AKTU B.Tech Academic Ordinances:** Dr. A.P.J. Abdul Kalam Technical University, Lucknow, https://aktu.ac.in/
6. **ABES Engineering College Official Portal:** Admissions, Courses, and Placement Statistics, https://www.abes.ac.in/

---

## Final Synopsis Checklist

* [x] Cover Page
* [x] Project Title
* [x] Introduction
* [x] Problem Statement
* [x] Objectives (5 project-specific points)
* [x] Proposed Solution
* [x] Scope (In-scope and Out-of-scope)
* [x] Methodology / Working (INPUT ➔ PROCESSING ➔ DATABASE/MODEL ➔ OUTPUT)
* [x] Technologies Used (Formatted Category Table)
* [x] Modules (Modules 1 to 5 mapped to actual codebase files)
* [x] Expected Outcome
* [x] Future Scope (5 concrete points)
* [x] References (6 official citations)
