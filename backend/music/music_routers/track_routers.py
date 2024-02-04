import os
from typing import List, TYPE_CHECKING
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import FileResponse
import shutil
from os import path

from sqlalchemy.ext.asyncio import AsyncSession



from ..music_handlers.track_handlers import (_create_track,)


  
  
from ..service import read_file_tags, write_file
from backend.database import get_db


router = APIRouter(
  prefix='/tracks',
  tags=['Tracks']
)



@router.post('/upload')
async def upload_tracks(upload_files: List[UploadFile],
                        session: AsyncSession = Depends(get_db)):
  created_tracks_list = []
  for file in upload_files:
    file.filename = file.filename.lower()
    open_name = file.filename.split('-')
    print(open_name[0])
    # file_path = f'/Users/ruslanprusakov/project/music_box/backend/media/{file.filename}'
    # writed_files = await write_file(file_name=file_path, file=file)
    # tags_data = await read_file_tags(file_path)
    # tags_data.update({'path': file_path})
    # created_track = await _create_track(session=session, body=tags_data)
    # created_tracks_list.append(created_track)
    

  # if upload_file.content_type == 'mp3':
  #   background_task.add_task()
  # with open(file_path, 'wb+') as buffer:
  #   shutil.copyfileobj(upload_file.file, buffer)
    
  # data = await read_file_tags(file_path)
  
    
    
  return {'created_tracks': created_tracks_list}