from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.auth.security import super_user_permission
from backend.users.models import User
from backend.auth.errors import access_denied_error
from ..schemas import CurrencyShow

from ..handlers.currency_hand import (_create_currency, _get_all_currencies, _get_currency_by_id,
                                      _update_currency, _delete_currency)

router = APIRouter(
  prefix='/currency',
  tags=['Currency']
)


@router.post('/', response_model=CurrencyShow, status_code=status.HTTP_201_CREATED)
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



@router.get('/', response_model=List[CurrencyShow])
async def get_all_currencies(
  session: AsyncSession = Depends(get_db),
  permissions: User = Depends(super_user_permission)
):
  if permissions:
    currencies = await _get_all_currencies(session)
    return currencies
  else:
    return access_denied_error



@router.get('/{currency_id}', response_model=CurrencyShow)
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



@router.patch('/{currency_id}', response_model=CurrencyShow)
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



@router.delete('/{currency_id}', status_code=status.HTTP_204_NO_CONTENT)
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