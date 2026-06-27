import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict
from app.models.job import JobStatus, JobType

class JobBase(BaseModel):
    job_type: JobType
    input_data: dict[str, Any]
    project_id: uuid.UUID | None = None
    priority: int = 0
    provider_name: str | None = None

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: uuid.UUID
    user_id: uuid.UUID
    status: JobStatus
    progress: int
    error_message: str | None = None
    provider_name: str | None = None
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class JobUpdate(BaseModel):
    status: JobStatus | None = None
    progress: int | None = None
    output_data: dict[str, Any] | None = None
    error_message: str | None = None
