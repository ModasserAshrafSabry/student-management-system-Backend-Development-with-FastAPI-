from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import hash_password, verify_password, create_access_token

import app.utils.metrics as metrics

router = APIRouter()


# 🟢 REGISTER
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    # 🔴 Check if email exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        metrics.recent_auth_logs.append(
            f"Register failed: email already exists ({user.email})"
        )
        raise HTTPException(status_code=400, detail="Email already exists")

    # 🔴 Check if username exists
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        metrics.recent_auth_logs.append(
            f"Register failed: username exists ({user.username})"
        )
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role="admin"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    metrics.recent_auth_logs.append(
        f"Register success: {user.username}"
    )

    if len(metrics.recent_auth_logs) > 5:
        metrics.recent_auth_logs.pop(0)

    return {"message": "User created successfully"}


# 🟢 LOGIN
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    # 🔴 Validation
    if not db_user:
        metrics.recent_auth_logs.append(
            f"Login failed: {form_data.username}"
        )

        if len(metrics.recent_auth_logs) > 5:
            metrics.recent_auth_logs.pop(0)

        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, db_user.password):
        metrics.recent_auth_logs.append(
            f"Login failed: {form_data.username}"
        )

        if len(metrics.recent_auth_logs) > 5:
            metrics.recent_auth_logs.pop(0)

        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.username})

    metrics.recent_auth_logs.append(
        f"Login success: {db_user.username}"
    )

    if len(metrics.recent_auth_logs) > 5:
        metrics.recent_auth_logs.pop(0)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }




