import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


def create_project(db: Session, data: ProjectCreate) -> Project:
    project = Project(
        name=data.name,
        description=data.description,
        status=data.status,
        owner_id=data.owner_id,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_project(db: Session, project_id: uuid.UUID) -> Project | None:
    return db.execute(
        select(Project).where(Project.id == project_id)
    ).scalar_one_or_none()


def list_projects(db: Session, *, skip: int = 0, limit: int = 100) -> list[Project]:
    return list(
        db.execute(
            select(Project)
            .order_by(Project.created_at.desc())
            .offset(skip)
            .limit(limit)
        ).scalars().all()
    )


def update_project(
    db: Session,
    project_id: uuid.UUID,
    data: ProjectUpdate,
) -> Project | None:
    project = get_project(db, project_id)
    if project is None:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    project.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project_id: uuid.UUID) -> bool:
    project = get_project(db, project_id)
    if project is None:
        return False

    db.delete(project)
    db.commit()
    return True
