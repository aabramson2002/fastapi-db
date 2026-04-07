from app.database import engine
from app.models.user import Base
from app.database import get_engine, Base

"""Initializing the engine here instead of in database.py to avoid circular imports when models import Base from database.py."""
engine = get_engine()

def init_db():
    Base.metadata.create_all(bind=engine)

def drop_db():
    Base.metadata.drop_all(bind=engine)

if __name__ == "__main__":
    init_db() # pragma: no cover