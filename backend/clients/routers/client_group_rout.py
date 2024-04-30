from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status


from backend.database import get_db
from backend.auth.security import super_user_permission, get_current_user_from_token
from backend.auth.errors import access_denied_error
from backend.users.models import User

from ..schemas import ClientGroupCreate
from ..handlers.client_group_hand import (_create_client_group_take_client_cluster, _get_all_client_groups_with_clients, _get_only_clients_group,
                                          _get_all_client_groups_with_users, _get_all_client_groups_with_clients_and_users, _get_only_client_group_by_id,
                                          _get_client_group_by_id_with_clients, _get_client_group_by_id_with_users, _get_client_group_by_id_with_users_and_clients, _update_client_group_by_id, _delete_client_group_by_id, _change_cluster_of_clients_group)
router = APIRouter(
  prefix='/client_groups',
  tags=['Client Groups']
)

@router.post('/')
async def create_client_group(
  body: ClientGroupCreate,
  session: AsyncSession = Depends(get_db),
  permission: bool = Depends(super_user_permission)
):
  if permission:
    created_group = await _create_client_group_take_client_cluster(
      session=session, body=body
    )
    return created_group
  else:
    return access_denied_error


@router.get('/client_group_with_clients', status_code=status.HTTP_200_OK)
async def get_all_client_groups_with_clients(
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  client_groups = await _get_all_client_groups_with_clients(
    session=session, user=current_user
  )
  return client_groups