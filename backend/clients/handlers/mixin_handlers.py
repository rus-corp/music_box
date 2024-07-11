from sqlalchemy.ext.asyncio import AsyncSession

from backend.users.dals import UserDAL
from backend.clients.dals.client_group_dals import ClientGroupDAL




class ClientGroupMixins:
  session: AsyncSession
  
  async def get_user_from_db(self, user_id: int):
    user_dal = UserDAL(self.session)
    user = await user_dal.get_scalar_user(user_id)
    return user
  
  async def get_client_group_from_db(self, client_group_id: int):
    client_group_dal = ClientGroupDAL(self.session)
    client_group = await client_group_dal.get_scalar_client_group_by_id(client_group_id)
    return client_group