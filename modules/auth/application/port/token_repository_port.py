from typing import Protocol, Optional

class TokenRepositoryPort(Protocol):
    def save_refresh(self, user_id: int, refresh_token: str, ttl_seconds: int = ...) -> None:
        ...

    def get_refresh(self, user_id: int) -> Optional[str]:
        ...

    def delete_refresh(self, user_id: int) -> None:
        ...