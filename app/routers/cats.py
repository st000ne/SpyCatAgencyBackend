from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..services.cat_breed_validator import validate_breed

router = APIRouter(prefix="/cats", tags=["Cats"])


@router.post("/", response_model=schemas.CatRead, status_code=status.HTTP_201_CREATED)
def create_cat(cat: schemas.CatCreate, db: Session = Depends(get_db)):
    validate_breed(cat.breed)

    db_cat = models.Cat(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


@router.get("/", response_model=list[schemas.CatRead])
def list_cats(db: Session = Depends(get_db)):
    return db.query(models.Cat).all()


@router.get("/{cat_id}", response_model=schemas.CatRead)
def get_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat


@router.patch("/{cat_id}", response_model=schemas.CatRead)
def update_cat_salary(
    cat_id: int,
    payload: schemas.CatUpdate,
    db: Session = Depends(get_db)
):
    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    cat.salary = payload.salary
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    if cat.mission is not None:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete a cat assigned to a mission"
        )

    db.delete(cat)
    db.commit()
