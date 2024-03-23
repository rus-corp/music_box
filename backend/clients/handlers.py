from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse



from backend.database import async_session_maker
from .schemas import ShowClient, CreateClient, CurrencyShow
from .dals import ClientDAL, CurrencyDAL
from backend.music.dals.track_group_dal import TrackCollectionDAL
from backend.music.schemas import TrackCollectionShow




# ======================== CLIENT =============================
async def _create_client(body: CreateClient, session: AsyncSession) -> ShowClient:
  async with session.begin():
    client_dal = ClientDAL(session)
    currency_dal = CurrencyDAL(session)
    model_data = body.model_dump()
    currency_id = model_data.pop('currency_id', 1)
    currency_data = await currency_dal.get_currency_by_id(currency_id)
    if currency_data is None:
      return JSONResponse(
        content=f'Currency not found'
      )
      
    model_data.update(currency=currency_data)
    client = await client_dal.create_client(**model_data)
    currency = CurrencyShow(
      id=client.currency.id,
      cur_name=client.currency.cur_name
    )
    return ShowClient(
      user_id=client.id,
      name=client.name,
      full_name=client.full_name,
      certificate=client.certificate,
      contract_number=client.contract_number,
      contract_date=client.contract_date,
      city=client.city,
      address= client.address,
      email=client.email,
      phone=client.phone,
      price=client.price,
      currency=currency
    )
      
      
async def _get_clients(session: AsyncSession):
  async with session.begin():
    client_dal = ClientDAL(session)
    clients = await client_dal.get_clients()
    return clients
  
  
  
async def _delete_client_in_trackcollection(session: AsyncSession, track_collection_id: int, client_id: int):
  async with session.begin():
    track_collection_dal = TrackCollectionDAL(session)
    deleted_client_in_track_collection = await track_collection_dal.delete_client_in_track_collection(
      track_collection_id=track_collection_id, client_id=client_id
    )
    return JSONResponse(content=f'Deleted {deleted_client_in_track_collection} rows', status_code=204)
  
  

async def _add_client_to_collection(session: AsyncSession, track_collection_id: int, client_id: int):
  async with session.begin():
    track_collection_dal = TrackCollectionDAL(session)
    track_collection = await track_collection_dal.get_track_collection_for_append_track_to_group(
      track_group_id=track_collection_id
    )
    if track_collection is None:
      return JSONResponse(content=f'Track Collection with id {track_collection_id} not found',
                          status_code=404)
    client_dal = ClientDAL(session)
    client = await client_dal.get_client_for_append(client_id=client_id)
    track_collection.clients.append(client)
    await session.commit()
    
    tracks_collection = TrackCollectionShow(
      id=track_collection.id,
      name=track_collection.name,
      player_option=track_collection.player_option
    )
    
    return ShowClient(
        user_id=client.client_id,
        name=client.name,
        full_name=client.full_name,
        certificate=client.cretificate,
        contract_number=client.contract_number,
        contract_date=client.contract_date,
        city=client.city,
        address= client.address,
        email=client.email,
        phone=client.phone,
        price=client.price,
        track_collections=tracks_collection
      )
    



    
# ======================== CURRENCY =============================
async def _create_currency(session: AsyncSession, currency_name: str):
  async with session.begin():
    currency_dal = CurrencyDAL(session)
    new_currency = await currency_dal.create_currency(name=currency_name)
    return CurrencyShow(
      cur_id=new_currency.id,
      cur_name=new_currency.cur_name
    )
    

async def _get_all_currencies(session: AsyncSession):
  async with session.begin():
    currency_dal = CurrencyDAL(session)
    currencies = await currency_dal.get_all_currency()
    return list(currencies)
  

async def _get_currency_by_id(session : AsyncSession, currency_id):
  async with session.begin():
    currency_dal = CurrencyDAL(session)
    currency = await currency_dal.get_currency_by_id(currency_id)
    if currency is None:
      return JSONResponse(
        content=f'Currency with id = {currency_id} not found',
        status_code=404
      )
    return currency
  

async def _update_currency(session: AsyncSession, currency_id: int, new_name: str):
  async with session.begin():
    currency_dal = CurrencyDAL(session)
    has_currency = await currency_dal.get_currency_by_id(currency_id)
    if has_currency is None:
      return JSONResponse(
        content=f'Currency with id = {currency_id} not found',
        status_code=404
      )
    updated_currency = currency_dal.update_currency(
      currency_id=currency_id, new_name=new_name
    )
    return updated_currency
  
  
async def _delete_currency(session: AsyncSession, currency_id: int):
  async with session.begin():
    currency_dal = CurrencyDAL(session)
    has_currency = await currency_dal.get_currency_by_id(currency_id)
    if has_currency is None:
      return JSONResponse(
        content=f'Currency with id = {currency_id} not found',
        status_code=404
      )
    deleted_currency = currency_dal.delete_currency_by_id(currency_id)
    return deleted_currency