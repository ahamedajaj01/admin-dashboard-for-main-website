from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.auth.deps import get_current_user
from app.models.training.mentor import Mentor
from app.schemas.mentor import MentorCreate, MentorUpdate, MentorResponse

router = APIRouter(
    prefix="/admin/mentors",
    tags=["Mentors"],
)

@router.get("/", response_model=list[MentorResponse])
def list_mentors(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    mentors = (
        db.query(Mentor)
        .order_by(Mentor.name.asc())
        .all()
    )

    return mentors

@router.post("/", response_model=MentorResponse)
def create_mentor(
    data: MentorCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    name_normalized = data.name.strip().lower()

    existing = (
        db.query(Mentor)
        .filter(Mentor.name.ilike(name_normalized))
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Mentor already exists",
        )

    mentor = Mentor(
        name=name_normalized,
        photo_url=data.photo_url,
    )

    db.add(mentor)
    db.commit()
    db.refresh(mentor)

    return mentor


# get mentor detail
@router.get("/{mentor_id}", response_model=MentorResponse)
def get_mentor(
    mentor_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()

    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")

    return mentor

@router.put("/{mentor_id}", response_model=MentorResponse)
def update_mentor(
    mentor_id: UUID,
    data: MentorUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()

    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")

    if data.name is not None:
         mentor.name = data.name.strip().lower()

    if data.photo_url is not None:
        mentor.photo_url = data.photo_url

    db.commit()
    db.refresh(mentor)

    return mentor
