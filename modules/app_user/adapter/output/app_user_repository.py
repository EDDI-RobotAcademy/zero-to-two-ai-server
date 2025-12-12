from sqlalchemy.orm import Session
from typing import Optional, Dict
from modules.app_user.adapter.output.app_user_model import AppUser

class AppUserRepository:
    def __init__(self, db_session_factory):
        self.db_session_factory = db_session_factory

    def find_by_email(self, email: str) -> Optional[Dict]:
        db: Session = self.db_session_factory()
        try:
            user: Optional[AppUser] = db.query(AppUser).filter(AppUser.email == email, AppUser.is_deleted.is_(False)).first()
            if not user:
                return None
            return {
                "user_id": user.user_id,
                "name": user.name,
                "nickname": user.nickname,
                "phone": user.phone,
                "email": user.email,
                "signup_type": user.signup_type,
                "user_type": user.user_type,
                "is_deleted": user.is_deleted,
                "first_create_dt": user.first_create_dt,
                "last_update_dt": user.last_update_dt
            }
        finally:
            db.close()

    def create_user(self, name: str, nickname: str | None, phone: str | None,
                    email: str, signup_type: str, user_type: str) -> Dict:
        db: Session = self.db_session_factory()
        try:
            new_user = AppUser(
                name=name,
                nickname=nickname,
                phone=phone,
                email=email,
                signup_type=signup_type,
                user_type=user_type,
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return {
                "user_id": new_user.user_id,
                "name": new_user.name,
                "nickname": new_user.nickname,
                "phone": new_user.phone,
                "email": new_user.email,
                "signup_type": new_user.signup_type,
                "user_type": new_user.user_type,
                "is_deleted": new_user.is_deleted,
                "first_create_dt": new_user.first_create_dt,
                "last_update_dt": new_user.last_update_dt
            }
        finally:
            db.close()
