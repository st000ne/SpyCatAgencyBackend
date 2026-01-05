from typing import List, Optional
from pydantic import BaseModel, Field, validator


# =========================
# Cats
# =========================

class CatBase(BaseModel):
    name: str = Field(..., min_length=1)
    years_of_experience: int = Field(..., ge=0)
    breed: str = Field(..., min_length=1)


class CatCreate(CatBase):
    salary: int = Field(..., ge=0)


class CatUpdate(BaseModel):
    salary: int = Field(..., ge=0)


class CatRead(CatBase):
    id: int
    salary: int

    class Config:
        orm_mode = True


# =========================
# Targets
# =========================

class TargetCreate(BaseModel):
    name: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)
    notes: Optional[str] = ""


class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    completed: Optional[bool] = None


class TargetRead(BaseModel):
    id: int
    name: str
    country: str
    notes: str
    completed: bool

    class Config:
        orm_mode = True


# =========================
# Missions
# =========================

class MissionCreate(BaseModel):
    targets: List[TargetCreate]

    @validator("targets")
    def validate_targets_count(cls, targets):
        if not 1 <= len(targets) <= 3:
            raise ValueError("Mission must have between 1 and 3 targets")
        return targets


class MissionRead(BaseModel):
    id: int
    completed: bool
    cat_id: Optional[int]
    targets: List[TargetRead]

    class Config:
        orm_mode = True
