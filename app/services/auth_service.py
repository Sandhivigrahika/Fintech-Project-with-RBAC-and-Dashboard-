from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

def register_user(db: Session,name: str, email: str, password: str):

    existing  = db.query(User).filter(User.email==email).first()

    if existing:
        raise HTTPException(400, "Email already registered")

    user = User(
        name=name,
        email=email,
        hashed_password=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

''' pydantic response model will serialize this user object into UserResponse '''


def login_user(db:Session, email: str, password: str):
    user= db.query(User).filter(User.email==email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(401,"Invalid credentials")

    token = create_access_token({"sub": str(user.id)})

    return token