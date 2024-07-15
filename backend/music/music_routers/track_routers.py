import os
from typing import List, TYPE_CHECKING
from fastapi import APIRouter, File, UploadFile, Depends, status
from fastapi.responses import FileResponse
import shutil
from pathlib import Path
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession



from ..music_handlers.track_handlers import (_create_track, _get_tracks, _get_track_by_id,
                                             _update_track, _delete_track_by_id)
from ..schemas import TrackCreateResponse, TrackShow, TrackUpdate

  
  
from ..service import read_file_tags, write_file, rename_file_name
from backend.database import get_db


router = APIRouter(
  prefix='/tracks',
  tags=['Tracks']
)



@router.post('/upload', response_model=TrackCreateResponse, status_code=status.HTTP_201_CREATED)
async def upload_tracks(upload_files: List[UploadFile],
                        session: AsyncSession = Depends(get_db)):
  tracks = {'error_tracks': [], 'created_tracks': []}
  media_directory = Path(__file__).resolve().parent.parent.parent / 'media'
  print(media_directory)
  for file in upload_files:
    file_open_name = await rename_file_name(file.filename)
    file.filename = file.filename.lower()
    file_path = os.path.join(media_directory, file.filename)
    writed_files = await write_file(file_name=file_path, file=file)
    tags_data = await read_file_tags(file_path=file_path, file_name=file_open_name)
    if 'exceptions_errors' in tags_data:
      os.remove(file_path)
      tracks['error_tracks'].append(tags_data['exceptions_errors'])
    tags_data.update({'path': file_path, 'open_name': file_open_name})
    created_track = await _create_track(session=session, body=tags_data)
    try:
      if 'IntegrityError' in created_track:
        error_message = created_track.split('DETAIL:')[1].split('.\n[SQL:')[0]
        tracks['error_tracks'].append(error_message)
    except:
      tracks['created_tracks'].append(file_open_name)
  response_data = TrackCreateResponse(error_tracks=tracks['error_tracks'], created_tracks=tracks['created_tracks'])
  return response_data



@router.get('/', response_model=List[TrackShow])
async def get_all_tracks(limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_db)):
  result = await _get_tracks(offset=offset, limit=limit, session=session)
  return result


@router.get('/{track_id}', response_model=TrackShow)
async def get_track_by_id(track_id: int, session: AsyncSession = Depends(get_db)):
  track = await _get_track_by_id(session=session, track_id=track_id)
  if track is None:
    raise HTTPException(status_code=404, detail=f'Track with id = {track_id} not found')
  return track


@router.patch('/{track_id}', response_model=TrackShow)
async def update_track(track_id: int, body: TrackUpdate, session: AsyncSession = Depends(get_db)):
  body_data = body.model_dump(exclude_none=True)
  if body_data == {}:
    raise HTTPException(status_code=403, detail='You need at least one parameter to change it')
  updated_track = await _update_track(
    session=session, track_id=track_id, body=body_data
  )
  return updated_track


@router.delete('/{track_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_track_by_id(track_id: int, session: AsyncSession = Depends(get_db)):
  deleted_track = await _delete_track_by_id(session=session, track_id=track_id)
  if deleted_track is None:
    raise HTTPException(status_code=404, detail='Track not found')
  return deleted_track


