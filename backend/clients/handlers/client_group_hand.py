from typing import TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncSession

from backend.users.models import User

from ..dals.client_cluster_dals import ClientClusterDAL
from ..dals.client_group_dals import ClientGroupDAL
from backend.auth.errors import not_Found_error, access_denied_error
from backend.users.dals import UserDAL



from ..schemas import (ClientGroupShow, ClientGroupCreate, ClientGroupUpdate)
from backend.general_schemas import ClientGroup_WithUsers
from backend.users.schemas import UserShowForClient




class ClientGroupHandler:
  def __init__(self, session: AsyncSession, current_user: User = None) -> None:
    self.session = session
    self.current_user = current_user
    self.roles = ['client', 'manager']
  
  async def _create_client_group(self, client_group_dal: ClientGroupDAL, name: str, comment: str):
    client_group_cerated = await client_group_dal.create_client_group(name=name, comment=comment)
    return client_group_cerated


  async def _create_client_group_take_client_cluster(self, body: ClientGroupCreate):
    async with self.session.begin():
      client_cluster_dal = ClientClusterDAL(self.session)
      client_group_dal = ClientGroupDAL(self.session)
      model_data = body.model_dump(exclude_none=True)
      client_cluster = await client_cluster_dal.get_client_cluster_for_client_group(
        client_cluster_id=model_data.pop('client_cluster_id')
      )
      if client_cluster is None:
        return not_Found_error
      client_group = await self._create_client_group(
        client_group_dal=client_group_dal,
        name=model_data['name'],
        comment=model_data.get('comment', '')
      )
      client_cluster.client_groups.append(client_group)
      await self.session.commit()
      
      client_group_schema = ClientGroupShow(
        id=client_group.id,
        name=client_group.name,
        comment=client_group.comment
      )
      # return ClientClusterShow_With_ClientGroups(
      #   id=client_cluster.id,
      #   name=client_cluster.name,
      #   client_groups=client_group_schema
      # )


  async def _get_only_clients_group(self):
    async with self.session.begin():
      client_group_dal = ClientGroupDAL(self.session)
      if self.current_user.is_superuser:
        client_groups = await client_group_dal.get_only_clients_group_superuser()
      elif self.current_user.role.role_name in self.roles:
        client_groups = await client_group_dal.get_only_client_groups_manager(user_id=self.current_user.id)
      else:
        return access_denied_error
      return list(client_groups)
  
  
  async def _get_client_groups_with_clients(self):
    async with self.session.begin():
      client_group_dal = ClientGroupDAL(self.session)
      if self.current_user.is_superuser:
        client_groups = await client_group_dal.get_client_groups_with_clients_superuser()
      elif self.current_user.role.role_name in self.roles:
        client_groups = await client_group_dal.get_client_groups_with_clients_manager(user_id=self.current_user.id)
      else:
        return access_denied_error
      return list(client_groups)
      






  async def _get_all_client_groups_with_clients(self, current_user: User):
    async with self.session.begin():
      client_group_dal = ClientGroupDAL(self.session)
      if current_user.is_superuser:
        client_groups = await client_group_dal.get_all_client_groups_with_clients_superuser()
      elif current_user.role.role_name in self.roles:
        client_groups = await client_group_dal.get_all_client_groups_with_clients_manager(user_id=current_user.id)
      else:
        return access_denied_error
      return list(client_groups)


  async def _get_all_client_groups_with_users(self, current_user: User):
    async with self.session.begin():
      client_group_dal = ClientGroupDAL(self.session)
      if current_user.is_superuser:
        client_groups = await client_group_dal.get_all_client_groups_with_users()
      elif current_user.role.role_name in self.roles:
        client_groups = await client_group_dal.get_all_client_groups_with_clients_and_users()
      return list(client_groups)







async def _get_all_client_groups_with_clients_and_users(session: AsyncSession):
  async with session.begin():
    client_group_dal = ClientGroupDAL(session)
    client_groups = await client_group_dal.get_all_client_groups_with_clients_and_users()
    return list(client_groups)


async def _get_only_client_group_by_id(session: AsyncSession, client_group_id: int):
  async with session.begin():
    client_group_dal = ClientGroupDAL(session)
    client_group = await client_group_dal.get_only_client_group_by_id(client_group_id)
    return client_group


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


async def _update_client_group_by_id(session: AsyncSession, body: ClientGroupUpdate):
  async with session.begin():
    client_group_dal = ClientGroupDAL(session)
    model_data = body.model_dump(exclude_none=True)
    client_group = await client_group_dal.get_only_client_group_by_id(model_data['id'])
    if client_group is None:
      return not_Found_error
    updated_client_group = await client_group_dal.update_client_group_by_id(
      client_group_id=model_data.pop('id'),
      kwargs=model_data
    )
    return updated_client_group


async def _delete_client_group_by_id(session: AsyncSession, client_group_id: int):
  async with session.begin():
    client_group_dal = ClientGroupDAL(session)
    client_group = await client_group_dal.get_only_client_group_by_id(client_group_id)
    if client_group is None:
      return not_Found_error
    deleted_client_group = await client_group_dal.delete_client_group_by_id(client_group_id)
    return deleted_client_group


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
