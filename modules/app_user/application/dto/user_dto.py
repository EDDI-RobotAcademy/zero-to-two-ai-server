from pydantic import BaseModel


class UserInfo(BaseModel):
    id: int
    email: str
    nickname: str
    user_type: str  # 임대인 / 임차인