from datetime import timezone, timedelta, datetime

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from psycopg.types import none
from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db import get_session
from app.models.tokens import Token
from app.models.user import User
from app.service.user_service import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
secret_key = "super secret key"
algorithm = "HS256"
access_token_lifetime_minutes = 15
refresh_token_lifetime_days = 7
credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

async def refresh_tokens(token: str, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_token(token, session)

    query = select(Token).where(Token.user_id == user.id)
    result = await session.execute(query)
    db_tokens = result.scalars().all()

    matched_token = None
    for db_token in db_tokens:
        db_hash_token = db_token.refresh_token_hashed.encode('utf-8')
        if  bcrypt.checkpw(db_hash_token, token.encode('utf-8')):
            matched_token = db_token
            break

    if matched_token is None:
        raise credentials_exception

    await session.delete(matched_token)
    return await reg_log_token_rotation(user, session)

def create_access_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=access_token_lifetime_minutes)
    to_encode = ({"sub": email, "exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

def create_refresh_token(email: str) -> tuple[str, datetime]:
    expire = datetime.now(timezone.utc) + timedelta(days=refresh_token_lifetime_days)
    to_encode = ({"sub": email, "exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt, expire

async def reg_log_token_rotation(user: User, session: AsyncSession):
    access_token = create_access_token(user.email)
    refresh_token, expires_at = create_refresh_token(user.email)

    refresh_token_hashed = "todo: hashing of refresh token"
    new_token = Token(
        user_id=user.id,
        expires_at=expires_at,
        refresh_token_hashed=refresh_token
    )
    session.add(new_token)
    await session.commit()
    await session.refresh(new_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

async def get_user_by_token(token: str, session: AsyncSession = Depends(get_session)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        email: str = payload.get("sub")
        if email is none:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is expired",
        )
    except jwt.InvalidTokenError:
        raise credentials_exception

    user_data = await get_user_by_email(email, session)

    if user_data is none:
        raise credentials_exception

    return user_data