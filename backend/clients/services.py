from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from .models import Client



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
  
  async def update_client(self, client_id):
    pass
    
  async def delete_client(self, client_id):
    pass
  
  
  