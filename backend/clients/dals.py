from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


from .models import Client, Currency, AnotherContracts



class ClientDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session
    
    
  async def create_client(self, name: str, full_name: str, certificate: str, contract_number: str,
                          contract_date, city: str, address: str, email: str, phone: str, price) -> Client:
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
      price=price
    )
    self.db_session.add(new_client)
    await self.db_session.commit()
    return new_client
  
  
  async def get_clients(self):
    query = select(Client)
    res = await self.db_session.execute(query)
    return res.all()
  
  
  async def get_user_by_id(self, id):
    query = select(Client).where(Client.client_id == id)
    res = await self.db_session.execute(query)
    client_row = res.fetchone()
    if client_row is not None:
      return client_row[0]
    
    
  async def get_client_for_append(self, client_id: int):
    query = select(Client).where(Client.id == client_id)
    client = await self.db_session.scalar(query)
    return client
    
  
  
  async def update_client(self, client_id):
    pass
  
    
  async def delete_client(self, client_id):
    pass
  
  
# =================== Currency ========================
class CurrenctDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session
  
  
  async def create_currency(self, name):
    new_currency = Currency(cur_name=name)
    await self.db_session.add(new_currency)
    return new_currency
  
  
  async def get_all_currency(self):
    query = select(Currency).order_by(Currency.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()
  
  
  async def get_currency_by_id(self, currency_id: int):
    query = select(Currency).where(Currency.id == currency_id)
    currency = await self.db_session.scalar(query)
    return currency
  
  
  async def update_currency(self, currency_id: int, new_name: str):
    stmt = update(Currency).where(Currency.id == currency_id).values(
      new_name).returning(Currency)
    result = await self.db_session.execute(stmt)
    currency = result.fetchone()
    if currency is not None:
      return currency[0]
    
    
  async def delete_currency_by_id(self, currency_id):
    stmt = delete(Currency).where(Currency.id == currency_id).returning(Currency.id)
    result = await self.db_session.execute(stmt)
    await self.db_session.commit()
    deleted_currency = result.fetchone()
    if deleted_currency is not None:
      return deleted_currency[0]
    
  
  
  
  
  
  
# =================== Anoteher Contract ========================