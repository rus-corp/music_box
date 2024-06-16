from sqlalchemy import select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.exc import IntegrityError

from ..models import ClientGroup, user_client_group_association
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
    return new_client_group


  async def get_only_clients_group_superuser(self):
    query = select(ClientGroup).order_by(ClientGroup.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()
  
  
  async def get_only_client_groups_manager(self, user_id: int):
    query = select(ClientGroup).join(user_client_group_association).join(User).filter(User.id == user_id)
    result = await self.db_session.execute(query)
    return result.scalars().all()
  
  
  async def get_client_groups_with_clients_superuser(self):
    query = select(ClientGroup).options(selectinload(ClientGroup.clients)).order_by(ClientGroup.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()
  
  async def get_client_groups_with_clients_manager(self, user_id: int):
    query = select(ClientGroup).join(user_client_group_association).join(User).options(joinedload(ClientGroup.clients)).filter(User.id == user_id).distinct()
    result = await self.db_session.execute(query)
    return result.scalars().all()
  
  # async def get_only_clients_group_manager(self, user_id: int):
  #   query = select(ClientGroup).options(joinedload(ClientGroup.users)).filter(ClientGroup.users.any_(
  #     User.id == user_id
  #   ))
  #   result = await self.db_session.execute(query)
  #   return result.scalars().all()


  async def get_all_client_groups_with_clients_superuser(self):
    query = select(ClientGroup).options(selectinload(ClientGroup.clients)).order_by(ClientGroup.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()
  
  
  async def get_all_client_groups_with_clients_manager(self, user_id: int):
    query = select(ClientGroup).join(user_client_group_association).join(User).filter(User.id == user_id)
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
    query = select(ClientGroup).where(
      and_(ClientGroup.id == client_group_id, ClientGroup.client_cluster_id == new_client_cluster_id)
    )
    result = await self.db_session.execute(query)
    if result.fetchone() is not None:
      stmt = update(ClientGroup).where(ClientGroup.id == client_group_id).values(client_cluster_id = new_client_cluster_id).returning(ClientGroup)
      result = await self.db_session.execute(stmt)
      updated_client_group = result.fetchone()
      if updated_client_group is not None:
        return updated_client_group[0]
    return 'Relationship exist'
    


  async def delete_client_group_by_id(self, client_group_id: int):
    try:
      stmt = delete(ClientGroup).where(ClientGroup.id == client_group_id).returning(ClientGroup.id)
      result = await self.db_session.execute(stmt)
      return result.scalar()
    except IntegrityError as e:
      error_message = 'Невозможно удалить ClientGroup из-за наличия зависимых записей.'
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