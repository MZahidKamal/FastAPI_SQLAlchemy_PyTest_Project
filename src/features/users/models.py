# External imports -----------------------------------------------------------------------------------------------------
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
# Internal imports -----------------------------------------------------------------------------------------------------
from src.db.base import SqlalchemyBase





# Necessary classes, objects and functions -----------------------------------------------------------------------------

class User(SqlalchemyBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Login credentials
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Profile info
    full_name = Column(String, nullable=True)

    # Account status flags — এগুলো পরে JWT/auth logic-এ ব্যবহার হবে
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)





class RefreshToken(SqlalchemyBase):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)




