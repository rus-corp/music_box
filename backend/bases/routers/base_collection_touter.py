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
  response_model=List[schemas.ShowBaseCollection]
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


@router.get(
  '/{collection_id}',
  status_code=status.HTTP_200_OK,
  response_model=schemas.ShowBaseCollection
)
async def get_base_collection_by_id(
  collection_id: int,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  collection_handler = BaseCollectionHandler(
    session=session, current_user=current_user
  )
  base_collection = await collection_handler._get_base_collection_by_id(
    collection_id=collection_id
  )
  return base_collection



@router.get(
  '/with_tracks/{collection_id}',
  status_code=status.HTTP_200_OK,
  # response_model=schemas.
)
async def get_base_collection_with_tracks(
  collection_id: int,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  collection_handler = BaseCollectionHandler(
    session=session, current_user=current_user
  )
  base_collection = await collection_handler._get_base_collection_by_id_with_tracks(
    collection_id=collection_id
  )
  return base_collection


@router.patch(
  '/{collection_id}',
  status_code=status.HTTP_200_OK,
)
async def update_base_collection_by_id(
  collection_id: int,
  body: schemas.BaseCollectionUpdateRequest,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  collection_handler = BaseCollectionHandler(
    session=session, current_user=current_user
  )
  updated_collection = await collection_handler._update_base_collection(
    collection_id=collection_id, body=body
  )
  return updated_collection