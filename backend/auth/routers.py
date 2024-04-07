from datetime import timedelta
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import Token
from .handlers import _authenticate_user
from .security import create_access_token
from backend.database import get_db
from config import ACCESS_TOKEN_EXPIRE_MINUTES


login_router = APIRouter(
  prefix='/auth',
  tags=['Auth']
)



@login_router.post('/token', response_model=Token, status_code=status.HTTP_201_CREATED)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
  user = await _authenticate_user(session=session, email=form_data.username, password=form_data.password)
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Incorrect password or email')
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
    data={'sub': user.email, 'role': user.role.role_name},
    expires_delta=access_token_expires
  )
  return {'access_token': access_token, 'token_type': 'bearer'}
