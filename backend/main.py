import os
import datetime
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# Ensure root .env is loaded automatically regardless of working directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.database import init_db, get_db_connection, check_db_health
from backend.auth import (
    verify_password,
    create_access_token,
    get_current_user,
    get_current_student,
    get_current_admin,
    get_optional_user
)
# =========================================================
# GEMINI API KEY CONFIGURATION (NO TERMINAL COMMAND NEEDED)
# =========================================================
# Option 1 (Recommended): Add GEMINI_API_KEY=your_key in your .env file
# Option 2: Or paste your Gemini API key directly between the quotes below:
DIRECT_GEMINI_API_KEY = ""

if DIRECT_GEMINI_API_KEY.strip() and not os.getenv("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = DIRECT_GEMINI_API_KEY.strip()

from backend.schemas import LoginRequest, TokenResponse, ChatRequest, ChatResponse
from backend.chatbot_service import get_answer


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing ABES Student Portal Database...")
    try:
        init_db()
        print("Database schema and baseline seed records verified!")
    except Exception as e:
        print(f"Database initialization warning: {e}")
    yield
    print("Shutting down ABES Student Support Portal API.")


app = FastAPI(
    title="ABES Student Support AI Portal",
    description="Intelligent AI Portal with Student Services, MySQL Integration, and Semantic Support for ABES Engineering College",
    version="2.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_dir = os.path.join(BASE_DIR, "frontend")
if os.path.exists(frontend_dir):
    app.mount("/portal", StaticFiles(directory=frontend_dir, html=True), name="portal")


# =========================================================
# SYSTEM & HEALTH ENDPOINTS
# =========================================================

@app.get("/")
def home():
    return {
        "portal": "ABES Engineering College Student Support AI Portal",
        "version": "2.0",
        "status": "Online",
        "database": "MySQL Connected" if check_db_health() else "Disconnected"
    }


@app.get("/health")
def health():
    db_healthy = check_db_health()
    return {
        "status": "healthy" if db_healthy else "degraded",
        "database": "connected" if db_healthy else "disconnected",
        "ai_engine": "SentenceTransformer all-MiniLM-L6-v2 active"
    }


# =========================================================
# PHASE 1: AUTHENTICATION (STUDENT & ADMIN)
# =========================================================

@app.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    user_id = credentials.username_or_id.strip()
    plain_password = credentials.password

    if not user_id or not plain_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID/Username and password are required."
        )

    try:
        conn = get_db_connection()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Student services are temporarily unavailable. Please try again later."
        )

    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, student_id, name, email, password_hash, course, branch, semester, section, enrollment_year
            FROM students
            WHERE student_id = %s OR email = %s
            """,
            (user_id, user_id)
        )
        student = cursor.fetchone()

        if student and verify_password(plain_password, student["password_hash"]):
            conn.close()
            token_payload = {
                "sub": student["student_id"],
                "id": student["id"],
                "role": "student",
                "name": student["name"]
            }
            token = create_access_token(token_payload)
            student_profile = {
                "id": student["id"],
                "student_id": student["student_id"],
                "name": student["name"],
                "email": student["email"],
                "course": student["course"],
                "branch": student["branch"],
                "semester": student["semester"],
                "section": student["section"],
                "enrollment_year": student["enrollment_year"]
            }
            return TokenResponse(
                access_token=token,
                token_type="bearer",
                role="student",
                user=student_profile
            )

        cursor.execute(
            """
            SELECT id, username, name, email, password_hash
            FROM admins
            WHERE username = %s OR email = %s
            """,
            (user_id, user_id)
        )
        admin = cursor.fetchone()

        if admin and verify_password(plain_password, admin["password_hash"]):
            conn.close()
            token_payload = {
                "sub": admin["username"],
                "id": admin["id"],
                "role": "admin",
                "name": admin["name"]
            }
            token = create_access_token(token_payload)
            admin_profile = {
                "id": admin["id"],
                "username": admin["username"],
                "name": admin["name"],
                "email": admin["email"]
            }
            return TokenResponse(
                access_token=token,
                token_type="bearer",
                role="admin",
                user=admin_profile
            )

    conn.close()
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Student ID or password."
    )


@app.post("/logout")
def logout():
    return {"message": "Logged out successfully."}


# =========================================================
# PHASE 2 & 3: STUDENT-SPECIFIC DATA APIS
# =========================================================

@app.get("/student/profile")
def get_student_profile(current_user: dict = Depends(get_current_student)):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, student_id, name, email, course, branch, semester, section, enrollment_year, created_at
                FROM students
                WHERE id = %s
                """,
                (current_user["id"],)
            )
            profile = cursor.fetchone()
        conn.close()

        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found."
            )

        if "created_at" in profile and profile["created_at"]:
            profile["created_at"] = str(profile["created_at"])

        return profile
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load student profile."
        )


@app.get("/student/attendance")
def get_student_attendance(current_user: dict = Depends(get_current_student)):
    """Fetch live subject-wise attendance and calculate overall percentage."""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT s.subject_code, s.subject_name, a.total_classes, a.attended_classes, a.attendance_percentage, a.updated_at
                FROM attendance a
                JOIN subjects s ON a.subject_id = s.id
                WHERE a.student_id = %s
                ORDER BY s.subject_code ASC
                """,
                (current_user["id"],)
            )
            records = cursor.fetchall()
        conn.close()

        if not records:
            return {
                "records": [],
                "overall_percentage": 0.0,
                "total_attended": 0,
                "total_classes": 0,
                "message": "Attendance data is not available yet."
            }

        total_classes = sum(r["total_classes"] for r in records)
        total_attended = sum(r["attended_classes"] for r in records)
        overall_percentage = round((total_attended / total_classes * 100), 2) if total_classes > 0 else 0.0

        for r in records:
            r["attendance_percentage"] = float(r["attendance_percentage"])
            if r.get("updated_at"):
                r["updated_at"] = str(r["updated_at"])

        return {
            "records": records,
            "overall_percentage": overall_percentage,
            "total_attended": total_attended,
            "total_classes": total_classes,
            "message": "Attendance data loaded successfully."
        }
    except Exception as e:
        print(f"Error loading attendance: {e}")
        return {
            "records": [],
            "overall_percentage": 0.0,
            "message": "Attendance data is not available yet."
        }


@app.get("/student/subjects")
def get_student_subjects(current_user: dict = Depends(get_current_student)):
    """Fetch registered academic subjects for the student."""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT s.id, s.subject_code, s.subject_name, s.semester, s.branch
                FROM subjects s
                JOIN student_subjects ss ON ss.subject_id = s.id
                WHERE ss.student_id = %s
                ORDER BY s.subject_code ASC
                """,
                (current_user["id"],)
            )
            subjects = cursor.fetchall()
        conn.close()
        return {"subjects": subjects}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load subjects."
        )


@app.get("/student/exams")
def get_student_exams(current_user: dict = Depends(get_current_student)):
    """Fetch upcoming examinations with room details and date countdown."""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT s.subject_code, s.subject_name, e.exam_type, e.exam_date, e.start_time, e.end_time, e.room
                FROM exams e
                JOIN subjects s ON e.subject_id = s.id
                JOIN student_subjects ss ON ss.subject_id = s.id
                WHERE ss.student_id = %s
                ORDER BY e.exam_date ASC
                """,
                (current_user["id"],)
            )
            exams = cursor.fetchall()
        conn.close()

        if not exams:
            return {
                "exams": [],
                "message": "No upcoming examination data is available."
            }

        today = datetime.date.today()
        formatted_exams = []
        for ex in exams:
            ex_date = ex["exam_date"]
            days_left = (ex_date - today).days if isinstance(ex_date, datetime.date) else 0
            formatted_exams.append({
                "subject_code": ex["subject_code"],
                "subject_name": ex["subject_name"],
                "exam_type": ex["exam_type"],
                "exam_date": str(ex_date),
                "start_time": str(ex["start_time"]),
                "end_time": str(ex["end_time"]),
                "room": ex["room"],
                "days_left": days_left
            })

        return {"exams": formatted_exams}
    except Exception as e:
        print(f"Error loading exams: {e}")
        return {
            "exams": [],
            "message": "No upcoming examination data is available."
        }


@app.get("/student/notices")
def get_notices():
    """Retrieve official college notices and circulars."""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, description, category, notice_date, source_url
                FROM notices
                ORDER BY notice_date DESC, id DESC
                """
            )
            notices = cursor.fetchall()
        conn.close()

        for n in notices:
            if n.get("notice_date"):
                n["notice_date"] = str(n["notice_date"])

        return {"notices": notices}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load notices."
        )


# =========================================================
# PHASE 4 & 5: CHATBOT & HISTORY ENDPOINTS
# =========================================================

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, req: Request):
    """
    Handle questions with automatic contextual routing:
    - If question is student-specific (attendance, exams, subjects, profile) and user is authenticated, query MySQL.
    - Else search ABES Knowledge Base, then generic university FAQ.
    """
    student_payload = get_optional_user(req)
    result = get_answer(request.question, student_context=student_payload)

    # Save to chat history if logged in
    if student_payload and student_payload.get("role") == "student":
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO chat_history (student_id, question, answer, matched_question, source)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        student_payload["id"],
                        request.question,
                        result.get("answer", ""),
                        result.get("matched_question", ""),
                        result.get("source", "")
                    )
                )
            conn.close()
        except Exception as e:
            print(f"Warning: Could not save chat history: {e}")

    return ChatResponse(
        answer=result.get("answer", ""),
        matched_question=result.get("matched_question", ""),
        similarity_score=result.get("similarity_score", 0.0),
        source=result.get("source", ""),
        source_url=result.get("source_url", ""),
        is_student_specific=result.get("is_student_specific", False)
    )


@app.get("/chat/history")
def get_chat_history(current_user: dict = Depends(get_current_student)):
    """Retrieve chat history for the authenticated student."""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, question, answer, matched_question, source, created_at
                FROM chat_history
                WHERE student_id = %s
                ORDER BY id ASC
                LIMIT 50
                """,
                (current_user["id"],)
            )
            history = cursor.fetchall()
        conn.close()

        for h in history:
            if h.get("created_at"):
                h["created_at"] = str(h["created_at"])

        return {"history": history}
    except Exception as e:
        print(f"Error fetching chat history: {e}")
        return {"history": []}


@app.delete("/chat/history")
def clear_chat_history(current_user: dict = Depends(get_current_student)):
    """Clear chat history for the authenticated student."""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM chat_history WHERE student_id = %s",
                (current_user["id"],)
            )
        conn.close()
        return {"message": "Chat history cleared successfully."}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear chat history."
        )