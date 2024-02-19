from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse



from backend.database import async_session_maker
from .schemas import ShowClient, CreateClient
from .dals import ClientDAL
from backend.music.dals.track_group_dal import TrackCollectionDAL


async def _create_client(body: CreateClient) -> ShowClient:
  async with async_session_maker() as session:
    async with session.begin():
      client_dal = ClientDAL(session)
      client = await client_dal.create_client(**body)
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
      )
      
      
async def _get_clients(session: AsyncSession):
  async with session.begin():
    client_dal = ClientDAL(session)
    clients = await client_dal.get_clients()
    return clients
  
  
async def _delete_client_in_trackcollection(session: AsyncSession, track_collection_id: int, client_id: int):
  async with session.begin():
    track_collection_dal = TrackCollectionDAL(session)
    deleted_client_in_track_collection = await track_collection_dal.delete_client_in_group_collection(
      track_collection_id=track_collection_id, client_id=client_id
    )
    return JSONResponse(content=f'Deleted {deleted_client_in_track_collection} rows', status_code=204)