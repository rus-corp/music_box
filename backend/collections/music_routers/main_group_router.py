from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

from backend.database import get_db

from backend.collections import schemas
from backend.collections.music_handlers.main_group_handlers import MainGroupHandler
from backend.auth.security import get_current_user_from_token





router = APIRouter(
  prefix='/main_collection',
  # tags=['MainGroup']
)



@router.post('/group_collections', response_model=schemas.GroupCollectionShow,
             status_code=status.HTTP_201_CREATED)
async def create_collection(
  name: schemas.GroupCollectionCreate,
  session: AsyncSession = Depends(get_db),
  current_user: bool = Depends(get_current_user_from_token)
):
  if name.group_name == '' or name.group_name is None:
    raise HTTPException(status_code=400, detail='To create a group, need a name')
  main_group_handler = MainGroupHandler(session, current_user)
  created_group = await main_group_handler._create_collection_group(name.group_name)
  if created_group is not None:
    return created_group
  raise HTTPException(status_code=403, detail='Не получилось создать колекцию')




@router.get('/group_with_track_collections', response_model=List[schemas.GroupCollectionWithTrackCollectionShow],
            status_code=status.HTTP_200_OK)
async def get_collections_with_track_collections(
  session: AsyncSession = Depends(get_db),
  current_user: bool = Depends(get_current_user_from_token)
):
  main_group_handler = MainGroupHandler(session, current_user)
  group_collections = await main_group_handler._get_all_collection_groups(flag=True)
  return group_collections



@router.get('/group_without_track_collections', response_model=List[schemas.GroupCollectionShow])
async def get_group_collections_without_track_collections(
  session: AsyncSession = Depends(get_db),
  current_user: bool = Depends(get_current_user_from_token)
):
  main_group_handler = MainGroupHandler(session, current_user)
  group_collections = await main_group_handler._get_all_collection_groups()
  if group_collections is None:
    raise HTTPException(status_code=404, detail='Collectoin not found')
  return group_collections



@router.get('/group_collection/{group_id}', response_model=schemas.GroupCollectionShow)
async def get_group_collection_by_id_without_track_collections(
  group_id: int,
  session: AsyncSession = Depends(get_db),
  current_user: bool = Depends(get_current_user_from_token)
):
  main_group_handler = MainGroupHandler(session, current_user)
  group_collection = await main_group_handler._get_group_collelctions_by_id(group_id=group_id)
  return group_collection



@router.get('/group_collection_with_track_collection/{group_id}',response_model=schemas.GroupCollectionWithTrackCollectionShow)
async def get_group_collection_by_id_with_track_collections(
  group_id: int,
  session: AsyncSession = Depends(get_db),
  current_user: bool = Depends(get_current_user_from_token)
):
  main_group_handler = MainGroupHandler(session, current_user)
  group_collection = await main_group_handler._get_group_collelctions_by_id(
    group_id=group_id, flag=True
  )
  return group_collection



@router.patch('/group_collections', response_model=schemas.GroupCollectionShow)
async def update_collection(
  body: schemas.UpdateCollectiongroupRequest,
  session: AsyncSession = Depends(get_db),
  current_user: bool = Depends(get_current_user_from_token)
):
  main_group_handler = MainGroupHandler(session, current_user)
  updated_collection_group = await main_group_handler._update_group_collection(body)
  return updated_collection_group



@router.delete('/group_collection/{collection_id}', response_model=schemas.DeletedGroupResponse)
async def delete_group(
  collection_id: int,
  session: AsyncSession = Depends(get_db),
  current_user: bool = Depends(get_current_user_from_token)
):
  main_group_handler = MainGroupHandler(session, current_user)
  deleted_group_id = await main_group_handler._delete_group_collection_by_id(
    collection_id=collection_id
  )
  return deleted_group_id