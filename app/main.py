from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.database import Base, engine
import app.models.user
import app.models.schedule
import app.models.group
import app.models.group_schedule
import app.models.meeting
import app.models.travel
from app.routers import auth, users, schedules, groups, travels

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(schedules.router)
app.include_router(groups.router)
app.include_router(travels.router)


@app.get("/")
def root():
    return {"message": "Hello, Cheonga Log!"}
