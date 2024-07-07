from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import selectinload, joinedload, aliased
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from ..models import ClientCluster, ClientGroup, user_client_group_association
from backend.users.models import User


class ClientClusterDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session


  async def create_client_cluster(self, name: str):
    new_cluster = ClientCluster(name=name)
    self.db_session.add(new_cluster)
    await self.db_session.commit()
    return new_cluster


  async def get_all_client_clusters_without_client_groups_superuser(self):
    query = select(ClientCluster).order_by(ClientCluster.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()
  
  
  async def get_all_client_clusters_without_client_groups_manager(self, user_id: int):
    query = select(ClientCluster).join(ClientCluster.client_groups).join(user_client_group_association).join(User).filter(User.id == user_id)
    result = await self.db_session.execute(query)
    return result.scalars().all()


  async def get_all_client_clusters_with_client_groups_superuser(self):
    query = select(ClientCluster).options(selectinload(ClientCluster.client_groups)).order_by(ClientCluster.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()
  
  
  async def get_all_client_clusters_with_client_groups_manager(self, user_id: int):
    cg = aliased(ClientGroup)
    cc = aliased(ClientCluster)
    ucga = aliased(user_client_group_association)
    u = aliased(User)
    query = (select(cc, cg).select_from(cc).join(cg, cg.client_cluster_id == cc.id).join(ucga, ucga.c.client_group_id == cg.id).join(u, u.id == ucga.c.user_id).filter(u.id == user_id))
    result = await self.db_session.execute(query)
    res = result.all()
    return res
  
  
  
  async def get_client_cluster_by_id_without_client_groups_superuser(self, client_cluster_id: int):
    query = select(ClientCluster).where(ClientCluster.id == client_cluster_id)
    result = await self.db_session.execute(query)
    client_cluster = result.fetchone()
    if client_cluster is not None:
      return client_cluster[0]
  
  
  async def get_client_cluster_by_id_without_client_groups_manager(self, cluster_id: int, user_id: int):
    query = select(ClientCluster).join(ClientGroup).join(user_client_group_association).join(User).filter(and_(User.id == user_id, ClientCluster.id == cluster_id))
    result = await self.db_session.execute(query)
    cluster_row = result.fetchone()
    if cluster_row is not None:
      return cluster_row[0]
  
  
  async def get_client_cluster_by_id_with_client_groups(self, client_cluster_id: int):
    query = select(ClientCluster).where(ClientCluster.id == client_cluster_id).options(selectinload(ClientCluster.client_groups))
    reuslt = await self.db_session.execute(query)
    client_cluster = reuslt.fetchone()
    if client_cluster is not None:
      return client_cluster[0]


  async def update_client_cluster_by_id(self, client_cluster_id: int, new_name: str):
    stmt = update(ClientCluster).where(ClientCluster.id == client_cluster_id).values(name=new_name).returning(ClientCluster)
    result = await self.db_session.execute(stmt)
    await self.db_session.commit()
    updated_client_cluster = result.fetchone()
    if updated_client_cluster is not None:
      return updated_client_cluster[0]


  async def delete_client_cluster_by_id(self, client_cluster_id: int):
    try:
      stmt = delete(ClientCluster).where(ClientCluster.id == client_cluster_id).returning(ClientCluster.id)
      result = await self.db_session.execute(stmt)
      await self.db_session.commit()
      return result.scalar()
    except IntegrityError as e:
      error_message = 'Невозможно удалить ClientCluster из-за наличия зависимых записей в ClientGroup.'
      return error_message



  async def get_client_cluster_for_client_group(self, client_cluster_id):
    query = select(ClientCluster).where(ClientCluster.id == client_cluster_id)
    result = await self.db_session.scalar(query)
    return result