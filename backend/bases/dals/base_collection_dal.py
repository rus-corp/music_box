from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload, selectinload


from ..models import BaseCollection



class BaseCollectionDAL:
  def __init__(self, session: AsyncSession) -> None:
    self.db_session = session
  
  
  async def create_base_collection(self, name: int, base_id: int):
    new_collection = BaseCollection(
      name=name,
      main_base_id=base_id
    )
    self.db_session.add(new_collection)
    await self.db_session.commit()
    return new_collection
  
  
  async def get_all_base_collections(self):
    query = select(BaseCollection).order_by(BaseCollection.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()
  
  
  async def get_collection_by_id(self, collection_id: int):
    query = select(BaseCollection).where(BaseCollection.id == collection_id)
    result = await self.db_session.execute(query)
    collection_row = result.fetchone()
    if collection_row is not None:
      return collection_row[0]
  
  
  async def get_collection_by_id_with_tracks(self, collection_id: int):
    query = (select(BaseCollection)
             .where(BaseCollection.id == collection_id)
             .options(selectinload(BaseCollection.tracks)))
    result = await self.db_session.execute(query)
    collection_row = result.fetchone()
    if collection_row is not None:
      return collection_row[0]
  
  
  async def update_collection_by_id(self, collection_id: int, values):
    stmt = (update(BaseCollection)
            .where(BaseCollection.id == collection_id)
            .values(values)).returning(BaseCollection)
    result = await self.db_session.execute(stmt)
    updated_row = result.fetchone()
    if updated_row is not None:
      return updated_row[0]
  
  
  async def delete_collection_by_id(self, collection_id: int):
    stmt = delete(BaseCollection).where(BaseCollection.id == collection_id).returning(BaseCollection.id)
    result = await self.db_session.execute(stmt)
    return result.scalar()