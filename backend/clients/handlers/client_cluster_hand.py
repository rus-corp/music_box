from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse


from backend.auth.errors import not_Found_error

from ..dals.client_cluster_dals import ClientClusterDAL
from ..schemas import (ClientClusterDeleteResponse, ClientClusterShow_With_ClientGroups,
                       ClientClusterShow)

from backend.users.models import User
from backend.auth.errors import access_denied_error




class ClientClusterHandler:
  def __init__(self, session: AsyncSession, current_user: User = None):
    self.session = session
    self.cluster_dal = ClientClusterDAL(self.session)
    self.current_user = current_user
    self.roles = ['manager', 'client']
  
  
  async def _create_client_cluster(self, name: str):
    async with self.session.begin():
      created_cluster = await self.cluster_dal.create_client_cluster(name)
      return created_cluster
  
  
  async def _get_all_client_clusters_without_client_groups(self):
    if self.current_user.is_superuser:
      client_clusters = await self.cluster_dal.get_all_client_clusters_without_client_groups_superuser()
      return list(client_clusters)
    elif self.current_user.role.role_name in self.roles:
      client_clusters = await self.cluster_dal.get_all_client_clusters_without_client_groups_manager(user_id=self.current_user.id)
      return list(client_clusters)
    else:
      return access_denied_error
  
  
  
  async def _get_client_cluster_by_id_without_client_groups(self, cluster_id: int):
    if self.current_user.is_superuser:
      client_cluster = await self.cluster_dal.get_client_cluster_by_id_without_client_groups_superuser(cluster_id)
    elif self.current_user.role.role_name in self.roles:
      client_cluster = await self.cluster_dal.get_client_cluster_by_id_without_client_groups_manager(
        cluster_id=cluster_id, user_id=self.current_user.id
      )
    else:
      return access_denied_error
    if client_cluster is None:
      return not_Found_error
    return client_cluster
  
  
  
  async def _update_client_cluster(self, cluster_id: int, name: str):
    async with self.session.begin():
      updated_cluster = await self.cluster_dal.update_client_cluster_by_id(
        client_cluster_id=cluster_id, new_name=name
      )
      return updated_cluster
  
  
  async def _delete_client_cluster(self, cluster_id: int):
    async with self.session.begin():
      deleted_cluster = await self.cluster_dal.delete_client_cluster_by_id(cluster_id)
      if isinstance(deleted_cluster, str):
        return JSONResponse(content=deleted_cluster, status_code=400)
      if deleted_cluster is None:
        return not_Found_error
      return ClientClusterDeleteResponse(id=deleted_cluster)
  
  
  
  # async def _get_all_client_clusters_with_client_groups(self):
  #   if self.current_user.is_superuser:
  #     client_clusters = await self.cluster_dal.get_all_client_clusters_with_client_groups_superuser()
  #     return list(client_clusters)
  #   elif self.current_user.role.role_name in self.roles:
  #     client_clusters = await self.cluster_dal.get_all_client_clusters_with_client_groups_manager(
  #       user_id=self.current_user.id
  #     )
  #     clusters= []
  #     for cluster_data, group_data in client_clusters:
  #       clusters.append(
  #         ClientClusterShow_With_ClientGroups(
  #           id = cluster_data.id,
  #           name=cluster_data.name,
  #           client_groups=[group_data]
  #         )
  #       )
  #     return clusters
  #   else:
  #     return access_denied_error
  
  
  # async def _get_client_cluster_by_id_with_client_groups(self, cluster_id: int):
  #   if self.current_user.is_superuser:
  #     client_cluster = await self.cluster_dal.get_client_cluster_by_id_with_client_groups_superuser(cluster_id)
  #     return client_cluster
  #   # elif self.current_user.role.role_name in self.roles:
  #   #   client_cluster = await self.cluster_dal.get_client_cluster_by_id_with_client_groups_manager(
  #   #     user_id=self.current_user.id, cluster_id=cluster_id
  #   #   )
  #   else:
  #     return access_denied_error