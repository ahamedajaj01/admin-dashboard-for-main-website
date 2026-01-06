from fastapi import APIRouter, Depends, HTTPException, Query
from app.db.session import get_db
from sqlalchemy.orm import Session, selectinload
from app.schemas.training import TrainingCreate, TrainingUpdate, TrainingResponse, MentorResponse
from app.auth.deps import get_current_user
from typing import List
from decimal import Decimal
from app.models.training.training import Training
from app.models.training.benefit import TrainingBenefit
from app.models.training.mentor import Mentor
from app.models.training.training_mentor import TrainingMentor
from app.models.pricing.enums import DiscountType
from uuid import UUID

router = APIRouter(
    prefix="/admin/trainings",
    tags=["Trainings"]
)
# ---------- shared pricing logic (single source of truth) ----------
def calculate_effective_price(base_price: Decimal, discount_value: Decimal, discount_type: DiscountType | None,) -> Decimal:
    if not discount_value or not discount_type:
        return base_price
    if discount_type == DiscountType.PERCENTAGE:
        return base_price - (base_price * discount_value / Decimal(100))
    return base_price - discount_value

# ---------- shared api response (used by CREATE, GET, UPDATE) ----------
def training_response(training:Training)->TrainingResponse:
        effective_price = calculate_effective_price(
        training.base_price,
        training.discount_value,
        training.discount_type,
    )
        return TrainingResponse(
        id=str(training.id),
        title=training.title,
        description=training.description,
        photo_url=training.photo_url,
        base_price=training.base_price,
        effective_price=effective_price,
        benefits=[b.text for b in training.benefits],  # read from DB, not request
        mentors=[
            MentorResponse(
                id=str(m.mentor.id),
                name=m.mentor.name,
                photo_url=m.mentor.photo_url,
            )
            for m in training.training_mentors
        ],
        created_at=training.created_at,
        updated_at=training.updated_at,
    )

# ==================  Crud operations ======================#
@router.post("/", response_model=TrainingResponse)
def create_training(
    data: TrainingCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # create base training
    training = Training(
        title=data.title,
        description=data.description,
        photo_url=data.photo_url,
        base_price=data.base_price,
        discount_type=data.discount_type,
        discount_value=data.discount_value,
    )
    db.add(training)
    db.flush()  # get training.id

    # insert benefits
    for benefit_text in data.benefits:
        db.add(
            TrainingBenefit(
                training_id=training.id,
                text=benefit_text,
            )
        )

    # insert mentors (loop may be empty — OK)
    for mentor_id in data.mentor_ids:
        mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()

        if not mentor:
            raise HTTPException(
                status_code=400,
                detail=f"Mentor {mentor_id} does not exist",
            )

        db.add(
            TrainingMentor(
                training_id=training.id,
                mentor_id=mentor.id,
            )
        )

    # ✅ commit ONCE
    db.commit()

    # ✅ refresh AFTER commit
    db.refresh(training)

    # ✅ ALWAYS return
    return training_response(training)


# ================== LIST TRAININGS ==================
@router.get("/", response_model=dict)
def list_trainings(
    page: int = Query(1, ge=1),          # 1-based pagination
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # total count 
    total = db.query(Training).count()
    # paginated query with eager loading (no N+1)
    trainings = (
        db.query(Training).options(
            selectinload(Training.benefits),          # load benefits
            selectinload(Training.training_mentors)   # load mentors join
            .selectinload(TrainingMentor.mentor)      # load mentor itself
        )
        .order_by(Training.created_at.desc())
        .offset((page - 1)* page_size)
        .limit(page_size)
        .all()
    )
    # build response
    items = [training_response(t) for t in trainings]
    return {
        "items":items,
        "page": page,
        "page_size": page_size,
        "total": total,
    }

    

@router.get("/{training_id}", response_model=TrainingResponse)
def get_training_detail(training_id: UUID, db: Session =Depends(get_db), user=Depends(get_current_user)):
    # fetch training with relations (no N+1)
    training = (
        db.query(Training)
        .options(
            selectinload(Training.benefits),                # load benefits
            selectinload(Training.training_mentors)
            .selectinload(TrainingMentor.mentor),           # load mentors
        )
        .filter(Training.id == training_id).first()
    )
    if not training:
        raise HTTPException(status_code=404, detail="Training program not found")
    return training_response(training)

# ================== UPDATE TRAINING ==================

@router.put("/{training_id}", response_model=TrainingResponse)
def update_training(
    training_id: UUID,
    data: TrainingUpdate,
    db:Session= Depends(get_db),
    user = Depends(get_current_user),
):
    # load training with relations
    training = (
        db.query(Training)
        .options(
            selectinload(Training.benefits),
            selectinload(Training.training_mentors),
        )
        .filter(Training.id == training_id)
        .first()
    )

    if not training:
        raise HTTPException(status_code=404, detail="Training not found")
    
     # ---------- update scalar fields ----------
    training.title = data.title
    training.description = data.description
    training.photo_url = data.photo_url
    training.base_price = data.base_price
    training.discount_type = data.discount_type
    training.discount_value = data.discount_value

    # ---------- replace benefits ----------
    training.benefits.clear()  # authoritative list
    for benefit_text in data.benefits:
        training.benefits.append(
            TrainingBenefit(text=benefit_text)
        )
    
    # ---------- replace mentors ----------
    training.training_mentors.clear()  # authoritative list

    for mentor_id in data.mentor_ids:
        mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()

        if not mentor:
            raise HTTPException(400, f"Mentor {mentor_id} does not exist")
     
        
        training.training_mentors.append(
            TrainingMentor(mentor_id=mentor.id)
        )
     # single commit = atomic update
    db.commit()
    db.refresh(training)

    return training_response(training)
    

@router.delete("/{training_id}", status_code=204)
def delete_training(
    training_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # fetch training
    training = db.query(Training).filter(Training.id == training_id).first()

    if not training:
        raise HTTPException(status_code=404, detail="Training not found")
    
     # hard delete (FK CASCADE handles benefits & mentors)
    db.delete(training)
    db.commit()

    # 204 = success, no response body
    return
    
