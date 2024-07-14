from sqlalchemy import select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload, aliased
from sqlalchemy.exc import IntegrityError

from ..models import ClientGroup, user_client_group_association, Client
from backend.users.models import User



class ClientGroupDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session


  async def create_client_group(self, name: str, client_cluster_id: int, comment: str = None):
    new_client_group = ClientGroup(
      name=name,
      comment=comment,
      client_cluster_id=client_cluster_id
    )
    self.db_session.add(new_client_group)
    await self.db_session.commit()
    return new_client_group


  async def get_only_clients_group_superuser(self):
    query = select(ClientGroup).order_by(ClientGroup.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()
  
  
  async def get_only_client_groups_manager(self, user_id: int):
    query = select(ClientGroup).join(user_client_group_association).join(User).filter(User.id == user_id)
    result = await self.db_session.execute(query)
    return result.scalars().all()
  
  
  async def get_client_group_by_id_superuser(self, group_id: int):
    query = select(ClientGroup).where(ClientGroup.id == group_id)
    result = await self.db_session.scalar(query)
    return result
    
    
  async def get_client_group_by_id_manager(self, group_id: int, user_id: int):
    query = select(ClientGroup).join(user_client_group_association).join(User).filter(and_(User.id == user_id, ClientGroup.id == group_id))
    result = await self.db_session.execute(query)
    client_group_row = result.fetchone()
    if client_group_row is not None:
      return client_group_row[0]
  
  
  async def get_all_client_groups_with_clients_superuser(self):
    query = select(ClientGroup).options(joinedload(ClientGroup.clients)).order_by(ClientGroup.id)
    result = await self.db_session.execute(query)
    return result.unique().scalars().all()
  
  
  async def get_all_client_groups_with_clients_manager(self, user_id: int):
    query = select(ClientGroup).options(joinedload(ClientGroup.clients))\
      .join(user_client_group_association)\
        .join(User)\
          .filter(User.id == user_id)
    result = await self.db_session.execute(query)
    return result.unique().scalars().all()
  
  
  async def get_client_group_by_id_with_clients_superuser(self, client_group_id: int):
    query = select(ClientGroup).where(ClientGroup.id == client_group_id).options(joinedload(ClientGroup.clients))
    result = await self.db_session.execute(query)
    client_group = result.unique().fetchone()
    if client_group is not None:
      return client_group[0]
  
  
  async def get_client_group_by_id_with_clients_manager(self, group_id: int, user_id: int):
    query = select(ClientGroup)\
      .options(joinedload(ClientGroup.clients))\
        .join(user_client_group_association)\
          .join(User)\
            .filter(and_(ClientGroup.id == group_id, User.id == user_id))
    result = await self.db_session.execute(query)
    client_group = result.unique().fetchone()
    if client_group is not None:
      return client_group[0]
  
  
  async def update_client_group_by_id(self, client_group_id: int, kwargs):
    stmt = update(ClientGroup).where(ClientGroup.id == client_group_id).values(kwargs).returning(ClientGroup)
    result = await self.db_session.execute(stmt)
    updated_client_group = result.fetchone()
    if updated_client_group is not None:
      return updated_client_group[0]
    


  async def delete_client_group_by_id(self, client_group_id: int):
    try:
      stmt = delete(ClientGroup).where(ClientGroup.id == client_group_id).returning(ClientGroup.id)
      result = await self.db_session.execute(stmt)
      await self.db_session.commit()
      return result.scalar()
    except IntegrityError as e:
      error_message = 'Невозможно удалить ClientGroup из-за наличия зависимых записей.'
      await self.db_session.rollback()
      return error_message


  async def get_scalar_client_group_by_id(self, client_group_id: int):
    query = select(ClientGroup).where(ClientGroup.id == client_group_id).options(joinedload(ClientGroup.users))
    result = await self.db_session.execute(query)
    return result.scalar()


  async def get_user_client_groups_with_clients(self, user_id: int):
    query = select(user_client_group_association).where(
      user_client_group_association.c.user_id == user_id
    )
    result = await self.db_session.execute(query)
    result_row = result.fetchone()
    if result is not None:
      return result_row[0]


  # async def clients_user(self, user_id: int):
  #   query = select(user_client_group_association).where(
  #     user_client_group_association.c.user_id == user_id
  #   )
  #   result = await self.db_session.execute(query)
  #   result_row = result.fetchone()
  #   if result is not None:
  #     return result_row[0]


  async def add_user_to_client_group(self): pass
  
  
  async def delete_user_in_client_group(self): pass
  
  
  async def user_has_in_client_group(self): pass
  
  
  async def add_client_to_clientGroup(self): pass
  
  
  async def client_has_in_client_group(self): pass
  
  async def delete_client_in_client_group(self): pass