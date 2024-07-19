from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status
from typing import List

from backend.auth.security import super_user_permission, get_current_user_from_token
from backend.auth.errors import access_denied_error, not_Found_error
from backend.database import get_db
from ..schemas import (ClientClusterShow, ClientClusterShow, ClientClusterDeleteResponse,
                       ClientClusterShow_With_ClientGroups, ClientClusterShow_With_Listr_ClientGroups)
from backend.general_schemas import ErrorMessageResponse
from backend.users.models import User

from ..handlers.client_cluster_hand import ClientClusterHandler





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
    cluster_handler = ClientClusterHandler(session)
    client_cluster = await cluster_handler._create_client_cluster(name)
    return client_cluster
  else:
    return access_denied_error



@router.get('/without_client_groups', response_model=List[ClientClusterShow], status_code=status.HTTP_200_OK)
async def get_all_client_clusters_without_client_groups(
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  cluster_handler = ClientClusterHandler(session, current_user)
  client_clusters = await cluster_handler._get_all_client_clusters_without_client_groups()
  return client_clusters



@router.get('/cluster_without_client_group/{cluster_id}', response_model=ClientClusterShow, status_code=status.HTTP_200_OK)
async def get_client_cluster_by_id_without_client_groups(
  cluster_id: int,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  cluster_handler = ClientClusterHandler(session, current_user)
  client_cluster = await cluster_handler._get_client_cluster_by_id_without_client_groups(cluster_id)
  return client_cluster



@router.patch('/{client_cluster_id}', response_model=ClientClusterShow, status_code=status.HTTP_200_OK, 
              responses={
                404: {'model':ErrorMessageResponse}
              })
async def update_client_cluster_by_id(
  cluster_id: int,
  name: str,
  session: AsyncSession = Depends(get_db),
  permission: bool = Depends(super_user_permission)
):
  if permission:
    cluster_handler = ClientClusterHandler(session)
    updated_cluster = await cluster_handler._update_client_cluster(
      cluster_id=cluster_id, name=name
    )
    if updated_cluster is None:
      return not_Found_error
    return updated_cluster
  else:
    return access_denied_error


@router.delete('/{cluster_id}', status_code=status.HTTP_200_OK, response_model=ClientClusterDeleteResponse,
               responses={
                 400: {'model': ErrorMessageResponse},
                 404: {'model':ErrorMessageResponse}
               })
async def delete_client_cluster_by_id(
  cluster_id: int,
  session: AsyncSession = Depends(get_db),
  permission: bool = Depends(super_user_permission)
):
  if permission:
    cluster_handler = ClientClusterHandler(session)
    deleted_cluster = await cluster_handler._delete_client_cluster(cluster_id)
    return deleted_cluster
  else:
    return access_denied_error



# @router.get('/with_client_groups', response_model=ClientClusterShow_With_ClientGroups, status_code=status.HTTP_200_OK)
# async def get_all_client_clusters_with_client_groups(
#   session: AsyncSession = Depends(get_db),
#   current_user: User = Depends(get_current_user_from_token)
# ):
#   cluster_handler = ClientClusterHandler(session, current_user)
#   client_cluster = await cluster_handler._get_all_client_clusters_with_client_groups()
#   return client_cluster


# @router.get('/cluster_with_client_group/{cluster_id}', response_model=ClientClusterShow_With_Listr_ClientGroups, status_code=status.HTTP_200_OK)
# async def get_client_cluster_by_id_with_client_groups(
#   cluster_id: int,
#   session: AsyncSession = Depends(get_db),
#   current_user: User = Depends(get_current_user_from_token)
# ):
#   cluster_handler = ClientClusterHandler(session, current_user)
#   client_cluster = await cluster_handler._get_client_cluster_by_id_with_client_groups(cluster_id)
#   return client_cluster











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