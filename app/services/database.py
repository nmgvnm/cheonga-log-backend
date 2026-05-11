from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "postgresql://todo_user:todo_pass@localhost:5433/todo_db"
DATABASE_URL = ""

# engine = create_engine(DATABASE_URL, pool_pre_ping=True)
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
