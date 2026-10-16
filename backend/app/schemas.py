from datetime import date, datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

Status = Literal["PENDING", "IN_PROGRESS", "SUBMITTED"]
Priority = Literal["LOW", "MEDIUM", "HIGH"]


class AssignmentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    subject: str = Field(default="General", max_length=120)
    notes: str = ""
    priority: Priority = "MEDIUM"
    status: Status = "PENDING"
    progress: int = Field(default=0, ge=0, le=100)
    due_date: date | None = None


class AssignmentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    subject: str | None = Field(default=None, max_length=120)
    notes: str | None = None
    priority: Priority | None = None
    status: Status | None = None
    progress: int | None = Field(default=None, ge=0, le=100)
    due_date: date | None = None


class AssignmentOut(AssignmentCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class StatsOut(BaseModel):
    total: int
    pending: int
    inProgress: int
    submitted: int
    overdue: int
    avgProgress: int


class AcademicAnalyticsOut(BaseModel):
    total_assignments: int
    subjects_count: int
    subject_breakdown: dict[str, int]
    completion_rate: int
    high_priority_pending: int
    next_deadline: date | None
    study_status: str

