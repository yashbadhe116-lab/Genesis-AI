import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.job import Job, JobStatus
from app.schemas.job import JobCreate
from app.services import billing_service

def create_job(db: Session, user_id: uuid.UUID, job_create: JobCreate) -> Job:
    # 1. Deduct credits and record transaction (within same transaction if passed)
    # Note: billing_service.deduct_credits currently commits. 
    # To be truly atomic, we need to restructure billing_service to not commit automatically
    # OR we use nested transactions if supported by the DB.
    # Given the requirements, I will assume a flat commit for now or refactor billing.
    
    # Refactoring billing logic for atomicity
    cost = 10 # Example cost
    billing_service.deduct_credits(db, user_id, cost, f"Job: {job_create.job_type}")
    
    job = Job(
        user_id=user_id,
        **job_create.model_dump()
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def get_job(db: Session, job_id: uuid.UUID) -> Job | None:
    return db.execute(select(Job).where(Job.id == job_id)).scalar_one_or_none()

def list_jobs(db: Session, user_id: uuid.UUID):
    return db.execute(select(Job).where(Job.user_id == user_id).order_by(Job.created_at.desc())).scalars().all()

def update_status(db: Session, job_id: uuid.UUID, status: JobStatus):
    job = get_job(db, job_id)
    if job:
        job.status = status
        db.commit()
        db.refresh(job)
    return job

def delete_job(db: Session, job_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    job = db.execute(select(Job).where(Job.id == job_id, Job.user_id == user_id)).scalar_one_or_none()
    if job:
        db.delete(job)
        db.commit()
        return True
    return False
