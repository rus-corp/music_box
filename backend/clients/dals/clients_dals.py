from sqlalchemy import select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from ..models import Client, AnotherContracts, Currency



class ClientDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session


  async def create_client(self, name: str, full_name: str, certificate: str, contract_number: str,
                          contract_date, city: str, address: str, email: str, phone: str, price, currency: Currency, user_id: int) -> Client:
    new_client = Client(
      name=name,
      full_name=full_name,
      certificate=certificate,
      contract_number=contract_number,
      contract_date=contract_date,
      city=city,
      address=address,
      email=email,
      phone=phone,
      price=price,
      currency=currency,
      user_id=user_id
    )
    self.db_session.add(new_client)
    # await self.db_session.commit()
    return new_client


  async def create_client_for_add_to_user(self, name: str, full_name: str, certificate: str, contract_number: str,
                          contract_date, city: str, address: str, email: str, phone: str, price, currency: Currency, user_id: int):
    new_client = Client(
      name=name,
      full_name=full_name,
      certificate=certificate,
      contract_number=contract_number,
      contract_date=contract_date,
      city=city,
      address=address,
      email=email,
      phone=phone,
      price=price,
      currency=currency,
      user_id=user_id
    )
    self.db_session.add(new_client)
    return new_client


  async def get_all_clients(self):
    query = select(Client).order_by(Client.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()


  async def get_client_by_id(self, client_id):
    query = select(Client).where(Client.id == client_id)
    res = await self.db_session.execute(query)
    client_row = res.fetchone()
    if client_row is not None:
      return client_row[0]


  async def update_client_by_id(self, client_id, kwargs):
    stmt = update(Client).where(Client.id == client_id).values(**kwargs).returning(Client)
    result = await self.db_session.execute(stmt)
    updated_client = result.scalar()
    return updated_client


  async def get_client_for_append(self, client_id: int):
    query = select(Client).where(Client.id == client_id)
    client = await self.db_session.scalar(query)
    return client


  async def delete_client(self, client_id):
    stmt = delete(Client).where(Client.id == client_id)
    deleted_client = await self.db_session.execute(stmt)
    await self.db_session.commit()
    if deleted_client is not None:
      return True


  # async def check_group_access(self, user_id: int, client_group_id: int) -> bool:
  #   query = select(user_client_group_association).where(
  #     and_(user_client_group_association.user_id == user_id,
  #          user_client_group_association.client_group_id == client_group_id)
  #   )
  #   result = await self.db_session.execute(query)
  #   return result.scalar() is not None







