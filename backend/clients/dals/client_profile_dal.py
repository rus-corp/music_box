from sqlalchemy.ext.asyncio import AsyncSession


from ..schemas import ClientProfileBase

from ..models import ClientProfile



class ClientProfileDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session
  
  
  async def create_client_profile(self, client_id: int, address, full_name, certificate, contract_number, contract_date):
    new_profile = ClientProfile(
      address=address,
      full_name=full_name,
      certificate=certificate,
      contract_number=contract_number,
      contract_date=contract_date,
      client_id=client_id
    )
    
    self.db_session.add(new_profile)
    await self.db_session.flush()
    return new_profile
  
  
  async def get_cliene_profile(self):pass
  
  async def update_client_profile(self, body):pass
  
  
  async def delete_client_profile_by_id(self, profile_id): pass