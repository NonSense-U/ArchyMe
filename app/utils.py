from passlib.context import CryptContext
from fastapi import Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db
import logging  # Added logging for better debugging and tracking

# Create a logger
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    This function takes a plain password, hashes it and returns the hashed password.
    """
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Error hashing password: {e}")
        raise

def Check_Credentials(plane_password: str, hashed_password: str) -> bool:
    """
    This function takes a plain password and a hashed password,
    verifies the plain password against the hashed password and returns the result.
    """
    try:
        return pwd_context.verify(plane_password, hashed_password)
    except Exception as e:
        logger.error(f"Error checking credentials: {e}")
        raise

def Count_Ups(post_id: int, db: Session) -> int:
    """
    This function takes a post id and a database session,
    counts the number of upvotes for the post and returns the count.
    """
    try:
        Ups = db.query(models.Ups).filter(models.Ups.post_id == post_id).count()
        return Ups
    except Exception as e:
        logger.error(f"Error counting ups: {e}")
        raise

def Count_Downs(post_id: int, db: Session) -> int:
    """
    This function takes a post id and a database session,
    counts the number of downvotes for the post and returns the count.
    """
    try:
        Downs = db.query(models.Downs).filter(models.Downs.post_id == post_id).count()
        return Downs
    except Exception as e:
        logger.error(f"Error counting downs: {e}")
        raise
