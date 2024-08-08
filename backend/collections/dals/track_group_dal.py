from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, exists, and_
from sqlalchemy.orm import selectinload, joinedload


from backend.collections.models.models import TrackCollection
from backend.clients.models import trackCollections_client_association, Client, user_client_group_association
from backend.users.models import User



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
    new_track_collection = TrackCollection(
      name=name,
      player_option=player_option
    )
    self.db_sesion.add(new_track_collection)
    return new_track_collection


  async def get_track_collections_with_tracks_redactor(self):
    query = (select(TrackCollection)
             .options(selectinload(TrackCollection.tracks))
             .order_by(TrackCollection.id))
    result = await self.db_sesion.execute(query)
    return result.scalars().all()
  
  
  async def get_track_collections_with_tracks_client(self, user_id: int):
    query = (select(TrackCollection)
             .options(selectinload(TrackCollection.tracks))
             .join(trackCollections_client_association)
             .join(Client)
             .join(Client.client_group)
             .join(user_client_group_association)
             .join(User)
             .filter(User.id == user_id))
    result = await self.db_sesion.execute(query)
    return result.scalars().all()
  
  
  
  async def get_track_collection_by_id_with_tracks_redactor(
    self, track_group_id: int
  ):
    query = (select(TrackCollection).where(TrackCollection.id == track_group_id)
             .options(selectinload(TrackCollection.tracks)))
    result = await self.db_sesion.execute(query)
    track_group_row = result.fetchone()
    if track_group_row is not None:
      return track_group_row[0]
  
  
  
  async def get_track_collection_by_id_with_tracks_client(
    self, user_id: int, track_collection_id: int
  ):
    query = (select(TrackCollection)
             .where(TrackCollection.id == track_collection_id)
             .options(selectinload(TrackCollection.tracks))
             .join(trackCollections_client_association)
             .join(Client)
             .join(Client.client_group)
             .join(user_client_group_association)
             .join(User)
             .filter(User.id == user_id))
    result = await self.db_sesion.execute(query)
    collection_row = result.fetchone()
    if collection_row is not None:
      return collection_row[0]
  
  
  
  async def get_all_track_collections_redactor(self):
    query = select(TrackCollection).group_by(TrackCollection.id)
    res = await self.db_sesion.execute(query)
    return res.scalars().all()
  
  
  
  async def get_all_track_collections_client(self, user_id):
    query = (
      select(TrackCollection)
      .join(trackCollections_client_association)
      .join(Client)
      .join(Client.client_group)
      .join(user_client_group_association)
      .join(User)
      .filter(User.id == user_id)
      .order_by(TrackCollection.id)
    )
    result = await self.db_sesion.execute(query)
    return result.scalars().all()
  
  
  
  async def get_track_collection_by_id_redactor(self, track_collection_id: int):
    query = select(TrackCollection).where(TrackCollection.id == track_collection_id)
    res = await self.db_sesion.execute(query)
    track_collection_id_row = res.fetchone()
    if track_collection_id_row is not None:
      return track_collection_id_row[0]
  
  
  async def get_track_collection_by_id_client(self, track_collection_id: int, user_id: int):
    query = (
      select(TrackCollection)
      .where(TrackCollection.id == track_collection_id)
      .join(trackCollections_client_association)
      .join(Client)
      .join(Client.client_group)
      .join(user_client_group_association)
      .join(User)
      .filter(User.id == user_id)
    )
    result = await self.db_sesion.execute(query)
    collection_row = result.fetchone()
    if collection_row is not None:
      return collection_row[0]
  
  
  
  async def update_track_collection(self, track_collection_id, **kwargs):
    query = update(TrackCollection).where(
      TrackCollection.id == track_collection_id).values(kwargs).returning(TrackCollection)
    res = await self.db_sesion.execute(query)
    track_collection_row = res.fetchone()
    if track_collection_row is not None:
      return track_collection_row[0]
  
  
  
  async def delete_track_collection(self, track_collcetion_id: int):
    query = delete(TrackCollection).where(
      TrackCollection.id == track_collcetion_id).returning(TrackCollection.id)
    result = await self.db_sesion.execute(query)
    return result.scalar()
  
  
  async def get_track_collection_for_append_client(self, track_group_id: int):
    query = (select(TrackCollection)
             .where(TrackCollection.id == track_group_id)
             .options(selectinload(TrackCollection.clients)))
    result = await self.db_sesion.scalar(query)
    return result