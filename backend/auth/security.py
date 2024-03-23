import datetime
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

from config import SECRET_KEY, ALGORITHM
from backend.database import get_db
from backend.users.handlers import _get_user_by_email

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')




def create_access_token(data: dict, expires_delta: timedelta = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=30)
  to_encode.update({'exp': expire})
  enoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
  return enoded_jwt



async def get_current_user_from_token(
  token: str = Depends(oauth_scheme),
  session: AsyncSession = Depends(get_db)
):
  credentials_exceptions = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials'
  )
  try:
    payload = jwt.decode(
      token, SECRET_KEY, algorithms=[ALGORITHM]
    )
    email: str = payload.get('sub')
    print(email)
    if email is None:
      raise credentials_exceptions
  except JWTError:
    raise credentials_exceptions
  user = await _get_user_by_email(session=session, email=email)
  if user is None:
    raise credentials_exceptions
  return user