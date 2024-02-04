from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

from backend.database import get_db

from backend.music import schemas
from backend.music.music_handlers.main_group_handlers import (_create_collection_group, _get_collcetions_group_all_with_track_collections, _get_collection_by_id,
                       _update_collection_group, _delete_collection_group, _get_group_collections_without_track_collections, _get_group_coll_by_id_with_track_collections)






router = APIRouter(
  prefix='/main_group',
  # tags=['MainGroup']
)

@router.post('/group_collections', response_model=schemas.GroupCollectionShow)
async def create_collection(group_name: schemas.GroupCollectionCreate, session: AsyncSession = Depends(get_db)):
  if group_name.group_name == '' or group_name.group_name is None:
    raise HTTPException(status_code=400, detail='To create a group, need a name')
  created_group = await _create_collection_group(session, group_name)
  if created_group is not None:
    return created_group
  raise HTTPException(status_code=403, detail='Не получилось создать колекцию')


@router.get('/group_track_collections', response_model=List[schemas.GroupCollectionWithTrackCollectionShow])
async def get_collections_with_track_collections(session: AsyncSession = Depends(get_db)):
  group_collections = await _get_collcetions_group_all_with_track_collections(session)
  if group_collections is None:
    raise HTTPException(status_code=404, detail='Collectoin not found')
  return group_collections


@router.get('/group_no_track_collections', response_model=List[schemas.GroupCollectionShow])
async def get_group_collections_without_track_collections(session: AsyncSession = Depends(get_db)):
  group_collections = await _get_group_collections_without_track_collections(session)
  if group_collections is None:
    raise HTTPException(status_code=404, detail='Collectoin not found')
  return group_collections


@router.get('/group_collection/{collection_id}', response_model=schemas.GroupCollectionShow)
async def get_group_collection_by_id_without_track_collections(collection_id: int, session: AsyncSession = Depends(get_db)):
  res = await _get_collection_by_id(session, collection_id=collection_id)
  if res is None:
    raise HTTPException(status_code=404, detail=f'Group collection with id = {collection_id} not found')
  return res


@router.get('/group_collection_with_track/{collection_id}',response_model=schemas.GroupCollectionWithTrackCollectionShow)
async def get_group_collection_by_id_with_track_collections(collection_id: int,session: AsyncSession = Depends(get_db)):
  group_collection = await _get_group_coll_by_id_with_track_collections(session=session, collection_id=collection_id)
  if group_collection is None:
    raise HTTPException(status_code=404, detail=f'Group collection with id = {collection_id} not found')
  return group_collection

@router.patch('/group_collection/{collection_id}', response_model=schemas.GroupCollectionShow)
async def update_collection(collection_id: int, name: str, session: AsyncSession = Depends(get_db)):
  if name:
    updated_collection_group = await _update_collection_group(session, collection_group_id=collection_id, name=name)
    if updated_collection_group is None:
      raise HTTPException(status_code=401, detail='The collection could not be changed')
    return updated_collection_group
  raise HTTPException(status_code=403, detail='For change the collection, need new name')


@router.delete('/group_collection/{collection_id}', response_model=schemas.DeletedGroupResponse)
async def delete_group(collection_id: int, session: AsyncSession = Depends(get_db)):
  deleted_group_id = await _delete_collection_group(session=session, collection_id=collection_id)
  if deleted_group_id is None:
    raise HTTPException(status_code=404, detail=f'Group with id = {collection_id} not found')
  return deleted_group_id