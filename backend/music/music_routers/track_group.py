from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException


from backend.database import get_db
from backend.music import schemas


from backend.music.music_handlers.track_group_handlers import (_get_track_collections,
                       _get_track_collection_by_id, _update_track_collection,
                       _delete_track_collection, _create_track_and_group_collections,
                       _append_track_to_collection)




router = APIRouter(
  prefix='/track_group',
  # tags=['TrackGroup']
)


@router.post('/track_group_collections', response_model=schemas.GroupCollectionWithTrackCollectionCreate,
             responses={
  404: {'desc': 'group collection not found'}
})
async def create_track_group_collection(body: schemas.TrackCollectionCreate,
                                        session: AsyncSession = Depends(get_db)):
  if body.track_collection_name == None or body.track_collection_name == '':
    raise HTTPException(status_code=400, detail='To create a group, need a name')
  created_track_collection = await _create_track_and_group_collections(session=session, body=body)
  if created_track_collection is None:
    raise HTTPException(status_code=403, detail='Track collection has not been created')
  return created_track_collection
    
    
@router.get('/track_group_collections', response_model=List[schemas.TrackCollectionShow])
async def get_track_collections(session: AsyncSession = Depends(get_db)):
  res = await _get_track_collections(session)
  if res is None:
    raise HTTPException(status_code=404, detail='Track collections not found')
  return res


@router.get('/track_collections/{track_collection_id}', response_model=schemas.TrackCollectionShow)
async def get_track_collection_by_id(track_collection_id: int,
                                     session: AsyncSession = Depends(get_db)):
  res = await _get_track_collection_by_id(
    session=session, track_collection_id=track_collection_id
  )
  if res is None:
    raise HTTPException(
      status_code=404, detail=f'Track collection with id = {track_collection_id} not found'
    )
  return res


@router.patch('/track_collections/{track_collection_id}', response_model=schemas.TrackCollectionShow)
async def update_track_collection(track_collection_id: int,
                                  body: schemas.TrackCollectionUpdateResponse,
                                  session: AsyncSession = Depends(get_db)):
  if body.model_dump(exclude_none=True) == {}:
    HTTPException(status_code=422, detail='At least one parameter is needed to change the collection')
  updated_track_collection = await _update_track_collection(
    session=session, track_collection_id=track_collection_id, body=body
  )
  if updated_track_collection is None:
    raise HTTPException(
      status_code=404, detail=f'Track collection with id = {track_collection_id} not found'
    )
  return updated_track_collection


@router.delete('/track_collections/{track_collection_id}', response_model=schemas.TrackCollectionDeleteResponse)
async def delete_track_collection(track_collection_id: int,
                                  session: AsyncSession = Depends(get_db)):
  deleted_track_collection = await _delete_track_collection(
    session, track_collection_id
  )
  if deleted_track_collection is None:
    raise HTTPException(
      status_code=404, detail=f'Track collection with id = {track_collection_id} not found'
    )
  return deleted_track_collection





@router.post('/append_track_to_collection')
async def append_track_to_collection(track_id: int, track_collection_id: int, session: AsyncSession = Depends(get_db)):
  res = await _append_track_to_collection(session=session, track_collection_id=track_collection_id, track_id=track_id)
  return res