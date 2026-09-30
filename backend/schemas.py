from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any


class LoginRequest(BaseModel):
    username_or_id: str = Field(..., description="Student ID (e.g. AKTU001) or Admin username")
    password: str = Field(..., description="User password")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user: dict


class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    matched_question: Optional[str] = ""
    similarity_score: Optional[float] = 0.0
    source: Optional[str] = ""
    source_url: Optional[str] = ""
    is_student_specific: Optional[bool] = False


class StudentProfile(BaseModel):
    id: int
    student_id: str
    name: str
    email: str
    course: str
    branch: str
    semester: int
    section: str
    enrollment_year: int
    created_at: Optional[Any] = None
