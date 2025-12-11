from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from shared.infrastructure.config.database import Base

class AppUser(Base):
    __tablename__ = "app_user"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    nickname = Column(String(50), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(150), nullable=False, unique=True)
    signup_type = Column(String(50), nullable=False)
    user_type = Column(String(20), nullable=False)
    is_deleted = Column(Boolean, default=False)
    first_create_dt = Column(DateTime, server_default=func.now())
    last_update_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())
