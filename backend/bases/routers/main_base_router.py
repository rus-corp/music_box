from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse


from backend.database import get_db
from backend.auth.security import get_current_user_from_token
from backend.users.models import User
from backend.general_schemas import ErrorMessageResponse

from ..handlers.main_base_handler import MainBaseHandler
from .. import schemas


router = APIRouter(
  tags=['MainBase']
)


@router.post(
  '/main_bases',
  status_code=status.HTTP_201_CREATED,
  response_model=schemas.ShowBase
)
async def create_main_base(
  body: schemas.CreateBase,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  if body.name == '':
    return JSONResponse(
      content='Имя не может быть пустым', status_code=403
    )
  base_handler = MainBaseHandler(
    session, current_user
  )
  new_base = await base_handler._create_main_base(body.name)
  return new_base



@router.get(
  '/main_bases',
  status_code=status.HTTP_200_OK,
  response_model=List[schemas.ShowBase]
)
async def get_all_bases_without_collection(
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  base_handler = MainBaseHandler(
    session, current_user
  )
  bases = await base_handler._get_all_bases(flag=False)
  return bases



@router.get(
  '/main_bases/with_collections',
  status_code=status.HTTP_200_OK,
  response_model=List[schemas.ShowBaseWithCollection]
)
async def get_all_bases_with_collections(
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  base_handler = MainBaseHandler(
    session, current_user
  )
  bases = await base_handler._get_all_bases(flag=True)
  return bases



@router.get(
  '/main_bases/{base_id}',
  status_code=status.HTTP_200_OK,
  response_model=schemas.ShowBase
)
async def get_base_by_id(
  base_id: int,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  base_handler = MainBaseHandler(
    session, current_user
  )
  base = await base_handler._get_base_by_id(
    base_id=base_id, flag=False
  )
  return base



@router.get(
  '/main_bases/with_collection/{base_id}',
  status_code=status.HTTP_200_OK,
  response_model=schemas.ShowBaseWithCollection
)
async def get_base_by_id_with_collection(
  base_id: int,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  base_handler = MainBaseHandler(
    session, current_user
  )
  base = await base_handler._get_base_by_id(
    base_id=base_id, flag=True
  )
  return base



@router.patch(
  '/main_bases/{base_id}',
  status_code=status.HTTP_200_OK,
  response_model=schemas.ShowBase
)
async def update_base_by_id(
  base_id: int,
  name: str,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  base_handler = MainBaseHandler(
    session, current_user
  )
  updated_base = await base_handler._update_base_by_id(
    base_id=base_id, new_name=name
  )
  return updated_base



@router.delete(
  '/main_bases/{base_id}',
  status_code=status.HTTP_200_OK,
  response_model=schemas.DeletedBase,
  responses={
    400:{'model': ErrorMessageResponse},
    404: {'model': ErrorMessageResponse}
  }
)
async def delete_base_by_id(
  base_id: int,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  base_handler = MainBaseHandler(
    session, current_user
  )
  deleted_base = await base_handler._delete_base_dy_id(
    base_id
  )
  return deleted_base