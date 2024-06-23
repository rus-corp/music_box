from sqlalchemy.ext.asyncio import AsyncSession



from backend.auth.errors import not_Found_error

from ..dals.client_cluster_dals import ClientClusterDAL



class ClientClusterHandler:
  def __init__(self, session: AsyncSession):
    self.session = session
    self.cluster_dal = ClientClusterDAL(self.session)
  
  
  async def _create_client_cluster(self, name: str):
    async with self.session.begin():
      created_cluster = await self.cluster_dal.create_client_cluster(name)
      return created_cluster
  
  
  async def _get_all_client_clusters_without_client_groups(self):
    async with self.session.begin():
      client_clusters = await self.cluster_dal.get_all_client_clusters_without_client_groups()
      return list(client_clusters)
  
  
  async def _get_all_client_clusters_with_client_groups(self):
    async with self.session.begin():
      client_clusters = await self.cluster_dal.get_all_client_clusters_with_client_groups()
      return list(client_clusters)
  
  
  async def _get_client_cluster_by_id_without_client_groups(self, cluster_id: int):
    async with self.session.begin():
      client_cluster = await self.cluster_dal.get_client_cluster_by_id_without_client_groups(cluster_id)
      return client_cluster
  
  
  async def _get_client_cluster_by_id_with_client_groups(self, cluster_id: int):
    async with self.session.begin():
      client_cluster = await self.cluster_dal.get_client_cluster_by_id_with_client_groups(cluster_id)
      return client_cluster
  
  
  async def _update_client_cluster(self, cluster_id: int, name: str):
    async with self.session.begin():
      client_cluster = await self._get_client_cluster_by_id_without_client_groups(cluster_id)
      if client_cluster is None:
        return not_Found_error
      updated_cluster = await self.cluster_dal.update_client_cluster_by_id(
        client_cluster_id=cluster_id, new_name=name
      )
      return updated_cluster
  
  
  async def _delete_client_cluster(self, cluster_id: int):
    async with self.session.begin():
      client_cluster = await self._get_client_cluster_by_id_without_client_groups(cluster_id)
      if client_cluster is None:
        return not_Found_error
      deleted_cluster = await self.cluster_dal.delete_client_cluster_by_id(cluster_id)
      return deleted_cluster
