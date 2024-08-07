import os
import eyed3
from fastapi import UploadFile
import aiofiles
from pathlib import Path
import os


from mutagen import File
from mutagen.id3 import ID3




class FileProcessing:
  def __init__(self, file) -> None:
    self.file = file
    self.media_directory = Path(__file__).resolve().parent.parent / 'media'
  
  
  async def read_file_tags(self, file_path, file_name: str):
    audiofile = File(file_path, easy=True)
    exceptions_errors = {}
    exceptions_errors.update({'file': file_name})
    try:
      artist = audiofile['artist']
    except Exception as ar:
      exceptions_errors.update({'name': str(ar)})
    try:
      album = audiofile['album']
    except Exception as al:
      exceptions_errors.update({'album': str(al)})
    try:
      title = audiofile['title']
    except Exception as ti:
      exceptions_errors.update({'title': str(ti)})
    try:
      genre = audiofile['genre']
    except Exception as ge:
      exceptions_errors.update({'genre': str(ge)})
    try:
      label = audiofile['artist']
    except Exception as pu:
      exceptions_errors.update({'label': str(pu)})
    
    errors_len = len(exceptions_errors)
    if errors_len >= 2:
      return {'exceptions_errors': exceptions_errors}
    
    return {
      'title': title[0],
      'artist': artist[0],
      'album': album[0],
      'label': label[0],
      'path': file_path,
      'genre': genre[0],
      'open_name': file_name
    }

  
  
  async def write_file(self, file_name: str, file: UploadFile):
    async with aiofiles.open(file_name, 'wb') as buffer:
      data = await file.read()
      await buffer.write(data)
      return data
  
  
  async def rename_file_name(self, file_name: str):
    new_file_name = file_name.replace('_', ' ')
    return new_file_name
  
  
  # tracks = {'error_tracks': [], 'created_tracks': []}
  async def file_proc(self):
    file_open_name = await self.rename_file_name(self.file.filename)
    file_filename = self.file.filename.lower()
    file_path = os.path.join(self.media_directory, self.file.filename)
    writed_files = await self.write_file(file_name=file_path, file=self.file)
    tags_data = await self.read_file_tags(file_path=file_path, file_name=file_open_name)
    if 'exceptions_errors' in tags_data:
      os.remove(file_path)
    return tags_data
  
  
  #     tracks['error_tracks'].append(tags_data['exceptions_errors'])
  # tags_data.update({'path': file_path, 'open_name': file_open_name})
  # return (tags_data, tracks)