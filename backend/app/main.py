from contextlib import asynccontextmanager
from datetime import date

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .config import settings
from .db import Base, engine, get_db
from .models import Assignment
from .schemas import AssignmentCreate, AssignmentOut, AssignmentUpdate, StatsOut

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Production containers run Alembic before Uvicorn; create_all keeps tests self-contained.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
Instrumentator().instrument(app).expose(app, endpoint="/metrics")


@app.get("/")
def root():
    return {"service": settings.app_name, "version": "1.1.0", "docs": "/docs", "status": "operational"}


@app.get("/health")
@app.get("/api/health")
def health():
    return {"status": "UP"}


@app.get("/ready")
@app.get("/api/ready")
def ready(db: Session = Depends(get_db)):
    db.execute(select(func.count(Assignment.id)))
    return {"status": "READY"}


@app.get("/api/assignments", response_model=list[AssignmentOut])
def list_assignments(subject: str | None = None, db: Session = Depends(get_db)):
    query = select(Assignment).order_by(Assignment.due_date.is_(None), Assignment.due_date, Assignment.id.desc())
    if subject:
        query = query.where(Assignment.subject == subject)
    return list(db.scalars(query))


@app.get("/api/assignments/stats", response_model=StatsOut)
def stats(db: Session = Depends(get_db)):
    rows = db.execute(select(Assignment.status, func.count(Assignment.id)).group_by(Assignment.status)).all()
    counts = {s: c for s, c in rows}
    overdue = db.scalar(
        select(func.count(Assignment.id)).where(
            Assignment.due_date < date.today(), Assignment.status != "SUBMITTED"
        )
    )
    avg = db.scalar(select(func.avg(Assignment.progress))) or 0
    return StatsOut(
        total=sum(counts.values()),
        pending=counts.get("PENDING", 0),
        inProgress=counts.get("IN_PROGRESS", 0),
        submitted=counts.get("SUBMITTED", 0),
        overdue=overdue or 0,
        avgProgress=int(round(avg)),
    )


@app.get("/api/assignments/{assignment_id}", response_model=AssignmentOut)
def get_assignment(assignment_id: int, db: Session = Depends(get_db)):
    item = db.get(Assignment, assignment_id)
    if not item:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return item


@app.post("/api/assignments", response_model=AssignmentOut, status_code=status.HTTP_201_CREATED)
def create_assignment(payload: AssignmentCreate, db: Session = Depends(get_db)):
    item = Assignment(**payload.model_dump())
    if item.status == "SUBMITTED":
        item.progress = 100
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.put("/api/assignments/{assignment_id}", response_model=AssignmentOut)
def update_assignment(assignment_id: int, payload: AssignmentUpdate, db: Session = Depends(get_db)):
    item = db.get(Assignment, assignment_id)
    if not item:
        raise HTTPException(status_code=404, detail="Assignment not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    if item.status == "SUBMITTED":
        item.progress = 100
    db.commit()
    db.refresh(item)
    return item


@app.delete("/api/assignments/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    item = db.get(Assignment, assignment_id)
    if not item:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(item)
    db.commit()
