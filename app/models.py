from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Text
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Cat(Base):
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    years_of_experience = Column(Integer, nullable=False)
    breed = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)

    mission = relationship(
        "Mission",
        back_populates="cat",
        uselist=False
    )


class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    completed = Column(Boolean, default=False)

    cat_id = Column(Integer, ForeignKey("cats.id"), nullable=True)
    cat = relationship("Cat", back_populates="mission")

    targets = relationship(
        "Target",
        back_populates="mission",
        cascade="all, delete-orphan"
    )


class Target(Base):
    __tablename__ = "targets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    notes = Column(Text, default="")
    completed = Column(Boolean, default=False)

    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)
    mission = relationship("Mission", back_populates="targets")
