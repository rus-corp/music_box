from sqlalchemy import select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from ..models import ClientGroup



class ClientGroupDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session


  async def create_client_group(self, name: str, comment: str):
    new_client_group = ClientGroup(
      name=name,
      comment=comment
    )
    self.db_session.add(new_client_group)
    await self.db_session.commit()
    return new_client_group


  async def get_all_client_groups_with_clients(self):
    query = select(ClientGroup).options(selectinload(ClientGroup.clients)).order_by(ClientGroup.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()


  async def get_only_clients_group(self):
    query = select(ClientGroup).order_by(ClientGroup.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()


  async def get_all_client_groups_with_users(self):
    query = select(ClientGroup).options(selectinload(ClientGroup.users)).order_by(ClientGroup.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()


  async def get_all_client_groups_with_clients_and_users(self):
    query = select(ClientGroup).options(selectinload(ClientGroup.clients), selectinload(ClientGroup.users)).order_by(ClientGroup.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()


  async def get_only_client_group_by_id(self, client_group_id: int):
    query = select(ClientGroup).where(ClientGroup.id == client_group_id)
    result = await self.db_session.execute(query)
    client_group = result.fetchone()
    if client_group is not None:
      return client_group[0]


  async def get_client_group_by_id_with_clients(self, client_group_id: int):
    query = select(ClientGroup).where(ClientGroup.id == client_group_id).options(selectinload(ClientGroup.clients))
    result = await self.db_session.execute(query)
    client_group = result.fetchone()
    if client_group is not None:
      return client_group[0]


  async def get_client_group_by_id_with_users(self, client_group_id: int):
    query = select(ClientGroup).where(ClientGroup.id == client_group_id).options(selectinload(ClientGroup.users))
    result = await self.db_session.execute(query)
    client_group = result.fetchone()
    if client_group is not None:
      return client_group[0]


  async def get_client_group_by_id_with_users_and_clients(self, client_group_id: int):
    query = select(ClientGroup).where(ClientGroup.id == client_group_id).options(selectinload(ClientGroup.clients), selectinload(ClientGroup.users))
    result = await self.db_session.execute(query)
    client_group = result.fetchone()
    if client_group is not None:
      return client_group[0]


  async def update_client_group_by_id(self, client_group_id: int, **kwargs):
    stmt = update(ClientGroup).where(ClientGroup.id == client_group_id).values(kwargs).returning(ClientGroup)
    result = await self.db_session.execute(stmt)
    updated_client_group = result.fetchone()
    if updated_client_group is not None:
      return updated_client_group[0]


  async def change_cluster_of_clients_group(self, client_group_id: int, new_client_cluster_id: int):
    stmt = update(ClientGroup).where(ClientGroup.id == client_group_id).values(client_cluster_id = new_client_cluster_id).returning(ClientGroup)
    result = await self.db_session.execute(stmt)
    updated_client_group = result.fetchone()
    if updated_client_group is not None:
      return updated_client_group[0]


  async def delete_client_group_by_id(self, client_group_id: int):
    try:
      stmt = delete(ClientGroup).where(ClientGroup.id == client_group_id).returning(ClientGroup.id)
      result = await self.db_session.execute(stmt)
      return result.scalar()
    except IntegrityError as e:
      error_message = 'Невозможно удалить ClientGroup из-за наличия зависимых записей.'
      return error_message
  
  
  async def add_user_to_client_group(self): pass
  
  
  async def delete_user_in_client_group(self): pass
  
  
  async def user_has_in_client_group(self): pass
  
  
  async def add_client_to_clientGroup(self): pass
  
  
  async def client_has_in_client_group(self): pass