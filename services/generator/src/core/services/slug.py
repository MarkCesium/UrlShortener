import string
import secrets


class SlugService:
    _alphabet = string.ascii_letters + string.digits

    def generate(self) -> str:
        return "".join(secrets.choice(self._alphabet) for _ in range(6))
