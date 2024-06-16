import datetime
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

from config import SECRET_KEY, ALGORITHM
from backend.database import get_db
from backend.users.handlers import UserHandler
from backend.users.models import User
from .permissions import Permissions



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



# Проверка что юзер авторизован
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
    if email is None:
      raise credentials_exceptions
  except JWTError:
    raise credentials_exceptions
  user_handler = UserHandler(session)
  user = await user_handler._get_user_by_email(email=email)
  if user is None:
    raise credentials_exceptions
  return user



async def super_user_permission(current_user: User = Depends(get_current_user_from_token)):
  permission = Permissions(current_user=current_user)
  super_user = await permission.superuser_permission()
  if super_user:
    return True
  return False



async def has_manager_permissions(current_user: User = Depends(get_current_user_from_token)):
  permission = Permissions(current_user=current_user)
  manager_permission = await permission.manager_permission()
  if manager_permission:
    return True
  return False



async def has_redactor_permissions(current_user: User = Depends(get_current_user_from_token)):
  permission = Permissions(current_user=current_user)
  redactor_permission = await permission.redactor_permission()
  if redactor_permission:
    return True
  return False



async def has_client_permission(current_user: User = Depends(get_current_user_from_token)):
  permission = Permissions(current_user=current_user)
  client_permission = await permission.client_permission()
  if client_permission:
    return True
  return False