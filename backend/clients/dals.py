from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


from .models import Client, Currency, AnotherContracts



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
    await self.db_session.commit()
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
    query = select(Client)
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


# =================== Currency ========================
class CurrencyDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session
  
  
  async def create_currency(self, name):
    new_currency = Currency(cur_name=name)
    self.db_session.add(new_currency)
    await self.db_session.flush()
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
    deleted_currency = await self.db_session.execute(stmt)
    await self.db_session.commit()
    if deleted_currency is not None:
      return True


# =================== Anoteher Contract ========================
class ClientGroupDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session
  
  async def create_client_group(self): pass
  
  async def get_all_client_groups(self): pass
  
  async def get_client_group_by_id(self): pass
  
  async def update_client_group_by_id(self): pass
  
  
  async def delete_client_group(self): pass



class ClientClusterDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session

  async def create_group_claster(self): pass
  
  
  async def get_all_client_clusters(self):pass
  
  
  async def get_client_cluster_by_id(self): pass
  
  
  async def update_client_cluster(self): pass
  
  
  async def delete_client_cluster(self): pass