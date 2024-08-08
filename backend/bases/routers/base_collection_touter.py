from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.auth.security import get_current_user_from_token
from backend.users.models import User
from backend.general_schemas import ErrorMessageResponse



from ..handlers.base_collection_handler import BaseCollectionHandler
from .. import schemas

router = APIRouter(
  prefix='/collection',
  tags=['BaseCollection']
)

@router.post(
  '/',
  status_code=status.HTTP_201_CREATED,
  response_model=schemas.ShowBaseCollection
)
async def create_base_collection(
  body: schemas.BaseCollectionCreateRequest,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  collection_handler = BaseCollectionHandler(
    session=session, current_user=current_user
  )
  new_collection = await collection_handler._create_base_collection(
    body=body
  )
  return new_collection


@router.get(
  '/',
  status_code=status.HTTP_200_OK,
  response_model=schemas.ShowBaseCollection
)
async def get_all_base_collections(
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  collection_handler = BaseCollectionHandler(
    session=session, current_user=current_user
  )
  base_collections = await collection_handler._get_all_base_collections()
  return base_collections


@router.get