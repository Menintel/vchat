"""Firebase Admin SDK initialization and token verification."""

import firebase_admin
from firebase_admin import auth, credentials
from fastapi import HTTPException, status

from app.core.config import get_settings

settings = get_settings()

# Initialize Firebase Admin SDK
_firebase_app = None


def get_firebase_app() -> firebase_admin.App:
    """Get or initialize the Firebase Admin app."""
    global _firebase_app

    if _firebase_app is None:
        try:
            # Try to get existing app
            _firebase_app = firebase_admin.get_app()
        except ValueError:
            # Initialize with service account if path is provided
            if settings.firebase_private_key_path:
                cred = credentials.Certificate(settings.firebase_private_key_path)
                _firebase_app = firebase_admin.initialize_app(cred)
            else:
                # Initialize with default credentials (for GCP environments)
                _firebase_app = firebase_admin.initialize_app()

    return _firebase_app


def verify_firebase_token(id_token: str) -> dict:
    """
    Verify a Firebase ID token and return the decoded claims.

    Args:
        id_token: The Firebase ID token from the frontend

    Returns:
        Decoded token claims containing uid, email, etc.

    Raises:
        HTTPException: If token is invalid or expired
    """
    # Ensure Firebase app is initialized
    get_firebase_app()

    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except auth.RevokedIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_user_by_uid(uid: str) -> auth.UserRecord:
    """Get Firebase user record by UID."""
    get_firebase_app()

    try:
        return auth.get_user(uid)
    except auth.UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
