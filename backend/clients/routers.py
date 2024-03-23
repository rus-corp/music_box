from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from backend.database import get_db

from .handlers import (_get_clients, _create_client, _add_client_to_collection,
                       _delete_client_in_trackcollection, _create_currency, _get_all_currencies,
                       _get_currency_by_id, _update_currency, _delete_currency)
from .schemas import ShowClient, CreateClient, CurrencyShow, CurrencyDeleteResponse



router = APIRouter(
  prefix='/clients',
  tags=['Clients']
)



@router.get('/')
async def get_clients(session: AsyncSession = Depends(get_db)):
  res = await _get_clients(session)
  return res



@router.post('/', response_model=ShowClient)
async def create_client(body: CreateClient, session: AsyncSession = Depends(get_db)) -> ShowClient:
  res = await _create_client(
    session=session, body=body
  )
  return res



@router.post('/add_client_to_track_collection/{track_collection_id}', response_model=ShowClient)
async def add_client_to_track_collection(track_collection_id: int, client_id: int, session: AsyncSession = Depends(get_db)):
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
@router.post('/currency', response_model=CurrencyShow)
async def create_currency(currency_name: str, session: AsyncSession = Depends(get_db)):
  new_currency = await _create_currency(
    session=session, currency_name=currency_name
  )
  return new_currency


@router.get('/currency', response_model=List[CurrencyShow])
async def get_all_currencies(session: AsyncSession = Depends(get_db)):
  currencies = await _get_all_currencies(session)
  return currencies
  
  
@router.get('/currency/{currency_id}', response_model=CurrencyShow)
async def get_currency_by_id(currency_id: int, session: AsyncSession = Depends(get_db)):
  currency = await _get_currency_by_id(
    session=session, currency_id=currency_id
  )
  return currency


@router.patch('/currency/{currency_id}', response_model=CurrencyShow)
async def update_currency(currency_id: int, new_name: str, session: AsyncSession = Depends(get_db)):
  updated_currency = await _update_currency(
    session=session, currency_id=currency_id, new_name=new_name
  )
  return updated_currency


@router.delete('/currency/{currency_id}', response_model=CurrencyDeleteResponse)
async def delete_currency(currency_id: int, session: AsyncSession = Depends(get_db)):
  deleted_currency = await _delete_currency(
    session=session, currency_id=currency_id
  )
  return deleted_currency