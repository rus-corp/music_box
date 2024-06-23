from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status


from backend.database import get_db
from backend.auth.security import super_user_permission, get_current_user_from_token
from backend.auth.errors import access_denied_error
from backend.users.models import User

from ..schemas import ClientGroupCreate, ClientGroupShow
from ..handlers.client_group_hand import ClientGroupHandler
from ..handlers.client_group_hand import _append_user_to_client_group

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


@router.get('/', response_model=List[ClientGroupShow])
async def get_only_client_groups(
  session: AsyncSession = Depends(get_db),
  current_user = Depends(get_current_user_from_token)
):
  client_group_handler = ClientGroupHandler(session, current_user)
  client_groups = await client_group_handler._get_only_clients_group()
  return client_groups



@router.get('/with_clients')
async def get_client_groups_with_clients(
  session: AsyncSession = Depends(get_db),
  current_user = Depends(get_current_user_from_token)
):
  client_group_handler = ClientGroupHandler(session, current_user)
  client_groups = await client_group_handler._get_client_groups_with_clients()
  return client_groups


# /clients/client_groups/append_user_to_client_group
# @router.post('/append')
# async def add_user_to_client_group():pass
# @router.post('/user_clients/{user_id}')
# async def add_user_to_client_group(
#   user_id: int,
#   body: CreateClient,
#   session: AsyncSession = Depends(get_db),
#   permissions: bool = Depends(super_user_permission)
# ):
#   if permissions:
#     user_handler = UserHandler(session)
#     add_clients = await _add_user_clients(
#       user_id=user_id, body=body
#     )
#     return add_clients
#   else:
#     return access_denied_error

# @router.post('/append_user_to_client_group')
# async def append_user_to_client_group(
#   client_group_id: int,
#   user_id: int,
#   session: AsyncSession = Depends(get_db)
# ):
#   append_client = await _append_user_to_client_group(
#     session, client_group_id, user_id
#   )
#   return append_client





async def remove_user_from_client_group():pass


async def change_users_client_group():pass




# @router.get('/client_group_with_clients', status_code=status.HTTP_200_OK)
# async def get_all_client_groups_with_clients(
#   session: AsyncSession = Depends(get_db),
#   current_user: User = Depends(get_current_user_from_token)
# ):
#   clientHandlers = ClientGroupHandler(session)
#   client_groups = await clientHandlers._get_all_client_groups_with_clients(current_user)
#   return client_groups


# @router.get('/client_group_without_clients')
# async def get_only_clients_group(
#   session: AsyncSession = Depends(get_db),
#   current_user: User = Depends(get_current_user_from_token)
# ): pass










