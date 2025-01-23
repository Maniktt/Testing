from sqlalchemy.orm import Session
from app.models import User  # Assuming User is the SQLAlchemy model
from .schema import UserUpdate, UserPatch  # The Pydantic model for updates
from fastapi import HTTPException


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.name = user_update.name
    db_user.email = user_update.email
    db_user.age = user_update.age

    db.commit()  # Save changes to the database
    db.refresh(db_user)  # Refresh the instance to reflect the changes
    return db_user  # This is the SQLAlchemy model, which will be serialized by Pydantic

def patch_user(db: Session, user_id: int, user_patch: UserPatch):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")  # User not found

    # Only update the fields that were provided (allow partial update)
    if user_patch.name is not None:
        db_user.name = user_patch.name
    if user_patch.email is not None:
      db_user.email = user_patch.email
    if user_patch.age is not None:
        db_user.age = user_patch.age

    db.commit()  # Save changes to the database
    db.refresh(db_user)  # Refresh the instance to reflect the changes

    return db_user
