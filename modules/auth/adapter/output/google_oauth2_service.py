import os
import requests
from urllib.parse import quote
from fastapi import HTTPException
from modules.auth.application.dto.auth_dto import GetAccessTokenRequest, AccessToken

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

class GoogleOAuth2Service:
    def get_authorization_url(self, state: str | None = None) -> str:
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        redirect_uri = quote(os.getenv("GOOGLE_REDIRECT_URI", ""), safe='')
        scope = "openid email profile"
        url = (
            f"{GOOGLE_AUTH_URL}"
            f"?client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type=code"
            f"&scope={quote(scope)}"
        )
        if state:
            url = f"{url}&state={quote(state)}"
        return url

    def exchange_code_for_token(self, request: GetAccessTokenRequest) -> AccessToken:
        data = {
            "code": request.code,
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
            "grant_type": "authorization_code"
        }
        try:
            resp = requests.post(GOOGLE_TOKEN_URL, data=data, timeout=10)
            resp.raise_for_status()
            token_data = resp.json()
        except requests.Timeout:
            raise HTTPException(status_code=504, detail="GOOGLE_API_TIMEOUT")
        except requests.HTTPError as e:
            # 구글 API 에러 (400, 401 등)
            raise HTTPException(status_code=502, detail="GOOGLE_TOKEN_EXCHANGE_FAILED")
        except requests.RequestException:
            # 네트워크 에러
            raise HTTPException(status_code=503, detail="GOOGLE_API_UNAVAILABLE")

        return AccessToken(
            access_token=token_data.get("access_token"),
            token_type=token_data.get("token_type"),
            expires_in=token_data.get("expires_in"),
            refresh_token=token_data.get("refresh_token")
        )

    def fetch_user_profile(self, access_token: AccessToken) -> dict:
        headers = {"Authorization": f"Bearer {access_token.access_token}"}
        try:
            resp = requests.get(GOOGLE_USERINFO_URL, headers=headers, timeout=5)
            resp.raise_for_status()
            return resp.json()
        except requests.Timeout:
            raise HTTPException(status_code=504, detail="GOOGLE_API_TIMEOUT")
        except requests.HTTPError:
            raise HTTPException(status_code=502, detail="GOOGLE_USERINFO_FAILED")
        except requests.RequestException:
            raise HTTPException(status_code=503, detail="GOOGLE_API_UNAVAILABLE")
