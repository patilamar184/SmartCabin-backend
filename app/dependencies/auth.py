import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import SECRET_KEY, ALGORITHM
from app.database.database import get_db
from app.models.owner import Owner
from app.models.admin import Admin



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/owner/login"
)


def get_current_owner(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        owner_id = payload.get("sub")
        role = payload.get("role")

        if owner_id is None or role != "owner":
            raise credentials_exception

    except jwt.InvalidTokenError:
        raise credentials_exception

    owner = db.query(Owner).filter(
        Owner.id == int(owner_id)
    ).first()

    if not owner or not owner.is_active:
        raise credentials_exception

    return owner

def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired admin token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        admin_id = payload.get("sub")
        role = payload.get("role")

        if admin_id is None or role != "admin":
            raise credentials_exception

        admin_id = int(admin_id)

    except (jwt.InvalidTokenError, ValueError):
        raise credentials_exception

    admin = db.query(Admin).filter(
        Admin.id == admin_id
    ).first()

    if not admin or not admin.is_active:
        raise credentials_exception

    return admin