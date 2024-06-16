from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status


from backend.auth.security import super_user_permission
from backend.auth.errors import access_denied_error
from backend.database import get_db
from ..schemas import ClientClusterShow, ClientClusterShow
from backend.general_schemas import ClientClusterShow_With_ClientGroups

from ..handlers.client_cluster_hand import (_create_client_cluster, _get_all_client_clusters_without_client_groups,
                                            _get_all_client_clusters_with_client_groups, _get_client_cluster_by_id_without_client_groups,
                                            _get_client_cluster_by_id_with_client_groups, _update_client_cluster, _delete_client_cluster_by_id)


router = APIRouter(
  prefix='/client_cluster',
  tags=['Client Clusetr']
)


@router.post('/', response_model=ClientClusterShow, status_code=status.HTTP_201_CREATED)
async def create_client_cluster(
  name: str,
  session: AsyncSession = Depends(get_db),
  permission: bool = Depends(super_user_permission)
):
  if permission:
    client_cluster = await _create_client_cluster(
      session, name
    )
    return client_cluster
  else:
    return access_denied_error


@router.get('/without_client_groups', response_model=ClientClusterShow, status_code=status.HTTP_200_OK)
async def get_all_client_clusters_without_client_groups(
  session: AsyncSession = Depends(get_db),
  permission: bool = Depends(super_user_permission)
):
  if permission:
    client_cluster = await _get_all_client_clusters_without_client_groups(session)
    return client_cluster
  else:
    return access_denied_error


@router.get('/with_client_groups', response_model=ClientClusterShow_With_ClientGroups, status_code=status.HTTP_200_OK)
async def get_all_client_clusters_with_client_groups(
  session: AsyncSession = Depends(get_db),
  permission: bool = Depends(super_user_permission)
):
  if permission:
    client_cluster = await _get_all_client_clusters_with_client_groups(session)
    return client_cluster
  else:
    return access_denied_error


@router.get('/cluster_with_client_group', response_model=ClientClusterShow_With_ClientGroups, status_code=status.HTTP_200_OK)
async def get_client_cluster_by_id_with_client_groups(
  session: AsyncSession = Depends(get_db),
  permission: bool = Depends(super_user_permission)
):
  if permission:
    client_cluster = await _get_client_cluster_by_id_with_client_groups(session)
    return client_cluster
  else:
    return
  access_denied_error


@router.get('/cluster_without_client_group', response_model=ClientClusterShow, status_code=status.HTTP_200_OK)
async def get_client_cluster_by_id_without_client_groups(
  session: AsyncSession = Depends(get_db),
  permission: bool = Depends(super_user_permission)
):
  if permission:
    client_cluster = await _get_client_cluster_by_id_without_client_groups(session)
    return client_cluster
  else:
    return access_denied_error


@router.patch('/{client_cluster_id}', response_model=ClientClusterShow, status_code=status.HTTP_200_OK)
async def update_client_cluster_by_id(
  cluster_id: int,
  name: str,
  session: AsyncSession = Depends(get_db),
  permission: bool = Depends(super_user_permission)
):
  if permission:
    updated_cluster = await _update_client_cluster(
      session=session, cluster_id=cluster_id, name=name
    )
    return updated_cluster
  else:
    return access_denied_error


@router.delete('/{client_cluster_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_client_cluster_by_id(
  client_cluster_id: int,
  session: AsyncSession = Depends(get_db),
  permission: bool = Depends(super_user_permission)
):
  if permission:
    deleted_cluster = await _delete_client_cluster_by_id(
      session=session, cluster_id=client_cluster_id
    )
    return deleted_cluster
  else:
    return access_denied_error














# ======================== ПРИМЕР РАЗГАРНИЧЕНИЯ ДОСТУПА =================
# @router.get('/')
# async def get_all_client_clusters_without_client_groups(
#     session: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user_from_token)
# ):
#     if current_user.is_superuser:
#         client_clusters = await _get_all_client_clusters(session)
#         return client_clusters
#     else:
#         # Фильтрация данных для обычного пользователя на основе его идентификации
#         client_clusters = await _get_filtered_client_clusters(session, current_user)
#         return client_clusters