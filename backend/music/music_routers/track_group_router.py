from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from backend.database import get_db
from backend.music import schemas



from backend.auth.security import get_current_user_from_token

from backend.general_schemas import ErrorMessageResponse, ClientWithTrackCollection
from backend.music.music_handlers.track_group_handlers import TrackGroupCollectionHandler
from backend.users.models import User


router = APIRouter(
  prefix='/track_group',
  # tags=['TrackGroup']
)


@router.post('/',
             response_model=schemas.GroupCollectionWithTrackCollectionCreate,
             status_code=status.HTTP_201_CREATED, responses={
               400: {'model': ErrorMessageResponse},
               404: {'model': ErrorMessageResponse},
               405: {'model': ErrorMessageResponse}
             })
async def create_track_group_collection(
  body: schemas.TrackCollectionCreate,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  track_group_handler = TrackGroupCollectionHandler(session, current_user)
  created_track_collection = await track_group_handler._create_track_and_group_collections(body=body)
  return created_track_collection



@router.get('/', response_model=List[schemas.TrackCollectionShow])
async def get_all_track_collections_without_tracks(
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  track_group_handler = TrackGroupCollectionHandler(session, current_user)
  track_collections = await track_group_handler._get_track_collections_without_trakcs()
  return track_collections



@router.get('/{track_collection_id}', response_model=schemas.TrackCollectionShow, responses={
  404: {'model': ErrorMessageResponse}
})
async def get_track_collection_by_id_withouts_tracks(
  track_collection_id: int,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  track_group_handler = TrackGroupCollectionHandler(session, current_user)
  res = await track_group_handler._get_track_collection_by_id_without_trakcs(
    track_collection_id=track_collection_id
  )
  if res is None:
    raise HTTPException(
      status_code=404, detail=f'Track collection with id = {track_collection_id} not found'
    )
  return res



@router.get('/with_tracks', response_model=List[schemas.TrackCollectionWithTracks])
async def get_all_track_collection_with_tracks(
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  track_group_handler = TrackGroupCollectionHandler(session, current_user)
  track_collections = await track_group_handler._get_track_collections_with_tracks()
  return track_collections



@router.get('/with_tracks/{track_collection_id}', response_model=schemas.TrackCollectionWithTracks)
async def get_track_collection_by_id_with_trakcs(
  track_collection_id: int,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  track_group_handler = TrackGroupCollectionHandler(session, current_user)
  track_collection = await track_group_handler._get_track_collection_by_id_with_tracks(
    track_collection_id=track_collection_id
  )
  return track_collection




@router.patch('/{track_collection_id}', response_model=schemas.TrackCollectionShow, responses={
  404: {'model': ErrorMessageResponse}
})
async def update_track_collection(
  track_collection_id: int,
  body: schemas.TrackCollectionUpdateResponse,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  track_group_handler = TrackGroupCollectionHandler(session, current_user)
  updated_track_collection = await track_group_handler._update_track_collection(
    track_collection_id=track_collection_id, body=body
  )
  if updated_track_collection is None:
    raise HTTPException(
      status_code=404, detail=f'Track collection with id = {track_collection_id} not found'
    )
  return updated_track_collection


@router.delete('/{track_collection_id}', response_model=schemas.TrackCollectionDeleteResponse)
async def delete_track_collection(
  track_collection_id: int,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  track_group_handler = TrackGroupCollectionHandler(session, current_user)
  deleted_track_collection = await track_group_handler._delete_track_collection(
    session, track_collection_id
  )
  if deleted_track_collection is None:
    raise HTTPException(
      status_code=404, detail=f'Track collection with id = {track_collection_id} not found'
    )
  return deleted_track_collection



@router.post('/append_track_collection_to_client', status_code=status.HTTP_200_OK,
             response_model=ClientWithTrackCollection)
async def append_track_collection_to_client(
  body: schemas.AppendTrackCollectionToClient,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  track_group_handler = TrackGroupCollectionHandler(session, current_user)
  appended_track_collection = await track_group_handler._append_track_collection_to_client(
    body
  )
  return appended_track_collection
  

@router.delete('/delete_track_collection_from_client', status_code=status.HTTP_200_OK,
               response_model=ErrorMessageResponse)
async def delete_track_collection_from_client(
  body: schemas.AppendTrackCollectionToClient,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  track_group_handler = TrackGroupCollectionHandler(session, current_user)
  deleted_track_collection = await track_group_handler._delete_track_collection_from_client(
    body
  )
  return deleted_track_collection


