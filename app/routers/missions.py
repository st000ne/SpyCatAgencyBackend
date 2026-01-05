from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.models as models
import app.schemas as schemas
from app.deps import get_db

router = APIRouter(prefix="/missions", tags=["Missions"])


@router.post("/", response_model=schemas.MissionRead, status_code=status.HTTP_201_CREATED)
def create_mission(
    payload: schemas.MissionCreate,
    db: Session = Depends(get_db)
):
    mission = models.Mission(completed=False)

    for target_data in payload.targets:
        target = models.Target(
            name=target_data.name,
            country=target_data.country,
            notes=target_data.notes or "",
            completed=False
        )
        mission.targets.append(target)

    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission


@router.get("/", response_model=list[schemas.MissionRead])
def list_missions(db: Session = Depends(get_db)):
    return db.query(models.Mission).all()


@router.get("/{mission_id}", response_model=schemas.MissionRead)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if mission.cat_id is not None:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete an assigned mission"
        )

    db.delete(mission)
    db.commit()


@router.patch("/{mission_id}/assign/{cat_id}", response_model=schemas.MissionRead)
def assign_cat_to_mission(
    mission_id: int,
    cat_id: int,
    db: Session = Depends(get_db)
):
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    if cat.mission is not None:
        raise HTTPException(
            status_code=400,
            detail="Cat already assigned to a mission"
        )

    mission.cat = cat
    db.commit()
    db.refresh(mission)
    return mission


@router.patch("/targets/{target_id}", response_model=schemas.TargetRead)
def update_target(
    target_id: int,
    payload: schemas.TargetUpdate,
    db: Session = Depends(get_db)
):
    target = db.query(models.Target).filter(models.Target.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    mission = target.mission

    if mission.completed or target.completed:
        raise HTTPException(
            status_code=400,
            detail="Cannot update a completed target or mission"
        )

    if payload.notes is not None:
        target.notes = payload.notes

    if payload.completed is True:
        target.completed = True

        if all(t.completed for t in mission.targets):
            mission.completed = True

    db.commit()
    db.refresh(target)
    return target
