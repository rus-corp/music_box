import os
from typing import List, TYPE_CHECKING
from fastapi import APIRouter, File, UploadFile, Depends, status
from fastapi.responses import FileResponse, JSONResponse
import shutil
from pathlib import Path
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession



from ..collection_handlers.track_handlers import TrackHandler
from ..schemas import (TrackCreateResponse, TrackShow,
                       TrackUpdate, TrackCollectionWithTracks,
                       AppendTrackToCollection)
from backend.users.models import User
from backend.auth.security import get_current_user_from_token
from backend.general_schemas import ErrorMessageResponse
from ..service import FileProcessing
from backend.auth import errors

from backend.database import get_db


router = APIRouter(
  prefix='/tracks',
  tags=['Tracks']
)



@router.post('/upload', status_code=status.HTTP_201_CREATED, response_model=TrackCreateResponse)
async def upload_tracks(
  upload_files: List[UploadFile],
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  track_handler = TrackHandler(
    session, current_user, upload_files
  )
  created_track = await track_handler._create_track()
  return created_track



@router.get('/', response_model=List[TrackShow])
async def get_all_tracks(
  limit: int = 100,
  offset: int = 0,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  track_handler = TrackHandler(session, current_user)
  result = await track_handler._get_tracks(offset=offset, limit=limit)
  return result



@router.get('/{track_id}', response_model=TrackShow)
async def get_track_by_id(
  track_id: int,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  track_handler = TrackHandler(session, current_user)
  track = await track_handler._get_track_by_id(session=session, track_id=track_id)
  if track is None:
    raise HTTPException(status_code=404, detail=f'Track with id = {track_id} not found')
  return track



@router.patch('/{track_id}', response_model=TrackShow)
async def update_track(
  track_id: int,
  body: TrackUpdate,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  track_handler = TrackHandler(session, current_user)
  body_data = body.model_dump(exclude_none=True)
  if body_data == {}:
    raise HTTPException(status_code=403, detail='You need at least one parameter to change it')
  updated_track = await track_handler._update_track(
    session=session, track_id=track_id, body=body_data
  )
  return updated_track



@router.delete('/{track_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_track_by_id(
  track_id: int,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  track_handler = TrackHandler(session, current_user)
  deleted_track = await track_handler._delete_track_by_id(session=session, track_id=track_id)
  if deleted_track is None:
    raise HTTPException(status_code=404, detail='Track not found')
  return deleted_track



@router.post(
  '/append_track_to_collection',
  status_code=status.HTTP_201_CREATED,
  response_model=TrackCollectionWithTracks,
  responses={
    404: {'model': ErrorMessageResponse},
    400: {'model': ErrorMessageResponse}
  }
)
async def append_track_to_collection(
  body: AppendTrackToCollection,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  track_handler = TrackHandler(session, current_user)
  body_data = body.model_dump(exclude_none=True)
  if len(body_data) < 2:
    return errors.not_parameters
  result = await track_handler._append_track_to_collection(
    track_collection_id=body_data['track_collection_id'],
    track_id=body_data['track_id']
  )
  return result



@router.delete(
  '/delete_track_from_track_collection/{track_id}',
  response_model=ErrorMessageResponse,
  status_code=status.HTTP_200_OK
)
async def delete_track_from_collection(
  track_id: int,
  track_collection_id: int,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  # body_data = body.model_dump(exclude_none=True)
  # if len(body_data) < 2:
  #   return errors.not_parameters
  track_handler = TrackHandler(session, current_user)
  result = await track_handler._delete_track_from_collection(
    track_id=track_id, track_collection_id=track_collection_id
  )
  return result




# @router.post('')
# async def append_track_collection_to_client(
#   sesion: AsyncSession = Depends(get_db),
#   current_user = Depends(get_current_user_from_token)
# ):pass

# @router.delete('')
# async def delete_track_collection_from_client(
#   sesion: AsyncSession = Depends(get_db),
#   current_user = Depends(get_current_user_from_token)
# ):pass