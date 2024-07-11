from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession


from backend.auth.security import super_user_permission, get_current_user_from_token
from backend.auth.errors import access_denied_error
from backend.auth.permissions import Permissions
from backend.database import get_db
from backend.users.models import User
from ..schemas import (CleintGroupDeleteMessage, ClientProfileCreateResponse, CreateClient, UpdateClientRequest,
                       UpdateClientResponse, ShowClient)


from ..handlers.clients_hand import ClientHandler



router = APIRouter(
  prefix='/clients',
  tags=['Clients']
)





@router.post('/', response_model=ClientProfileCreateResponse,
             status_code=status.HTTP_201_CREATED)
async def create_client(
  body: CreateClient,
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    client_handler_dal = ClientHandler(session)
    client = await client_handler_dal._create_client(body)
    return client
  else:
    return access_denied_error



@router.get('/', status_code=status.HTTP_200_OK,
            response_model=List[ShowClient])
async def get_all_clients(
  session: AsyncSession = Depends(get_db),
  current_user = Depends(get_current_user_from_token)
):
  client_handler_dal = ClientHandler(session, current_user=current_user)
  clients_list = await client_handler_dal._get_all_clients()
  return clients_list



@router.get('/{client_id}', status_code=status.HTTP_200_OK,
            response_model=ShowClient, responses={
              400: {'model': CleintGroupDeleteMessage}
            })
async def get_all_clients(
  client_id: int,
  session: AsyncSession = Depends(get_db),
  current_user = Depends(get_current_user_from_token)
):
  client_handler_dal = ClientHandler(session, current_user=current_user)
  client_item = await client_handler_dal._get_client_by_id(
    client_id=client_id
  )
  return client_item


@router.patch('/{client_id}', status_code=status.HTTP_200_OK,
              response_model=ShowClient, responses={
                404: {'model': CleintGroupDeleteMessage}
              })
async def update_client_by_id(
  client_id: int,
  body: UpdateClientRequest,
  session: AsyncSession = Depends(get_db),
  permission: bool = Depends(super_user_permission)
):
  if permission:
    client_handler_dal = ClientHandler(session)
    updated_client = await client_handler_dal._update_client_by_id(
      client_id=client_id, body=body
    )
    return updated_client
  else:
    return access_denied_error
  




# @router.get('/', response_model=List[ShowClient])
# async def get_all_clients(
#   session: AsyncSession = Depends(get_db),
#   permissions: bool = Depends(super_user_permission)
# ):
#   if permissions:
#     result = await _get_all_clients(session)
#     return result
#   else:
#     return access_denied_error



# @router.get('/{client_id}', response_model=ShowClient)
# async def get_client_by_id(
#   client_id: int,
#   session: AsyncSession = Depends(get_db),
#   current_user: User = Depends(get_current_user_from_token)
# ):
#   permission = Permissions(current_user=current_user)
#   permission_role = await permission.superuser_permission()
#   if permission_role:
#     client = await _get_client_by_id(
#       session=session, client_id=client_id
#     )
#     return client
#   else:
#     return access_denied_error



# @router.patch('/{client_id}', response_model=UpdateClientResponse)
# async def update_client_by_id(
#   body: UpdateClientRequest,
#   session: AsyncSession = Depends(get_db),
#   permissions: User = Depends(super_user_permission)
# ):
#   if permissions:
#     updated_client = await _update_client_by_id(session=session, body=body)
#     return updated_client
#   else:
#     return access_denied_error



# @router.delete('/{client_id}', status_code=status.HTTP_204_NO_CONTENT)
# async def delete_client_by_id(
#   client_id: int,
#   session: AsyncSession = Depends(get_db),
#   permissions: User = Depends(super_user_permission)
# ):
#   if permissions:
#     deleted_client = await _delete_client_by_id(session=session, client_id=client_id)
#     return deleted_client
#   else:
#     return access_denied_error




# @router.post('')
# async def add_currency_to_user(): pass




# @router.post('/add_client_to_track_collection/{track_collection_id}', response_model=ShowClient)
# async def add_client_to_track_collection(
#   track_collection_id: int,
#   client_id: int,
#   session: AsyncSession = Depends(get_db)
# ):
#   aded_client_to_track_collection = await _add_client_to_collection(
#     session=session, track_collection_id=track_collection_id, client_id=client_id
#   )
#   return aded_client_to_track_collection


# @router.delete('/delete_client_in_track_collections/{track_collection_id}', )
# async def delete_client_in_track_collection(track_collection_id: int,
#                                             client_id: int,
#                                             session: AsyncSession = Depends(get_db)):
#   deleted_client_in_track_collection = await _delete_client_in_trackcollection(
#     session, track_collection_id, client_id
#   )
#   return deleted_client_in_track_collection