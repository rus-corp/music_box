import eyed3
from fastapi import UploadFile
import aiofiles



async def read_file_tags(file_path):
  audiofile = eyed3.load(file_path)
  artist = audiofile.tag.artist
  album = audiofile.tag.album
  title = audiofile.tag.title
  try:
    label = audiofile.tag.label
  except:
    label = 'Track has not label'
    
  return {
    'title': title,
    'artist': artist,
    'album': album,
    'label': label,
    'path': file_path 
  }
  
  
async def write_file(file_name: str, file: UploadFile):
  async with aiofiles.open(file_name, 'wb') as buffer:
    data = await file.read()
    await buffer.write(data)
    return data