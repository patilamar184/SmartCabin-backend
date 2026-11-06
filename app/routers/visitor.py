from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_owner
from app.schemas.visitor import (
    VisitorCreate,
    VisitorRegistrationResponse
)
from app.services.visitor import register_visitor

from app.schemas.visitor import VisitorResponse
from app.services.visitor import get_all_visitors

from app.services.visitor import get_visitor_by_id

router = APIRouter(
    prefix="/api/visitors",
    tags=["Visitors"]
)


@router.post(
    "/",
    response_model=VisitorRegistrationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_visitor(
    data: VisitorCreate,
    db: Session = Depends(get_db),
    current_owner=Depends(get_current_owner)
):
    return register_visitor(
        data=data,
        owner_id=current_owner.id,
        db=db
    )

@router.get(
    "/",
    response_model=list[VisitorResponse]
)
def list_visitors(
    db: Session = Depends(get_db),
    current_owner=Depends(get_current_owner)
):
    return get_all_visitors(
        owner_id=current_owner.id,
        db=db
    )



@router.get(
    "/{visitor_id}",
    response_model=VisitorResponse
)
def get_visitor(
    visitor_id: int,
    db: Session = Depends(get_db),
    current_owner=Depends(get_current_owner)
):
    return get_visitor_by_id(
        visitor_id=visitor_id,
        owner_id=current_owner.id,
        db=db
    )