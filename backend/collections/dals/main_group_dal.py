from sqlalchemy import select, delete, update, and_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from backend.collections.models.models import CollectionGroup


class CollectionGroupDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session
    
    
  async def create_collection_group(self, name: str) -> CollectionGroup:
    new_group_collection = CollectionGroup(
      group_name=name
    )
    self.db_session.add(new_group_collection)
    await self.db_session.commit()
    return new_group_collection
  
  
  async def get_all_group_collections_without_track_collections(self):
    query = select(CollectionGroup).order_by(CollectionGroup.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()
  
  
  async def get_all_group_collections_with_track_collections(self):
    query = select(CollectionGroup).options(joinedload(CollectionGroup.track_collections)).order_by(CollectionGroup.id)
    result = await self.db_session.execute(query)
    return result.unique().scalars().all()
  
  
  async def get_group_collection_by_id_without_track_collections(self, group_id: int):
    query = select(CollectionGroup).where(CollectionGroup.id == group_id)
    result = await self.db_session.execute(query)
    group_row = result.fetchone()
    if group_row is not None:
      return group_row[0]
  
  
  async def get_group_collection_by_id_with_track_collections(self, group_id: int):
    query = select(CollectionGroup).where(CollectionGroup.id == group_id).options(joinedload(CollectionGroup.track_collections))
    result = await self.db_session.execute(query)
    group_row = result.fetchone()
    if group_row is not None:
      return group_row[0]
  
  
  
  async def update_collection_group(self, collection_group_id: int, name: str):
    stmt = update(CollectionGroup).where(CollectionGroup.id == collection_group_id).values({'group_name':name}).returning(CollectionGroup)
    res = await self.db_session.execute(stmt)
    await self.db_session.commit()
    update_collcetion_group_row = res.fetchone()
    if update_collcetion_group_row is not None:
      return update_collcetion_group_row[0]
  
  
  async def delete_collection_group(self, collection_id):
    try:
      query = delete(CollectionGroup).where(CollectionGroup.id == collection_id).returning(CollectionGroup.id)
      res = await self.db_session.execute(query)
      await self.db_session.commit()
      return res.scalar()
    except IntegrityError as e:
      error_message = 'Невозможно удалить CollectionGroup из-за наличия зависимых записей в TrackCollection.'
  
  
  async def get_collection_group_for_track_collection(self, group_collection_id: int):
    """Для создания группы и подгруппы"""
    query = select(CollectionGroup).where(CollectionGroup.id == group_collection_id).options(selectinload(CollectionGroup.track_collections))
    res = await self.db_session.scalar(query)
    return res
  
  
  # async def delete_track_group_in_main_group(
  #   self,
  #   old_main_grop_id: int,
  #   track_collection_group_id: int) -> int:
  #   stmt = delete(group_track_collection_association).where(
  #     and_(group_track_collection_association.c.group_collection_id == old_main_grop_id,
  #          group_track_collection_association.c.track_collection_id == track_collection_group_id)
  #   ).returning(group_track_collection_association.c.group_collection_id)
  #   result = await self.db_session.execute(stmt)
  #   deleted_relationship = result.scalar()
  #   if deleted_relationship is not None:
  #     return deleted_relationship
    