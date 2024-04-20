from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession


from backend.database import get_db
from backend.auth.security import get_current_user_from_token, super_user_permission
from backend.users.models import User
from backend.auth.permissions import Permissions
from backend.auth.errors import access_denied_error

from .handlers import (_get_all_clients, _get_client_by_id, _create_client, _update_client_by_id, _delete_client_by_id, _add_client_to_collection,
                       _delete_client_in_trackcollection, _create_currency, _get_all_currencies,
                       _get_currency_by_id, _update_currency, _delete_currency)
from .schemas import (ShowClient, CreateClient, CurrencyShow,
                      UpdateClientRequest, UpdateClientResponse)



router = APIRouter(
  prefix='/clients',
  tags=['Clients']
)




@router.post('/', response_model=ShowClient, status_code=status.HTTP_201_CREATED)
async def create_client(
  body: CreateClient,
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
) -> ShowClient:
  if permissions:
    client = await _create_client(
      session=session, body=body
    )
    return client
  else:
    return access_denied_error



@router.get('/', response_model=List[ShowClient])
async def get_all_clients(
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    result = await _get_all_clients(session)
    return result
  else:
    return access_denied_error



@router.get('/{client_id}', response_model=ShowClient)
async def get_client_by_id(
  client_id: int,
  session: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user_from_token)
):
  permission = Permissions(current_user=current_user)
  permission_role = await permission.superuser_permission()
  if permission_role:
    client = await _get_client_by_id(
      session=session, client_id=client_id
    )
    return client
  else:
    return access_denied_error



@router.patch('/{client_id}', response_model=UpdateClientResponse)
async def update_client_by_id(
  body: UpdateClientRequest,
  session: AsyncSession = Depends(get_db),
  permissions: User = Depends(super_user_permission)
):
  if permissions:
    updated_client = await _update_client_by_id(session=session, body=body)
    return updated_client
  else:
    return access_denied_error



@router.delete('/{client_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_client_by_id(
  client_id: int,
  session: AsyncSession = Depends(get_db),
  permissions: User = Depends(super_user_permission)
):
  if permissions:
    deleted_client = await _delete_client_by_id(session=session, client_id=client_id)
    return deleted_client
  else:
    return access_denied_error




@router.post('')
async def add_currency_to_user(): pass




@router.post('/add_client_to_track_collection/{track_collection_id}', response_model=ShowClient)
async def add_client_to_track_collection(
  track_collection_id: int,
  client_id: int,
  session: AsyncSession = Depends(get_db)
):
  aded_client_to_track_collection = await _add_client_to_collection(
    session=session, track_collection_id=track_collection_id, client_id=client_id
  )
  return aded_client_to_track_collection


@router.delete('/delete_client_in_track_collections/{track_collection_id}', )
async def delete_client_in_track_collection(track_collection_id: int,
                                            client_id: int,
                                            session: AsyncSession = Depends(get_db)):
  deleted_client_in_track_collection = await _delete_client_in_trackcollection(
    session, track_collection_id, client_id
  )
  return deleted_client_in_track_collection



# ======================== CURRENCY =============================
@router.post('/currency', response_model=CurrencyShow, status_code=status.HTTP_201_CREATED)
async def create_currency(
  currency_name: str,
  session: AsyncSession = Depends(get_db),
  permissions: User = Depends(super_user_permission)
):
  if permissions:
    new_currency = await _create_currency(
      session=session, currency_name=currency_name
    )
    return new_currency
  else:
    return access_denied_error



@router.get('/currency', response_model=List[CurrencyShow])
async def get_all_currencies(
  session: AsyncSession = Depends(get_db),
  permissions: User = Depends(super_user_permission)
):
  if permissions:
    currencies = await _get_all_currencies(session)
    return currencies
  else:
    return access_denied_error



@router.get('/currency/{currency_id}', response_model=CurrencyShow)
async def get_currency_by_id(
  currency_id: int,
  session: AsyncSession = Depends(get_db),
  permissions: User = Depends(super_user_permission)
):
  if permissions:
    currency = await _get_currency_by_id(
      session=session, currency_id=currency_id
    )
    return currency
  else:
    return access_denied_error



@router.patch('/currency/{currency_id}', response_model=CurrencyShow)
async def update_currency(
  currency_id: int,
  new_name: str,
  session: AsyncSession = Depends(get_db),
  permissions: User = Depends(super_user_permission)
):
  if permissions:
    updated_currency = await _update_currency(
      session=session, currency_id=currency_id, new_name=new_name
    )
    return updated_currency
  else:
    return access_denied_error



@router.delete('/currency/{currency_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_currency(
  currency_id: int,
  session: AsyncSession = Depends(get_db),
  permissions: User = Depends(super_user_permission)
):
  if permissions:
    deleted_currency = await _delete_currency(
      session=session, currency_id=currency_id
    )
    return deleted_currency
  else:
    return access_denied_error