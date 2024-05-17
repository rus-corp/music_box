from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status


from backend.database import get_db
from backend.auth.security import super_user_permission, get_current_user_from_token
from backend.auth.errors import access_denied_error
from backend.users.models import User

from ..schemas import ClientGroupCreate
from ..handlers.client_group_hand import ClientGroupHandler


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
    clientHandlers = ClientGroupHandler(session)
    created_group = await clientHandlers._create_client_group_take_client_cluster(body)
    return created_group
  else:
    return access_denied_error


@router.get('/client_group_with_clients', status_code=status.HTTP_200_OK)
async def get_all_client_groups_with_clients(
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  clientHandlers = ClientGroupHandler(session)
  client_groups = await clientHandlers._get_all_client_groups_with_clients(current_user)
  return client_groups


# @router.get('/client_group_without_clients')
# async def get_only_clients_group(
#   session: AsyncSession = Depends(get_db),
#   current_user: User = Depends(get_current_user_from_token)
# ): pass


