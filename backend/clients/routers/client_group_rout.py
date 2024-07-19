from typing import List, Union
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status


from backend.database import get_db
from backend.auth.security import super_user_permission, get_current_user_from_token
from backend.auth.errors import access_denied_error
from backend.users.models import User

from ..schemas import (ClientGroupCreateRequest, ClientGroupCreateResponse,
                       ClientGroupShowDefault, ClientGroupWithClientShow, ClientGroupUpdateRequset, ClientGroupUpdateResponse,
                       ClientGroupDeleteResponse, AppendUserToGroupRequest)

from backend.general_schemas import (ClientGroupAppendUserResponse, ErrorMessageResponse)

from ..handlers.client_group_hand import ClientGroupHandler


router = APIRouter(
  prefix='/client_groups',
  tags=['Client Groups']
)



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ClientGroupCreateResponse)
async def create_client_group(
  body: ClientGroupCreateRequest,
  session: AsyncSession = Depends(get_db),
  permission: bool = Depends(super_user_permission)
):
  if permission:
    clientHandlers = ClientGroupHandler(session)
    created_group = await clientHandlers._create_client_group_take_client_cluster(body)
    return created_group
  else:
    return access_denied_error



@router.get('/', response_model=List[ClientGroupShowDefault], status_code=status.HTTP_200_OK)
async def get_only_client_groups(
  session: AsyncSession = Depends(get_db),
  current_user = Depends(get_current_user_from_token)
):
  client_group_handler = ClientGroupHandler(session, current_user)
  client_groups = await client_group_handler._get_only_clients_group()
  return client_groups



@router.get('/{client_group_id}', status_code=status.HTTP_200_OK, response_model=ClientGroupShowDefault)
async def get_client_group_by_id(
  client_group_id: int,
  session: AsyncSession = Depends(get_db),
  current_user = Depends(get_current_user_from_token)
):
  client_group_handler = ClientGroupHandler(session, current_user)
  client_group = await client_group_handler._get_only_client_group_by_id(
    client_group_id
  )
  return client_group




@router.get('/with_clients/', status_code=status.HTTP_200_OK, response_model=List[ClientGroupWithClientShow])
async def get_all_client_groups_with_clients(
  session: AsyncSession = Depends(get_db),
  current_user = Depends(get_current_user_from_token)
):
  client_group_handler = ClientGroupHandler(session, current_user)
  client_groups = await client_group_handler._get_all_client_groups_with_clients()
  return client_groups



@router.get('/with_clients/{client_group_id}', status_code=status.HTTP_200_OK, response_model=ClientGroupWithClientShow)
async def get_client_group_by_id_with_clients(
  client_group_id: int,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  client_group_handler = ClientGroupHandler(session, current_user)
  client_group = await client_group_handler._get_client_group_by_id_with_clients(
    client_group_id=client_group_id
  )
  return client_group



@router.patch('/{client_group_id}', status_code=status.HTTP_200_OK, response_model=ClientGroupUpdateResponse)
async def change_client_group_data(
  client_group_id: int,
  body: ClientGroupUpdateRequset,
  session: AsyncSession = Depends(get_db),
  permission: bool = Depends(super_user_permission)
):
  if permission:
    clientHandlers = ClientGroupHandler(session)
    updated_group = await clientHandlers._update_client_group(
      client_group_id=client_group_id, body=body
    )
    return updated_group
  else:
    return access_denied_error



@router.delete('/{client_group_id}', status_code=status.HTTP_200_OK,
               response_model=Union[ClientGroupDeleteResponse,ErrorMessageResponse])
async def delete_client_group_by_id(
  client_group_id: int,
  session: AsyncSession = Depends(get_db),
  permission: bool = Depends(super_user_permission)
):
  if permission:
    clientHandlers = ClientGroupHandler(session)
    deleted_group = await clientHandlers._delete_client_group_by_id(
      client_group_id=client_group_id
    )
    return deleted_group
  else:
    return access_denied_error



@router.post('/append_user_to_client_group', status_code=status.HTTP_201_CREATED,
             response_model=ClientGroupAppendUserResponse,
             responses= {
               400: {'model': ErrorMessageResponse}
             })
async def append_user_to_client_group(
  body: AppendUserToGroupRequest,
  session: AsyncSession = Depends(get_db),
  permission: bool = Depends(super_user_permission)
):
  if permission:
    clientHandlers = ClientGroupHandler(session)
    appended_user = await clientHandlers._append_user_to_client_group(
      body=body
    )
    return appended_user
  else:
    return access_denied_error



@router.delete('/delete_user_from_client_group/',
               status_code=status.HTTP_200_OK, response_model=ErrorMessageResponse)
async def delete_user_from_client_group(
  body: AppendUserToGroupRequest,
  session: AsyncSession = Depends(get_db),
  permission: bool = Depends(super_user_permission)
):
  if permission:
    clientHandlers = ClientGroupHandler(session)
    deleted_user = await clientHandlers._delete_user_from_client_group(
      body=body
    )
    return deleted_user
  else:
    return access_denied_error


# @router.get('/client_group_with_users/{client_group_id}', status_code=status.HTTP_200_OK)
# async def get_client_group_with_users(
#   client_group_id: int,
#   session: AsyncSession = Depends(get_db),
#   permission: bool = Depends(super_user_permission)
# ):
#   if permission:
#     clientHandlers = ClientGroupHandler(session)
#     client_groups = await clientHandlers.
#     return client_groups
#   else:
#     return access_denied_error




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










