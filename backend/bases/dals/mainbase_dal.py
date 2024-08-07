from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

from ..models import MainBase



class MainBaseDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session
  
  
  async def create_main_base(self, name: str):
    new_base = MainBase(name=name)
    self.db_session.add(new_base)
    await self.db_session.commit()
    return new_base
  
  
  async def get_all_main_base(self):
    query = select(MainBase).order_by(MainBase.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()
  
  
  async def get_all_main_base_with_collection(self):
    query = select(MainBase).options(joinedload(MainBase)).order_by(MainBase.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()
    
  
  async def get_main_base_by_id_without_collection(self, main_group_id: int):
    query = select(MainBase).where(MainBase.id == main_group_id)
    result = await self.db_session.execute(query)
    group_row = result.fetchone()
    if group_row is not None:
      return group_row[0]
  
  async def get_main_base_by_id_with_collection(self, main_group_id: int):
    query = select(MainBase).where(MainBase.id == main_group_id).options(joinedload(MainBase.collection))
    result = await self.db_session.execute(query)
    group_row = result.fetchone()
    if group_row is not None:
      return group_row[0]
  
  
  async def update_main_base(self, main_group_id: int, new_name: str):
    stmt = update(MainBase).where(MainBase.id == main_group_id).values(name=new_name).returning(MainBase)
    result = await self.db_session.execute(stmt)
    group_row = result.fetchone()
    if group_row is not None:
      return group_row[0]
  
  
  async def delete_main_base(self, main_group_id: int):
    try:
      stmt = delete(MainBase).where(MainBase.id == main_group_id)
      result = await self.db_session.execute(stmt)
      await self.db_session.commit()
      return result.scalar()
    except IntegrityError:
      error_message = 'Невозможно удалить Main Base из-за наличия зависимых записей в BaseCollection'
