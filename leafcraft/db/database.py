
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

#Connecting to mysql database - leafcraft
DATABASE_URL = "mysql+mysqlconnector://root:n%40rm%40d%40%211@127.0.0.1:3306/leafcraft"



engine = create_engine(DATABASE_URL, echo="debug", future=True)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()

#dependency function for FASTAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

