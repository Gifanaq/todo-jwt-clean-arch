from typing import cast

from passlib.context import CryptContext

from src.domain.interfaces.security.password_hasher import PasswordHasher


class Pbkdf2PasswordHasher(PasswordHasher):
    def __init__(self) -> None:
        self._context = CryptContext(
            schemes=["pbkdf2_sha256"],
            deprecated="auto",
            pbkdf2_sha256__rounds=600_000,
        )

    def hash(self, password: str) -> str:
        return cast(str, self._context.hash(password))

    def verify(self, password: str, password_hash: str) -> bool:
        return cast(bool, self._context.verify(password, password_hash))
