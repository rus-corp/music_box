from sqlalchemy import select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.exc import IntegrityError

from ..models import Client, AnotherContracts, Currency
from ..models import user_client_group_association
from backend.users.models import User



class ClientDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session
  
  
  async def check_client_in_db(self, client_id: int):
    query = select(Client).where(Client.id == client_id)
    result = await self.db_session.execute(query)
    return result.scalar()
    
    
  async def create_client(self, name: str, city: str, email: str, phone: str,
                          price, currency: Currency, client_group_id: int) -> Client:
    new_client = Client(
      name=name,
      city=city,
      email=email,
      phone=phone,
      price=price,
      currency=currency,
      client_group_id=client_group_id
      
    )
    self.db_session.add(new_client)
    await self.db_session.flush()
    return new_client
  
  
  async def get_all_clients_with_profiles_and_track_collection_superuser(self):
    query = select(Client).options(joinedload(Client.track_collections)).order_by(Client.id)
    result = await self.db_session.execute(query)
    return result.unique().scalars().all()
  
  
  async def get_all_clients_with_profiles_and_track_collection_manager(self, user_id: int):
    query = select(Client).options(selectinload(Client.track_collections)).join(Client.client_group).join(user_client_group_association).join(User).filter(User.id == user_id)
    result = await self.db_session.execute(query)
    return result.unique().scalars().all()
  
  
  async def get_all_clients_with_client_group_superuser(self):
    query = select(Client).options(joinedload(Client.client_group)).order_by(Client.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()
  
  
  async def get_all_clients_with_client_group_manager(self, user_id: int):
    query = select(Client).options(joinedload(Client.client_group))\
      .join(Client.client_group)\
        .join(user_client_group_association)\
          .join(User)\
            .filter(User.id == user_id)
    result = await self.db_session.execute(query)
    return result.scalars().all()
  
  
  async def get_client_with_track_collection_by_id_superuser(self, client_id: int):
    query = select(Client).where(Client.id == client_id).options(joinedload(Client.client_group), selectinload(Client.track_collections))
    result = await self.db_session.execute(query)
    client_row = result.fetchone()
    if client_row is not None:
      return client_row[0] 
  
  
  async def get_client_with_track_collection_by_id_manager(self, client_id: int, user_id: int):
    query = select(Client).options(selectinload(Client.track_collections))\
      .join(Client.client_group)\
        .join(user_client_group_association)\
          .join(User)\
            .filter(and_(User.id == user_id, Client.id == client_id))
    result = await self.db_session.execute(query)
    client_row = result.fetchone()
    if client_row is not None:
      return client_row[0]
  
  
  async def get_client_by_id_with_client_group_superuser(self, client_id: int):
    query = select(Client).options(joinedload(Client.client_group)).where(Client.id == client_id)
    result = await self.db_session.execute(query)
    client_row = result.fetchone()
    if client_row is not None:
      return client_row[0]
  
  
  async def get_client_by_id_with_client_group_manager(self, client_id: int, user_id: int):
    query = select(Client).options(joinedload(Client.client_group))\
      .join(Client.client_group)\
        .join(user_client_group_association)\
          .join(User)\
            .filter(and_(User.id == user_id, Client.id == client_id))
    result = await self.db_session.execute(query)
    client_row = result.fetchone()
    if client_row is not None:
      return client_row[0]
  
  
  async def update_client_by_id(self, client_id: int, kwargs: dict):
    stmt = update(Client).where(Client.id == client_id).values(**kwargs).returning(Client)
    result = await self.db_session.execute(stmt)
    updated_client = result.fetchone()
    if updated_client is not None:
      return updated_client[0]
  
  
  async def delete_client(self, client_id):
    stmt = delete(Client).where(Client.id == client_id)
    deleted_client = await self.db_session.execute(stmt)
    await self.db_session.commit()
    if deleted_client is not None:
      return True
  
  
  async def get_client_for_append(self, client_id: int):
    query = select(Client)\
      .where(Client.id == client_id)\
      .options(selectinload(Client.track_collections))
    client = await self.db_session.scalar(query)
    return client



  # async def check_group_access(self, user_id: int, client_group_id: int) -> bool:
  #   query = select(user_client_group_association).where(
  #     and_(user_client_group_association.user_id == user_id,
  #          user_client_group_association.client_group_id == client_group_id)
  #   )
  #   result = await self.db_session.execute(query)
  #   return result.scalar() is not None







