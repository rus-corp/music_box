from typing import TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncSession

from backend.users.models import User

from ..dals.client_cluster_dals import ClientClusterDAL
from ..dals.client_group_dals import ClientGroupDAL
from backend.auth.errors import not_Found_error, access_denied_error
from backend.users.dals import UserDAL



from ..schemas import (ClientGroupShow, ClientGroupCreateRequest, ClientGroupCreateResponse, ClientClusterShow,
                      ClientGroupUpdateRequset, ClientGroupUpdateResponse, ClientClusterShow, CleintGroupDeleteMessage, ClientGroupDeleteResponse)
from backend.general_schemas import ClientGroup_WithUsers
from backend.users.schemas import UserShowForClient




class ClientGroupHandler:
  def __init__(self, session: AsyncSession, current_user: User = None) -> None:
    self.session = session
    self.client_group_dal = ClientGroupDAL(self.session)
    self.current_user = current_user
    self.roles = ['client', 'manager']
  
  async def _create_client_group(self, name: str, comment: str, client_cluster_id: int):
    client_group_cerated = await self.client_group_dal.create_client_group(
      name=name, comment=comment, client_cluster_id=client_cluster_id
    )
    return client_group_cerated


  async def _create_client_group_take_client_cluster(self, body: ClientGroupCreateRequest):
    async with self.session.begin():
      client_cluster_dal = ClientClusterDAL(self.session)
      model_data = body.model_dump(exclude_none=True)
      client_cluster = await client_cluster_dal.get_client_cluster_for_client_group(
        client_cluster_id=model_data.get('client_cluster_id')
      )
      if client_cluster is None:
        return not_Found_error
      client_group = await self._create_client_group(
        name=model_data['name'],
        comment=model_data.get('comment'),
        client_cluster_id=model_data.get('client_cluster_id')
      )
      client_cluster_schema = ClientClusterShow(
        id=client_cluster.id,
        name=client_cluster.name
      )
      client_group_schema = ClientGroupCreateResponse(
        id=client_group.id,
        name=client_group.name,
        comment=client_group.comment,
        client_cluster=client_cluster_schema
      )
      return client_group_schema
  
  
  
  async def _get_only_clients_group(self,):
    async with self.session.begin():
      if self.current_user.is_superuser:
        client_groups = await self.client_group_dal.get_only_clients_group_superuser()
      elif self.current_user.role.role_name in self.roles:
        client_groups = await self.client_group_dal.get_only_client_groups_manager(user_id=self.current_user.id)
      else:
        return access_denied_error
      return list(client_groups)
  
  
  
  async def _get_only_client_group_by_id(self, client_group_id: int):
    async with self.session.begin():
      if self.current_user.is_superuser:
        client_group = await self.client_group_dal.get_client_group_by_id_superuser(client_group_id)
      elif self.current_user.role.role_name in self.roles:
        client_group = await self.client_group_dal.get_client_group_by_id_manager(
          group_id=client_group_id, user_id=self.current_user.id
        )
      else:
        return access_denied_error
      if client_group is None:
        return not_Found_error
      return client_group
  
  
  async def _get_all_client_groups_with_clients(self):
    if self.current_user.is_superuser:
      client_groups_data = await self.client_group_dal.get_all_client_groups_with_clients_superuser()
    elif self.current_user.role.role_name in self.roles:
      client_groups_data = await self.client_group_dal.get_all_client_groups_with_clients_manager(
        user_id=self.current_user.id
      )
    else:
      return access_denied_error
    return client_groups_data
  
  
  async def _get_client_group_by_id_with_clients(self, client_group_id: int):
    if self.current_user.is_superuser:
      cleint_group = await self.client_group_dal.get_client_group_by_id_with_clients_superuser(client_group_id)
    elif self.current_user.role.role_name in self.roles:
      cleint_group = await self.client_group_dal.get_client_group_by_id_with_clients_manager(
        group_id=client_group_id, user_id=self.current_user.id
      )
    else:
      return access_denied_error
    if cleint_group is None:
      return not_Found_error
    return cleint_group
  
  
  async def _update_client_group(self, client_group_id: int, body: ClientGroupUpdateRequset):
    async with self.session.begin():
      body_data = body.model_dump(exclude_none=True)
      client_group = await self.client_group_dal.get_client_group_by_id_superuser(
        group_id=client_group_id
      )
      if client_group is None:
        return not_Found_error
      updated_group = await self.client_group_dal.update_client_group_by_id(
        client_group_id=client_group_id, kwargs=body_data
      )
      client_cluster = ClientClusterShow(
        id=updated_group.client_cluster.id,
        name=updated_group.client_cluster.name
      )
      return ClientGroupUpdateResponse(
        id=updated_group.id,
        name=updated_group.name,
        comment=updated_group.comment,
        client_cluster=updated_group.client_cluster_id,
        old_client_cluster=client_cluster
      )
  
  
  async def _delete_client_group_by_id(self, client_group_id: int):
    async with self.session.begin():
      client_group = await self.client_group_dal.get_client_group_by_id_superuser(client_group_id)
      if client_group is None:
        return not_Found_error
      deleted_client_group = await self.client_group_dal.delete_client_group_by_id(client_group_id)
      if type(deleted_client_group) == str:
        return CleintGroupDeleteMessage(
          message=deleted_client_group
        )
      else:
        return ClientGroupDeleteResponse(
          id=deleted_client_group
        )
    
  
  
  
  
  
  # async def _get_all_client_groups_with_clients(self, current_user: User):
  #   async with self.session.begin():
  #     client_group_dal = ClientGroupDAL(self.session)
  #     if current_user.is_superuser:
  #       client_groups = await client_group_dal.get_all_client_groups_with_clients_superuser()
  #     elif current_user.role.role_name in self.roles:
  #       client_groups = await client_group_dal.get_all_client_groups_with_clients_manager(user_id=current_user.id)
  #     else:
  #       return access_denied_error
  #     return list(client_groups)


  # async def _get_all_client_groups_with_users(self, current_user: User):
  #   async with self.session.begin():
  #     client_group_dal = ClientGroupDAL(self.session)
  #     if current_user.is_superuser:
  #       client_groups = await client_group_dal.get_all_client_groups_with_users()
  #     elif current_user.role.role_name in self.roles:
  #       client_groups = await client_group_dal.get_all_client_groups_with_clients_and_users()
  #     return list(client_groups)







async def _get_all_client_groups_with_clients_and_users(session: AsyncSession):
  async with session.begin():
    client_group_dal = ClientGroupDAL(session)
    client_groups = await client_group_dal.get_all_client_groups_with_clients_and_users()
    return list(client_groups)





async def _get_client_group_by_id_with_clients(session: AsyncSession, client_group_id: int):
  async with session.begin():
    client_group_dal = ClientGroupDAL(session)
    client_group = await client_group_dal.get_client_group_by_id_with_clients(client_group_id)
    return client_group


async def _get_client_group_by_id_with_users(session: AsyncSession, client_group_id: int):
  async with session.begin():
    client_group_dal = ClientGroupDAL(session)
    client_group = await client_group_dal.get_client_group_by_id_with_users(client_group_id)
    return client_group


async def _get_client_group_by_id_with_users_and_clients(session: AsyncSession, client_group_id: int):
  async with session.begin():
    client_group_dal = ClientGroupDAL(session)
    client_group = await client_group_dal.get_client_group_by_id_with_users_and_clients(client_group_id)
    return client_group








async def _change_cluster_of_clients_group(session: AsyncSession, client_group_id: int, new_client_cluster_id: int) -> ClientGroupShow:
  async with session.begin():
    client_group_dal = ClientGroupDAL(session)
    client_cluster_dal = ClientClusterDAL(session)
    has_client_group = await client_group_dal.get_only_client_group_by_id(client_group_id)
    has_client_cluster = client_cluster_dal.get_all_client_clusters_without_client_groups(new_client_cluster_id)
    if has_client_group is None or has_client_cluster is None:
      return not_Found_error
    changed_cluster_of_client_group = await client_group_dal.change_cluster_of_clients_group(
      client_group_id=client_group_id,
      new_client_cluster_id=new_client_cluster_id
    )
    return changed_cluster_of_client_group


async def _append_user_to_client_group(session: AsyncSession, client_group_id: int, user_id: int):
  async with session.begin():
    client_group_dal = ClientGroupDAL(session)
    user_dal = UserDAL(session)
    client_group = await client_group_dal.get_scalar_client_group_by_id(client_group_id)
    user = await user_dal.get_scalar_user(user_id)
    if client_group is None or user is None:
      return not_Found_error
    user.client_groups.append(client_group)
    await session.flush()
    
  users = [UserShowForClient(
    id=user.id,
    name=user.name,
    comment=user.comment,
    login=user.comment,
    email=user.email,
    is_active=user.is_active,
    is_superuser=user.is_superuser
  )]
  client_group_show = ClientGroup_WithUsers(
    id=client_group.id,
    name=client_group.name,
    comment=client_group.comment,
    users=users
  )
  return client_group_show
