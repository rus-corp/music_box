from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse


from backend.auth import errors
from ..schemas import (CreateClient, ShowClientWithTrackColections, CurrencyShow, UpdateClientRequest,
                       UpdateClientResponse, ClientProfileCreateResponse, ClientProfileDefaultResponse)
from ..dals.clients_dals import ClientDAL
from ..dals.currency_dals import CurrencyDAL
from ..dals.client_profile_dal import ClientProfileDAL
from backend.music.dals.track_group_dal import TrackCollectionDAL
from backend.music.schemas import TrackCollectionShow
from backend.users.models import User



# ======================== CLIENT =============================

class ClientHandler:
  def __init__(self, session: AsyncSession, current_user: User= None) -> None:
    self.session: AsyncSession = session
    self.client_dal = ClientDAL(self.session)
    self.current_user = current_user
    self.roles = ['manager', 'client']
  
  
  async def _create_client(self, body: CreateClient):
    async with self.session.begin():
      currency_dal = CurrencyDAL(self.session)
      client_data = body.model_dump()
      currency_id = client_data.pop('currency_id', 1)
      currency_data = await currency_dal.get_currency_by_id(currency_id)
      if currency_data is None:
        return errors.not_Found_error
      
      profile_data = client_data.pop('profile')
      
      if profile_data is None:
        return JSONResponse(content='error profile', status_code=401)
      
      client_data.update(currency=currency_data)
      new_client = await self.client_dal.create_client(**client_data)
      
      client_profile_dal = ClientProfileDAL(self.session)
      client_profile = await client_profile_dal.create_client_profile(
        new_client.id, **profile_data
      )
      
      new_client.profile = client_profile
      await self.session.commit()
      
      client_profile_data = ClientProfileDefaultResponse(
        id=client_profile.id,
        full_name=client_profile.full_name,
        address=client_profile.address,
        certificate=client_profile.certificate,
        contract_number=client_profile.contract_number,
        contract_date=client_profile.contract_date
        
      )
      
      return ClientProfileCreateResponse(
        id=new_client.id,
        name=new_client.name,
        city=new_client.city,
        email=new_client.email,
        phone=new_client.phone,
        price=new_client.price,
        client_group_id=new_client.client_group_id,
        profile=client_profile_data
      )
  
  
  async def _get_all_clients_with_track_collecions(self):
    if self.current_user.is_superuser:
      clients = await self.client_dal.get_all_clients_with_profiles_and_track_collection_superuser()
    elif self.current_user.role.role_name in self.roles:
      clients = await self.client_dal.get_all_clients_with_profiles_and_track_collection_manager(
        user_id=self.current_user.id
      )
    else:
      return errors.access_denied_error
    return list(clients)
  
  
  async def _get_all_clients_with_client_groups(self):
    if self.current_user.is_superuser:
      clients = await self.client_dal.get_all_clients_with_client_group_superuser()
    elif self.current_user.role.role_name in self.roles:
      clients = await self.client_dal.get_all_clients_with_client_group_manager(
        user_id=self.current_user.id
      )
    else:
      return errors.access_denied_error
    return list(clients)
  
  
  async def _get_client_by_id_with_track_collecions(self, client_id: int):
    if self.current_user.is_superuser:
      client = await self.client_dal.get_client_with_track_collection_by_id_superuser(client_id)
    elif self.current_user.role.role_name in self.roles:
      client = await self.client_dal.get_client_with_track_collection_by_id_manager(
        client_id=client_id, user_id=self.current_user.id
      )
    else:
      return errors.access_denied_error
    if client is None:
      return errors.not_Found_error
    return client
  
  
  async def _get_client_by_id_with_client_group(self, client_id: int):
    if self.current_user.is_superuser:
      client_item = await self.client_dal.get_client_by_id_with_client_group_superuser(client_id)
    elif self.current_user.role.role_name in self.roles:
      client_item = await self.client_dal.get_client_by_id_with_client_group_manager(
        client_id=client_id, user_id=self.current_user.id
      )
    else:
      return errors.access_denied_error
    if client_item is None:
      return errors.relation_exist(user_id=self.current_user.id, client_group_id=client_id)
    return client_item
  
  
  async def _update_client_by_id(self, client_id: int, body: UpdateClientRequest):
    async with self.session.begin():
      body_data = body.model_dump(exclude_none=True)
      profile_data = body_data.pop('profile', None)
      client_data = await self.client_dal.check_client_in_db(client_id)
      
      if client_data is None:
        return errors.not_Found_error
      
      if profile_data is not None:
        client_profile_dal = ClientProfileDAL(self.session)
        updated_profile = await client_profile_dal.update_client_profile(
          client_id=client_data.id, body=profile_data
        )
        if updated_profile is None:
          return JSONResponse(
            content=f'Client Profile for client {client_data.id} no found',
            status_code=404
          )
          
      updated_client = await self.client_dal.update_client_by_id(
        client_id=client_data.id, kwargs=body_data
      )
      return updated_client
  
  
  async def _delete_client_group_by_id(self, client_id: int):
    async with self.session.begin():
      client_data = await self.client_dal.check_client_in_db(client_id)
      if client_data is None:
        return errors.not_Found_error
      deleted_client = await self.client_dal.delete_client(client_id)
      if deleted_client:
        return {'message': f'Client with id {client_id} deleted'}
  
  



