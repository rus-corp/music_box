from sqlalchemy.ext.asyncio import AsyncSession



from ..dals.client_cluster_dals import ClientClusterDAL


async def _create_client_cluster(session: AsyncSession, name: str):
  async with session.begin():
    cluster_dal = ClientClusterDAL(session)
    created_cluster = await cluster_dal.create_client_cluster(name=name)
    return created_cluster


async def _get_all_client_clusters_without_client_groups(session: AsyncSession):
  async with session.begin():
    cluster_dal = ClientClusterDAL(session)
    client_clusters = await cluster_dal.get_all_client_clusters_without_client_groups()
    return list(client_clusters)


async def _get_all_client_clusters_with_client_groups(session: AsyncSession):
  async with session.begin():
    cluster_dal = ClientClusterDAL(session)
    client_cluster = await cluster_dal.get_all_client_clusters_with_client_groups()
    return list(client_cluster)


async def _get_client_cluster_by_id_without_client_groups(session: AsyncSession, cluster_id: int):
  async with session.begin():
    cluster_dal = ClientClusterDAL(session)
    client_cluster = await cluster_dal.get_client_cluster_by_id_without_client_groups(cluster_id)
    return client_cluster


async def _get_client_cluster_by_id_with_client_groups(session: AsyncSession, cluster_id: int):
  async with session.begin():
    cluster_dal = ClientClusterDAL(session)
    client_cluster = await cluster_dal.get_client_cluster_by_id_with_client_groups(cluster_id)
    return client_cluster


async def _update_client_cluster(session: AsyncSession, cluster_id: int, name: str):
  async with session.begin():
    cluster_dal = ClientClusterDAL(session)
    client_cluster = await cluster_dal.update_client_cluster_by_id(client_cluster_id=cluster_id, new_name=name)
    return client_cluster


async def _delete_client_cluster_by_id(session: AsyncSession, cluster_id: int):
  async with session.begin():
    cluster_dal = ClientClusterDAL(session)
    client_cluster = await cluster_dal.delete_client_cluster_by_id(cluster_id)
    return client_cluster