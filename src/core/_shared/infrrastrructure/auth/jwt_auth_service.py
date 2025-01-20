import os

import jwt
from src._shared.logger import get_logger
from src.core._shared.infrrastrructure.auth.auth_interface import AuthServiceInterface


class JwtAuthService(AuthServiceInterface):
    def __init__(self, token: str = "") -> None:
        self.raw_public_key = os.getenv('AUTH_PUBLIC_KEY', None)
        self.public_key = f"-----BEGIN PUBLIC KEY-----\n{self.raw_public_key}\n-----END PUBLIC KEY-----"
        self.token = token.replace('Bearer ', '', 1)
        self.logger = get_logger(__name__)
        self.logger.debug(f'instância iniciada com {self.public_key}')
        
    def _decode_token(self) -> dict:
        try:
            return jwt.decode(self.token, self.public_key, algorithms=["RS256"], audience="account")
        except Exception as err:
            print(self.token)
            self.logger.error(f"Erro para para realizar decode do token {err}")
            return {}

    def is_authenticated(self) -> bool:
        return bool(self._decode_token())

    def has_role(self, role: str) -> bool:
        decode_token = self._decode_token()
        realm_access = decode_token.get("realm_access", {})
        roles = realm_access.get("roles", [])
        return role in roles