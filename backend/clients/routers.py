from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from backend.database import get_db

from .handlers import (_get_clients, _create_client,
                       _delete_client_in_trackcollection)
from .schemas import ShowClient, CreateClient



router = APIRouter(
  prefix='/clients',
  tags=['Clients']
)



@router.get('/')
async def get_clients(session: AsyncSession = Depends(get_db)):
  res = await _get_clients(session)
  return res



@router.post('/', response_model=ShowClient)
async def create_client(body: CreateClient) -> ShowClient:
  res = await _create_client(body)
  return res



@router.post('/add_client_to_track_collection/{track_collection_id}')
async def add_client_to_track_collection(track_collection_id: int, session: AsyncSession = Depends(get_db)):
  pass


@router.delete('/delete_client_in_track_collections/{track_collection_id}', )
async def delete_client_in_track_collection(track_collection_id: int,
                                            client_id: int,
                                            session: AsyncSession = Depends(get_db)):
  deleted_client_in_track_collection = await _delete_client_in_trackcollection(
    session, track_collection_id, client_id
  )
  return deleted_client_in_track_collection