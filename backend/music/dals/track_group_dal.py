from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, exists, and_
from sqlalchemy.orm import selectinload

from backend.music.models import TrackCollection
from backend.clients.models import trackCollections_client_association




class TrackCollectionDAL:
  def __init__(self, db_sesion: AsyncSession) -> None:
    self.db_sesion = db_sesion
  
  
  async def collection_has_client(self, track_collection_id: int) -> bool:
    query = select(exists().where(
      trackCollections_client_association.c.track_collection_id == track_collection_id
    ))
    result = await self.db_sesion.execute(query)
    has_client = result.scalar()
    return has_client
  
  
  
  async def create_track_collection(self, name: str, player_option: bool) -> TrackCollection:
    new_track_collcetion = TrackCollection(
      name=name,
      player_option=player_option
    )
    self.db_sesion.add(new_track_collcetion)
    return new_track_collcetion
  
  
  async def get_track_collection_by_id(self, track_collection_id: int):
    query = select(TrackCollection).where(TrackCollection.id == track_collection_id)
    res = await self.db_sesion.execute(query)
    track_collection_id_row = res.fetchone()
    if track_collection_id_row is not None:
      return track_collection_id_row[0]
  
  
  async def get_track_collections_with_tracks(self):
    query = select(TrackCollection).options(selectinload(TrackCollection.tracks)).order_by(TrackCollection.id)
    result = await self.db_sesion.execute(query)
    return result.scalars().all()
  
  
  async def get_all_track_collections(self):
    query = select(TrackCollection).group_by(TrackCollection.id)
    res = await self.db_sesion.execute(query)
    return res.scalars().all()
  
  
  async def get_track_group_by_id_with_tracks(self, track_group_id: int):
    query = select(TrackCollection).where(TrackCollection.id == track_group_id).options(selectinload(TrackCollection.tracks))
    result = await self.db_sesion.execute(query)
    track_group_row = result.fetchone()
    if track_group_row is not None:
      return track_group_row[0]
  
  
  async def update_track_collection(self, track_collection_id, **kwargs):
    query = update(TrackCollection).where(
      TrackCollection.id == track_collection_id).values(kwargs).returning(TrackCollection.name)
    res = await self.db_sesion.execute(query)
    track_collection_row = res.fetchone()
    if track_collection_row is not None:
      return track_collection_row[0]
  
  
  async def delete_track_collection(self, track_collcetion_id: int):
    query = delete(TrackCollection).where(
      TrackCollection.id == track_collcetion_id).returning(TrackCollection.id)
    res = await self.db_sesion.execute(query)
    deleted_track_collcetion_row = res.fetchone()
    if deleted_track_collcetion_row is not None:
      return deleted_track_collcetion_row[0]
    
    
  async def delete_client_in_group_collection(self, track_collection_id, client_id):
    stmt = delete(trackCollections_client_association).where(
      and_(trackCollections_client_association.c.track_collection_id == track_collection_id,
           trackCollections_client_association.c.client_id == client_id)
    )
    result = await self.db_sesion.execute(stmt)
    deleted_client_in_trackcollection = result.rowcount
    if deleted_client_in_trackcollection is not None:
      return deleted_client_in_trackcollection
    
  
  async def get_track_collection_for_append_track_to_group(self, track_group_id: int):
    query = select(TrackCollection).where(TrackCollection.id == track_group_id).options(selectinload(TrackCollection.tracks))
    result = await self.db_sesion.scalar(query)
    return result