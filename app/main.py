from fastapi import FastAPI

from database import engine
from models import Base
from routers import cats, missions

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Spy Cat Agency API")

app.include_router(cats.router)
app.include_router(missions.router)
