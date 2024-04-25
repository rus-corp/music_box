from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse


from backend.auth import errors
from ..schemas import CreateClient, ShowClient, CurrencyShow, UpdateClientRequest, UpdateClientResponse
from ..dals.clients_dals import ClientDAL
from ..dals.currency_dals import CurrencyDAL
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
      return errors.not_Found_error
    
    model_data.update(currency=currency_data)
    client = await client_dal.create_client(**model_data)
    currency = CurrencyShow(
      id=client.currency.id,
      cur_name=client.currency.cur_name
    )
    return ShowClient(
      client_id=client.id,
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
      currency=currency,
      user=client.user_id
    )



async def _create_client_for_user(session: AsyncSession, body: CreateClient):
  client_dal = ClientDAL(session)
  currency_dal = CurrencyDAL(session)
  model_data = body.model_dump()
  currency_id = model_data.pop('currency_id', 1)
  currency_data = await currency_dal.get_currency_by_id(currency_id)
  if currency_data is None:
      return errors.not_Found_error
  model_data.update(currency=currency_data)
  client = await client_dal.create_client_for_add_to_user(**model_data)
  return client



async def _get_all_clients(session: AsyncSession):
  async with session.begin():
    client_dal = ClientDAL(session)
    clients = await client_dal.get_all_clients()
    return list(clients)



async def _get_client_by_id(session: AsyncSession, client_id: int):
  async with session.begin():
    client_dal = ClientDAL(session)
    client = await client_dal.get_client_by_id(client_id=client_id)
    return client



async def _update_client_by_id(session: AsyncSession, body: UpdateClientRequest):
  async with session.begin():
    client_dal = ClientDAL(session)
    client_data = body.model_dump(exclude_none=True)
    client = await client_dal.get_client_by_id(client_id=client_data.get('id'))
    if client is None:
      return errors.not_Found_error
    updated_client = await client_dal.update_client_by_id(
      client_id=client_data.pop('id'),
      kwargs=client_data
    )
    return UpdateClientResponse(
      id=updated_client.id,
      name=updated_client.name,
      full_name=updated_client.full_name,
      certificate=updated_client.certificate,
      contract_number=updated_client.contract_number,
      contract_date=updated_client.contract_date,
      city=updated_client.city,
      address=updated_client.address,
      email=updated_client.email,
      phone=updated_client.phone,
      price=updated_client.price,
      currency_id=updated_client.currency_id,
      user_id=updated_client.user_id
    )



async def _delete_client_by_id(session: AsyncSession, client_id: int):
  async with session.begin():
    client_dal = ClientDAL(session)
    client = await client_dal.get_client_by_id(client_id=client_id)
    if client is None:
      return errors.not_Found_error
    deleted_client = await client_dal.delete_client(client_id)
    if deleted_client:
      return deleted_client



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


# async def _check_user_and_client(session: AsyncSession, user_id: int, client_group_id: int) -> bool:
#   async with session.begin():
#     client_dal = ClientDAL(session)
#     return await client_dal.check_group_access(
#       user_id=user_id, client_group_id=client_group_id
#     )
    