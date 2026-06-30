from fastapi import Header, HTTPException, status

ADMIN_KEY = "campus-admin-123"


def verify_admin_key(x_admin_key: str | None = Header(default=None)) -> None:
    """Validate admin API key from request header."""
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Invalid admin key",
        )
