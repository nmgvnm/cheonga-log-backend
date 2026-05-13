from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.services.database import Base, engine
import app.models.user
import app.models.schedule
import app.models.group
import app.models.group_schedule
import app.models.meeting
import app.models.travel
from app.routers import auth, users, schedules, groups, travels

Base.metadata.create_all(bind=engine)

# 신규 컬럼 마이그레이션 (이미 존재하면 무시)
with engine.connect() as conn:
    for col, col_type in [("confirmed_time", "VARCHAR"), ("confirmed_location", "VARCHAR")]:
        try:
            conn.execute(text(f"ALTER TABLE group_schedules ADD COLUMN {col} {col_type}"))
            conn.commit()
        except Exception:
            conn.rollback()

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
