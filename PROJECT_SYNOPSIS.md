# PROJECT SYNOPSIS
## B.Tech 3rd Year Mini Project

---

### 1. COVER PAGE DETAILS

* **Project Title:** ABES Student Support AI Portal (AI-Powered Student Academic ERP & Knowledge Assistant)
* **Student Name:** Akash Shukla
* **Student ID / Roll No:** AK0001
* **Department:** Department of Computer Science and Engineering
* **Semester / Section:** 5th Semester (3rd Year) / Section: CSE-12
* **Institution:** ABES Engineering College, Ghaziabad (UP)
* **Affiliated University:** Dr. A.P.J. Abdul Kalam Technical University (AKTU), Lucknow
* **Project Guide:** [Faculty Guide Name / Department Coordinator]
* **Academic Year:** 2026 – 2027

---

### 2. PROJECT TITLE
**ABES Student Support AI Portal: An Intelligent Academic ERP Assistant with Semantic Retrieval and Live Data Integration**

---

### 3. INTRODUCTION
In modern educational institutions, academic administrative operations and student query resolution are traditionally handled through separate, fragmented platforms. Students frequently navigate clunky ERP portals, PDF circulars, and departmental notice boards to access basic academic necessities such as subject-wise attendance, examination timetables, and college guidelines. Existing institutional chatbots are typically rule-based keyword matchers or generic large language models (LLMs) that lack access to real-time institutional data and often suffer from factual hallucinations.

The **ABES Student Support AI Portal** is designed to address this challenge by integrating institutional enterprise resource data with modern natural language processing (NLP). The portal combines a relational database containing live student academic records with a local semantic search engine based on Sentence Transformers (`all-MiniLM-L6-v2`) and large language models (Google Gemini). This hybrid system provides students with a single, unified interface for real-time academic tracking and instant, verified query resolution.

---

### 4. PROBLEM STATEMENT
Students at technical institutions face multiple operational hurdles in obtaining immediate and accurate academic information:
1. **Fragmented Academic Information:** Attendance records, internal examination schedules, syllabus details, and administrative notices are scattered across disconnected systems and notice boards.
2. **High Administrative Workload:** College administrative offices, heads of departments (HODs), and faculty mentors spend substantial time addressing repetitive queries regarding fee schedules, attendance criteria, and exam timetables.
3. **Inaccuracy and Hallucination in Generic AI:** Public conversational models (such as standalone ChatGPT) lack real-time access to private institutional databases and college-specific policies, leading to incorrect or fabricated responses.

There is a critical need for an automated, secure, and authenticated student support system that delivers 100% verified, zero-hallucination institutional data alongside contextual AI capabilities.

---

### 5. OBJECTIVES
The primary objectives of the project are:
* **To Develop an Authenticated Student Portal:** Provide secure, role-based access for students and administrators using industry-standard Bcrypt password hashing and JSON Web Tokens (JWT).
* **To Provide Real-Time Academic Tracking:** Deliver live subject-wise attendance percentages, upcoming examination schedules (Pre-University Exams - PUE), and academic notices from an ACID-compliant relational database.
* **To Implement Semantic Natural Language Processing:** Deploy a local sentence transformer model (`all-MiniLM-L6-v2`) capable of understanding student intent and phrasing in both English and Hinglish without relying on rigid keyword matching.
* **To Eliminate AI Hallucinations via Deterministic SQL Routing:** Build an intelligent decision router that isolates personal student queries and resolves them via parameterized SQL queries while directing college policy questions to verified knowledge datasets.
* **To Create a Lightweight and Responsive User Interface:** Design an intuitive web dashboard using vanilla HTML5, CSS3, and JavaScript that operates without heavy frontend dependencies or rendering lag.

---

### 6. PROPOSED SOLUTION
The proposed solution is a client-server web application featuring a dual-pipeline query architecture:
1. **Unified Dashboard:** A single-page student dashboard displaying real-time academic cards (Attendance, Enrolled Subjects, Upcoming Exams, and Official Circulars) alongside an interactive AI chat assistant.
2. **Bcrypt & JWT Security:** User credentials are encrypted using one-way salted hashing, and authenticated sessions are maintained via signed bearer tokens, ensuring complete student data privacy.
3. **Dual-Pipeline Query Routing:**
   * **Personal Data Pipeline:** When a student inquires about personal academic status (e.g., *"What is my attendance?"* or *"When is my DAA exam?"*), the backend extracts the student ID from the authenticated token and queries live MySQL tables directly, returning 100% accurate, factual numbers.
   * **Institutional Knowledge Pipeline:** When a general institutional question is received (e.g., *"What is the fee structure?"* or *"What is the highest placement package?"*), the query is transformed into a 384-dimensional dense vector and compared against pre-computed embeddings of verified college policies using Cosine Similarity.
4. **Verified Source Attribution:** Every response generated by the assistant includes an official source badge (e.g., *ABES Academic ERP*, *Official Placement Cell*, or *AKTU Circulars*), ensuring complete transparency.

---

### 7. SCOPE OF THE PROJECT

#### In-Scope Features:
* **User Authentication:** Secure login for students (using Student ID e.g., `AK0001`) and administrators with hashed credentials and token validation.
* **Student Academic Records:** Subject-wise class attendance tracking, calculation of aggregate attendance percentages, and notification of the mandatory 75% AKTU threshold.
* **Examination Management:** Display of upcoming internal/PUE exam dates, reporting times, and examination hall allocations.
* **Knowledge Retrieval Engine:** Semantic vector similarity matching over college-specific FAQs covering admissions, branch intake, tuition fees, hostel facilities, placements, and anti-ragging policies.
* **Bilingual Query Handling:** Support for standard English and conversational Hinglish queries (e.g., *"mera exam kab hai"* or *"fees kitni hai"*).
* **Administrative Data Seeding:** Structured MySQL schema provisioning and database seeding for students, subjects, exams, and notices.

#### Out-of-Scope (Current Version):
* Online fee payment gateway integration.
* Automated real-time optical face recognition attendance scanning.
* Native iOS / Android mobile application packaging (planned for future phases).

---

### 8. METHODOLOGY / WORKING

The system operates across four primary stages:

```
[Student Input] ➔ [Authentication & Intent Routing] ➔ [Database / Vector Engine] ➔ [Structured UI Output]
```

#### Detailed Workflow:
1. **User Input & Request Dispatch:** The student enters credentials on the login screen or submits a natural language question via the dashboard chat interface. The client issues an asynchronous HTTP request (`fetch`) with the JWT bearer token.
2. **Security & Session Verification:** The FastAPI backend inspects the `Authorization` header, decodes the signed JWT, and verifies the identity and role of the student.
3. **Intent Classification & Processing:**
   * **Branch A (Personal Intent):** The request matches personal intents (attendance, exams, subjects). The system triggers parameterized SQL statements against MySQL:
     $$\text{Attendance \%} = \left(\frac{\sum \text{Attended Classes}}{\sum \text{Total Classes}}\right) \times 100$$
   * **Branch B (Institutional Intent):** The request matches general institutional queries. The query string is passed to `all-MiniLM-L6-v2`, which computes a 384-dimensional dense embedding vector $\vec{q}$.
4. **Vector Similarity Computation:** The query vector $\vec{q}$ is evaluated against pre-computed knowledge base embedding vectors $\vec{d}_i$ using Cosine Similarity:
   $$\text{Cosine Similarity}(\vec{q}, \vec{d}_i) = \frac{\vec{q} \cdot \vec{d}_i}{\|\vec{q}\| \|\vec{d}_i\|}$$
   If $\text{Similarity} \ge 0.40$, the verified official institutional record is retrieved. If similarity is low, the request is forwarded to Google Gemini with strict context grounding.
5. **Response Generation & UI Rendering:** The backend serializes the structured JSON response, and the frontend dynamically updates the DOM to display interactive stat cards, modal dialogues, or conversational messages.

---

### 9. TECHNOLOGIES USED

| Category | Technology / Tool | Version / Details |
| :--- | :--- | :--- |
| **Programming Language** | Python | Version 3.11+ |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) | Vanilla client-side architecture with Glassmorphism UI |
| **Backend Framework** | FastAPI (ASGI) | Asynchronous, high-performance REST framework |
| **Web Server** | Uvicorn | Production ASGI web server implementation |
| **Database** | MySQL Server | Version 8.0 (Relational schema with InnoDB engine) |
| **Database Driver** | PyMySQL | Pure-Python MySQL client library |
| **Security & Cryptography** | Bcrypt & PyJWT | 12-round salted hashing & HMAC-SHA256 signed JWT |
| **Natural Language Processing** | Sentence-Transformers | Hugging Face `all-MiniLM-L6-v2` (384-dimensional embeddings) |
| **Machine Learning / Math** | PyTorch, Scikit-learn, NumPy | Vector algebra, cosine similarity calculation |
| **LLM Integration** | Google GenAI SDK | Gemini 2.5 Flash for context-grounded reasoning |
| **IDE & Development** | Visual Studio Code | Cross-platform code editing and debugging |
| **Version Control** | Git & GitHub | Source code tracking and version control |

---

### 10. PROJECT MODULES

The project is structured into five distinct, decoupled functional modules:

* **Module 1 – Authentication & Security Management (`backend/auth.py`):**
  Handles user sign-in, credential verification using salted Bcrypt hashes, token creation, and FastAPI dependency injection (`get_current_student`, `get_current_admin`) to protect restricted endpoints.

* **Module 2 – Academic Database Management (`backend/database.py`):**
  Manages MySQL connection pooling, table schema creation (`students`, `subjects`, `student_subjects`, `attendance`, `exams`, `notices`, `chat_history`), relational foreign-key integrity, and automated seeding.

* **Module 3 – Student Academic Service (`backend/main.py`):**
  Provides RESTful endpoints for student-specific resources: `GET /student/profile`, `GET /student/attendance` (calculates aggregate and subject-wise metrics), `GET /student/exams` (computes countdown days), and `GET /student/notices`.

* **Module 4 – Intelligent AI Chatbot & Semantic Search (`backend/chatbot_service.py`):**
  Implements the dual-pipeline routing engine, Hinglish query normalization, sentence embedding computation, cosine similarity vector comparison, and live database query execution.

* **Module 5 – Responsive Student ERP Dashboard (`frontend/dashboard.html` & `.js`):**
  A user interface featuring student welcome telemetry, four interactive stat cards with detailed modal dialogues, real-time message exchange, theme switching, and secure session termination.

---

### 11. EXPECTED OUTCOMES
Upon complete deployment, the project delivers the following operational outcomes:
1. **Instantaneous Academic Access:** Students can view live subject-wise attendance and examination timetables in less than 200 milliseconds.
2. **Zero-Hallucination Academic Responses:** By querying MySQL directly for student records, personal information is guaranteed to be 100% factual and immune to generative AI fabrication.
3. **Reduced Administrative Inquiries:** Automated resolution of high-frequency repetitive queries (admissions, fee structures, placement records, hostel regulations) reduces manual counter inquiries by an estimated 60%–70%.
4. **Enhanced Data Privacy:** Plain-text passwords are eliminated through Bcrypt cryptographic protection, and student records are accessible solely through valid, signed tokens.

---

### 12. FUTURE SCOPE
Future extensions planned for the system include:
* **Mobile Application Development:** Building a native cross-platform mobile client using Flutter or React Native with biometric (fingerprint/face) sign-in.
* **Automated Alerting & Push Notifications:** Integrating automated WhatsApp / SMS / Email alerts when a student's attendance falls below the mandatory 75% AKTU threshold.
* **Cloud Infrastructure Deployment:** Containerizing the application and deploying on AWS / Google Cloud Platform with managed relational database services (RDS).
* **Predictive Performance Analytics:** Leveraging machine learning algorithms to forecast semester examination performance based on continuous internal assessment and attendance trends.
* **Voice-Activated Student Assistant:** Integrating real-time Web Speech APIs for speech-to-text and text-to-speech queries in regional languages.

---

### 13. REFERENCES
1. **FastAPI Documentation:** Tiangolo, S. *FastAPI: Modern, High-Performance Web Framework for Building APIs with Python*. Available at: https://fastapi.tiangolo.com/
2. **Sentence-Transformers & Dense Embeddings:** Reimers, N., & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. In Proceedings of EMNLP-IJCNLP 2019. Available at: https://arxiv.org/abs/1908.10084
3. **Bcrypt Cryptographic Hashing:** Provos, N., & Mazières, D. (1999). *A Future-Adaptable Password Scheme*. USENIX Annual Technical Conference.
4. **JWT Specification (RFC 7519):** Jones, M., Bradley, J., & Sakimura, N. (2015). *JSON Web Token (JWT)*. Internet Engineering Task Force (IETF). Available at: https://datatracker.ietf.org/doc/html/rfc7519
5. **AKTU Academic Regulations & Ordinances:** Dr. A.P.J. Abdul Kalam Technical University, Lucknow. *B.Tech Ordinance and Academic Regulations*. Available at: https://aktu.ac.in/
6. **ABES Engineering College Official Portal:** ABESEC Admissions, Course Structures, and Placement Records. Available at: https://www.abes.ac.in/
