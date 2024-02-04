from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from backend.database import get_db
from .handlers import _get_clients, _create_client
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