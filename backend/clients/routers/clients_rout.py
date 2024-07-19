from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession


from backend.auth.security import super_user_permission, get_current_user_from_token
from backend.auth.errors import access_denied_error
from backend.auth.permissions import Permissions
from backend.database import get_db
from backend.users.models import User
from ..schemas import (ClientProfileCreateResponse, CreateClient, UpdateClientRequest,
                       UpdateClientResponse, ShowClientWithTrackColections, ShowClientWithClientGroup)
from backend.general_schemas import ErrorMessageResponse

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
            response_model=List[ShowClientWithTrackColections])
async def get_all_clients_with_track_collection_and_currency(
  session: AsyncSession = Depends(get_db),
  current_user = Depends(get_current_user_from_token)
):
  client_handler_dal = ClientHandler(session, current_user=current_user)
  clients_list = await client_handler_dal._get_all_clients_with_track_collecions()
  return clients_list



@router.get('/clients_with_client_groups', status_code=status.HTTP_200_OK, response_model=List[ShowClientWithClientGroup])
async def get_clients_with_client_groups(
  session: AsyncSession = Depends(get_db),
  current_user = Depends(get_current_user_from_token)
):
  client_handler_dal = ClientHandler(session, current_user=current_user)
  clients_list = await client_handler_dal._get_all_clients_with_client_groups()
  return clients_list



@router.get('/clients_with_client_groups/{client_id}', status_code=status.HTTP_200_OK,
            response_model= ShowClientWithClientGroup,
            responses={
              400: {'model': ErrorMessageResponse}
            })
async def get_client_by_id_with_client_group(
  client_id: int,
  session: AsyncSession = Depends(get_db),
  current_user = Depends(get_current_user_from_token)
):
  client_handler_dal = ClientHandler(session, current_user=current_user)
  client_item = await client_handler_dal._get_client_by_id_with_client_group(
    client_id=client_id
  )
  return client_item


@router.get('/{client_id}', status_code=status.HTTP_200_OK,
            response_model=ShowClientWithTrackColections, responses={
              404: {'model': ErrorMessageResponse}
            })
async def get_client_by_id_with_track_collection_and_currency(
  client_id: int,
  session: AsyncSession = Depends(get_db),
  current_user = Depends(get_current_user_from_token)
):
  client_handler_dal = ClientHandler(session, current_user=current_user)
  client_item = await client_handler_dal._get_client_by_id_with_track_collecions(
    client_id=client_id
  )
  return client_item


@router.patch('/{client_id}', status_code=status.HTTP_200_OK,
              response_model=ShowClientWithTrackColections, responses={
                404: {'model': ErrorMessageResponse}
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


@router.delete('/{client_id}', status_code=200, response_model=ErrorMessageResponse)
async def delete_client_group_by_id(
  client_id: int,
  session: AsyncSession = Depends(get_db),
  permission: bool = Depends(super_user_permission)
):
  if permission:
      client_handler_dal = ClientHandler(session)
      deleted_client_group = await client_handler_dal._delete_client_group_by_id(
        client_id=client_id
      )
      return deleted_client_group
  else:
    return access_denied_error



@router.post('/append_track_collection_to_client', status_code=status.HTTP_201_CREATED)
async def append_track_collection_to_client(
  session: AsyncSession = Depends(get_db),
  current_user = Depends(get_db),
):
  client_handler_dal = ClientHandler(session, current_user)



@router.delete('/delete_track_collection_from_client')
async def delete_track_collection_from_client(
  session: AsyncSession = Depends(get_db),
  current_user = Depends(get_db),
):
  client_handler_dal = ClientHandler(session, current_user)


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