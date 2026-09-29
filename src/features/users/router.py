# External imports -----------------------------------------------------------------------------------------------------
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timezone
# Internal imports -----------------------------------------------------------------------------------------------------
from src.features.users.schemas import UserCreate, UserResponse, UserLogin, LoginResponse, TokenResponse
from src.features.users.models import User, RefreshToken
from src.db.session import get_db
from src.core.security import create_access_token, create_refresh_token, decode_token
from src.features.users.dependencies import get_current_user
from src.features.users.schemas import RefreshRequest





# Necessary classes, objects and functions -----------------------------------------------------------------------------

router = APIRouter(prefix="/users", tags=["users api"])

password_hasher = PasswordHasher()





def store_refresh_token(db: Session, token: str) -> None:
    payload = decode_token(token)
    db.add(RefreshToken(
        jti=payload["jti"],
        user_id=int(payload["sub"]),
        expires_at=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
    ))









# Create A New User API ------------------------------------------------------------------------------------------------

@router.post("/signup", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):

    try:
        user_exists = db.query(User).filter((User.email == user.email) | (User.username == user.username)).first()

        if user_exists:
            raise HTTPException(status_code=400, detail="Email or username already registered")

        hashed_password = password_hasher.hash(user.password)

        new_user = User(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            hashed_password=hashed_password,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except HTTPException:
        raise

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred while creating user") from error

    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error occurred") from error

    else:
        return new_user





# Get All Users API ----------------------------------------------------------------------------------------------------

@router.get("/all", response_model=list[UserResponse], status_code=200)
async def get_users(db: Session = Depends(get_db)):
    try:
        all_users = db.query(User).all()

    except HTTPException:
        raise

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Database error occurred while fetching users") from error

    except Exception as error:
        raise HTTPException(status_code=500, detail="Unexpected error occurred") from error

    else:
        return all_users





# Get A Single User API ------------------------------------------------------------------------------------------------

# @router.post("/refresh", response_model=TokenResponse, status_code=200)
# async def refresh_tokens(request: RefreshRequest, db: Session = Depends(get_db)):
#     try:
#         payload = decode_token(request.refresh_token)
#
#         if payload is None or payload.get("type") != "refresh":
#             raise HTTPException(status_code=401, detail="Invalid refresh token")
#
#         stored_token = db.query(RefreshToken).filter(RefreshToken.jti == payload.get("jti")).first()
#
#         if stored_token is None:
#             raise HTTPException(status_code=401, detail="Invalid refresh token")
#
#         if stored_token.revoked:
#             db.query(RefreshToken).filter(RefreshToken.user_id == stored_token.user_id).update({"revoked": True})
#             db.commit()
#             raise HTTPException(status_code=401, detail="Refresh token reuse detected. Please sign in again.")
#
#         user = db.query(User).filter(User.id == stored_token.user_id).first()
#
#         if user is None or not user.is_active:
#             raise HTTPException(status_code=401, detail="Invalid refresh token")
#
#         stored_token.revoked = True
#
#         new_access_token = create_access_token({"sub": str(user.id)})
#         new_refresh_token = create_refresh_token({"sub": str(user.id)})
#         store_refresh_token(db, new_refresh_token)
#         db.commit()
#
#     except HTTPException:
#         raise
#
#     except SQLAlchemyError as error:
#         db.rollback()
#         raise HTTPException(status_code=500, detail="Database error occurred during token refresh") from error
#
#     except Exception as error:
#         db.rollback()
#         raise HTTPException(status_code=500, detail="Unexpected error occurred") from error
#
#     else:
#         return {"access_token": new_access_token, "refresh_token": new_refresh_token}


@router.post("/refresh", response_model=TokenResponse, status_code=200)
async def refresh_tokens(request: RefreshRequest, db: Session = Depends(get_db)):
    try:
        payload = decode_token(request.refresh_token)

        if payload is None or payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        stored_token = db.query(RefreshToken).filter(RefreshToken.jti == payload.get("jti")).first()

        if stored_token is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        if stored_token.revoked:
            db.query(RefreshToken).filter(RefreshToken.user_id == stored_token.user_id).update({"revoked": True})
            db.commit()
            raise HTTPException(status_code=401, detail="Refresh token reuse detected. Please sign in again.")

        user = db.query(User).filter(User.id == stored_token.user_id).first()

        if user is None or not user.is_active:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        stored_token.revoked = True

        new_access_token = create_access_token({"sub": str(user.id)})
        new_refresh_token = create_refresh_token({"sub": str(user.id)})
        store_refresh_token(db, new_refresh_token)
        db.commit()

    except HTTPException:
        raise

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred during token refresh") from error

    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error occurred") from error

    else:
        return {"access_token": new_access_token, "refresh_token": new_refresh_token}





# Get A Single User API ------------------------------------------------------------------------------------------------

@router.get("/{user_id}", response_model=UserResponse, status_code=200)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.id == user_id).first()

        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")

    except HTTPException:
        raise

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Database error occurred while fetching user") from error

    except Exception as error:
        raise HTTPException(status_code=500, detail="Unexpected error occurred") from error

    else:
        return existing_user





# Update A Single User API ---------------------------------------------------------------------------------------------

@router.put("/update/{user_id}", response_model=UserResponse, status_code=200)
async def update_user(user_id: int, updated_user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.id == user_id).first()

        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        existing_user.email = updated_user.email
        existing_user.username = updated_user.username
        existing_user.full_name = updated_user.full_name
        existing_user.hashed_password = password_hasher.hash(updated_user.password)

        db.commit()
        db.refresh(existing_user)

    except HTTPException:
        raise

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred while updating user") from error

    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error occurred") from error

    else:
        return existing_user





# Delete A Single User API ---------------------------------------------------------------------------------------------

@router.delete("/delete/{user_id}", status_code=200)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.id == user_id).first()

        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(existing_user)
        db.commit()

    except HTTPException:
        raise

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred while deleting user") from error

    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error occurred") from error

    else:
        return {"message": "User deleted successfully!"}





# Sign-In A Single User API --------------------------------------------------------------------------------------------

# @router.post("/signin", response_model=LoginResponse, status_code=200)
# async def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
#     try:
#         existing_user = db.query(User).filter(User.email == credentials.email).first()
#
#         if existing_user is None:
#             raise HTTPException(status_code=401, detail="Incorrect email or password")
#
#         try:
#             password_hasher.verify(existing_user.hashed_password, credentials.password)
#         except VerifyMismatchError:
#             raise HTTPException(status_code=401, detail="Incorrect email or password")
#
#         if not existing_user.is_active:
#             raise HTTPException(status_code=403, detail="Account is inactive")
#
#     except HTTPException:
#         raise
#
#     except SQLAlchemyError as error:
#         raise HTTPException(status_code=500, detail="Database error occurred during login") from error
#
#     except Exception as error:
#         raise HTTPException(status_code=500, detail="Unexpected error occurred") from error
#
#     else:
#         return {"message": "Login successful", "user_id": existing_user.id, "email": existing_user.email}


# @router.post("/signin", response_model=TokenResponse, status_code=200)
# async def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
#     try:
#         existing_user = db.query(User).filter(User.email == credentials.email).first()
#
#         if existing_user is None:
#             raise HTTPException(status_code=401, detail="Incorrect email or password")
#
#         try:
#             password_hasher.verify(existing_user.hashed_password, credentials.password)
#         except VerifyMismatchError:
#             raise HTTPException(status_code=401, detail="Incorrect email or password")
#
#         if not existing_user.is_active:
#             raise HTTPException(status_code=403, detail="Account is inactive")
#
#     except HTTPException:
#         raise
#
#     except SQLAlchemyError as error:
#         raise HTTPException(status_code=500, detail="Database error occurred during login") from error
#
#     except Exception as error:
#         raise HTTPException(status_code=500, detail="Unexpected error occurred") from error
#
#     else:
#         access_token = create_access_token({"sub": str(existing_user.id)})
#         refresh_token = create_refresh_token({"sub": str(existing_user.id)})
#         return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/signin", response_model=TokenResponse, status_code=200)
async def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == credentials.email).first()

        if existing_user is None:
            raise HTTPException(status_code=401, detail="Incorrect email or password")

        try:
            password_hasher.verify(existing_user.hashed_password, credentials.password)
        except VerifyMismatchError:
            raise HTTPException(status_code=401, detail="Incorrect email or password")

        if not existing_user.is_active:
            raise HTTPException(status_code=403, detail="Account is inactive")

        access_token = create_access_token({"sub": str(existing_user.id)})
        refresh_token = create_refresh_token({"sub": str(existing_user.id)})
        store_refresh_token(db, refresh_token)
        db.commit()

    except HTTPException:
        raise

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred during login") from error

    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error occurred") from error

    else:
        return {"access_token": access_token, "refresh_token": refresh_token}





# Get A Single User (through JWT verification) API ---------------------------------------------------------------------

@router.get("/verified/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user




