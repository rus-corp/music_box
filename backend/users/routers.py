from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from backend.database import get_db

from .schemas import ShowUser, CreateUser, UserRoleShow, DeleteUserRole, UpdateRoleShow
from .handlers import (_create_user, _get_users, _get_user_by_id, _create_user_role, _get_all_roles, _get_role_by_id,
                       _update_role_by_id, _delete_role_by_id)





router = APIRouter(
  prefix='/users',
  tags=['Users']
)



@router.post('/roles', response_model=UserRoleShow)
async def create_new_user_role(role_name: str, session: AsyncSession = Depends(get_db)):
  created_role = await _create_user_role(session, role_name)
  if created_role is not None:
    return created_role
  
@router.get('/roles', response_model=List[UserRoleShow])
async def get_all_roles(session: AsyncSession = Depends(get_db)):
  user_roles = await _get_all_roles(session)
  return user_roles

@router.get('/roles/{role_id}', response_model=UserRoleShow)
async def get_role_by_id(role_id: int, session: AsyncSession = Depends(get_db)):
  role = await _get_role_by_id(session, role_id)
  return role
  
@router.patch('/roles/{role_id}', response_model=UpdateRoleShow)
async def update_role_by_id(role_id: int, new_name: str, session: AsyncSession = Depends(get_db)):
  updated_role = await _update_role_by_id(
    session=session, role_id=role_id, new_name=new_name
  )
  return updated_role


@router.delete('/roles/{role_id}', response_model=DeleteUserRole)
async def delete_role_by_id(role_id: int, session: AsyncSession = Depends(get_db)):
  deleted_role = await _delete_role_by_id(session, role_id)
  return deleted_role



# =============== Users routers ================
@router.get('/', response_model=List[ShowUser])
async def get_users(session: AsyncSession = Depends(get_db)) -> ShowUser:
  return await _get_users(session)


@router.post('/', response_model=ShowUser)
async def create_user(body: CreateUser, session: AsyncSession = Depends(get_db)):
  created_user = await _create_user(session=session, body=body)
  return created_user


@router.get('/{user_id}', response_model=ShowUser)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_db)):
  user = await _get_user_by_id(
    session=session,
    user_id=user_id
  )
  return user