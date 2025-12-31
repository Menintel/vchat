"""API dependencies for authentication and common utilities."""

from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from app.core.firebase import verify_firebase_token


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
) -> dict:
    """
    Dependency to get the current authenticated user from Firebase token.

    Expects Authorization header in format: "Bearer <token>"

    Returns:
        Decoded Firebase token claims containing:
        - uid: User's unique ID
        - email: User's email (if available)
        - name: User's display name (if available)
        - picture: User's photo URL (if available)
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract token from "Bearer <token>" format
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Use 'Bearer <token>'",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = parts[1]
    return verify_firebase_token(token)


# Type alias for dependency injection
CurrentUser = Annotated[dict, Depends(get_current_user)]


async def get_optional_user(
    authorization: Annotated[str | None, Header()] = None,
) -> dict | None:
    """
    Dependency to optionally get the current user.
    Returns None if no valid token is provided.
    """
    if not authorization:
        return None

    try:
        return await get_current_user(authorization)
    except HTTPException:
        return None


# Type alias for optional user dependency
OptionalUser = Annotated[dict | None, Depends(get_optional_user)]
