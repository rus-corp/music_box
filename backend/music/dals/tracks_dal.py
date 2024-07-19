from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import selectinload

from ..models import Track, track_collection_tracks_association


class TrackDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session


  async def create_track(
    self,
    title: str,
    artist: str,
    label: str,
    open_name: str,
    path: str,
    album: str,
    genre: str
  ):
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
    return track_row


  async def update_track(self, track_id, **kwargs):
    stmt = update(Track).where(Track.id == track_id).values(kwargs).returning(Track)
    result = await self.db_session.execute(stmt)
    if result is not None:
      return result.fetchone[0]


  async def delete_track_by_id(self, track_id: int):
    stmt = delete(Track).where(Track.id == track_id).returning(Track.id)
    delete_track_row = await self.db_session.execute(stmt)
    await self.db_session.commit()
    if delete_track_row is not None:
      return True


  async def get_track_for_append_to_group(self, track_id: int):
    query = select(Track).where(Track.id == track_id).options(selectinload(Track.track_collections))
    result = await self.db_session.scalar(query)
    return result


  async def delete_track_from_collection(self, track_id: int, track_collection_id: int):
    stmt = delete(track_collection_tracks_association).where(
      and_(track_collection_tracks_association.c.track_collection_id == track_collection_id,
           track_collection_tracks_association.c.track_id == track_id)
    ).returning(track_collection_tracks_association.c.track_collection_id)
    result = await self.db_session.execute(stmt)
    deleted_track_in_collection = result.scalar()
    if deleted_track_in_collection is not None:
      return deleted_track_in_collection