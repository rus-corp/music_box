from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from ..models import Track
from ..schemas import TrackCreate, TrackShow

class TrackDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session
    
  async def create_track(self, title: str,
                         artist: str, label: str,
                         open_name: str, path: str, album: str, genre: str):
    new_track = Track(
      title=title,
      artist=artist,
      label=label,
      open_name=open_name,
      file_path=path,
      album=album,
      genre=genre
    )
    try:
      self.db_session.add(new_track)
      await self.db_session.commit()
      return new_track
    except IntegrityError as er:
      return str(er)
  
  
  async def get_tracks(self, limit: int, offset: int):
    query = select(Track).offset(offset).limit(limit)
    result = await self.db_session.execute(query)
    return result.scalars().all()
  
  
  async def get_track_by_id(self, track_id: int):
    query = select(Track).where(Track.id == track_id)
    result = await self.db_session.execute(query)
    track_row = result.scalar()
    if track_row is not None:
      return track_row
  
  
  async def update_track(self, track_id, **kwargs):
    stmt = update(Track).where(Track.id == track_id).values(kwargs).returning(Track)
    result = await self.db_session.execute(stmt)
    if result is not None:
      return result.fetchone[0]
  
  
  async def delete_track_by_id(self, track_id: int):
    stmt = delete(Track).where(Track.id == track_id).returning(Track.id)
    result = await self.db_session.execute(stmt)
    await self.db_session.commit()
    delete_track_row = result.fetchone()
    if delete_track_row is not None:
      return delete_track_row[0]
  
  
  async def get_track_for_append_to_group(self, track_id: int):
    query = select(Track).where(Track.id == track_id).options(selectinload(Track.track_collections))
    result = await self.db_session.scalar(query)
    return result