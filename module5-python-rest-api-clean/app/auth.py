import secrets

DEMO_USERNAME = "student"
DEMO_PASSWORD = "module5"

_tokens = set()


def login(username: str, password: str):
    if secrets.compare_digest(username, DEMO_USERNAME) and secrets.compare_digest(
        password, DEMO_PASSWORD
    ):
        token = secrets.token_urlsafe(32)
        _tokens.add(token)
        return token
    return None


def is_valid_token(token: str | None) -> bool:
    return bool(token) and token in _tokens
