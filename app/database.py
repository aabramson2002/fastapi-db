# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

from .config import settings

# Base declarative class that our models will inherit from
Base = declarative_base()

SessionLocal = None  # Will be initialized after engine creation

def get_engine(database_url: str = settings.DATABASE_URL):
    """
    Create and return a new SQLAlchemy engine.

    Args:
        database_url (str): The database connection URL.

    Returns:
        Engine: A new SQLAlchemy Engine instance.
    """
    try:
        # Create an engine instance with echo=True to log SQL queries (useful for learning)
        engine = create_engine(database_url, echo=True)
        return engine
    except SQLAlchemyError as e:
        print(f"Error creating engine: {e}")
        raise

def get_sessionmaker(engine):
    """
    Create and return a new sessionmaker.

    Args:
        engine (Engine): The SQLAlchemy Engine to bind the sessionmaker to.

    Returns:
        sessionmaker: A configured sessionmaker factory.
    """
    return sessionmaker(
        autocommit=False,  # Disable autocommit to control transactions manually
        autoflush=False,   # Disable autoflush to control when changes are sent to the DB
        bind=engine        # Bind the sessionmaker to the provided engine
    )

def init_db(database_url: str = settings.DATABASE_URL):
    """Initialize the database by creating the engine and sessionmaker.
    This function should be called at application startup to set up the database connection.
    
    Args:        
        database_url (str): The database connection URL.
    
    Returns:        
        Engine: The initialized SQLAlchemy Engine instance.
    """
    global SessionLocal
    engine = get_engine(database_url)
    SessionLocal = get_sessionmaker(engine)
    return engine

def get_db():
    """
    Dependency function that provides a database session.

    This function can be used with FastAPI's dependency injection system
    to provide a database session to your route handlers.

    Yields:
        Session: A SQLAlchemy Session instance.
    """
    if SessionLocal is None:
       raise RuntimeError("Database not initialized")
    
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Provide the session to the caller
    finally:
        db.close()  # Ensure the session is closed after use