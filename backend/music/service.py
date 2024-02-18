import eyed3
from fastapi import UploadFile
import aiofiles



async def read_file_tags(file_path, file_name: str):
  audiofile = eyed3.load(file_path)
  exceptions_errors = {}
  exceptions_errors.update({'file': file_name})
  try:
    artist = audiofile.tag.artist
  except Exception as ar:
    exceptions_errors.update({'name': str(ar)})
  try:
    album = audiofile.tag.album
  except Exception as al:
    exceptions_errors.update({'album': str(al)})
  try:
    title = audiofile.tag.title
  except Exception as ti:
    exceptions_errors.update({'title': str(ti)})
  try:
    genre = audiofile.tag.genre.name
  except Exception as ge:
    exceptions_errors.update({'genre': str(ge)})
  try:
    label = audiofile.tag.publisher
  except Exception as pu:
    exceptions_errors.update({'label': str(pu)})
  
  errors_len = len(exceptions_errors)
  if errors_len >= 2:
    return {'exceptions_errors': exceptions_errors}
  
  return {
    'title': title,
    'artist': artist,
    'album': album,
    'label': label,
    'path': file_path,
    'genre': genre
  }
  
  
async def write_file(file_name: str, file: UploadFile):
  async with aiofiles.open(file_name, 'wb') as buffer:
    data = await file.read()
    await buffer.write(data)
    return data
  
  
async def rename_file_name(file_name: str):
  new_file_name = file_name.replace('_', ' ')
  return new_file_name