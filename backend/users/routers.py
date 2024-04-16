from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession



from backend.database import get_db
from backend.auth.security import super_user_permission, get_current_user_from_token
from backend.auth.errors import access_denied_error
from backend.auth.permissions import Permissions
from config import super_user_email
from backend.clients.schemas import CreateClient



from .schemas import ShowUser, CreateUser, UserRoleShow, UpdateRoleShow, UserUpdate, CreateSuperUser, DeleteUserResponse
from .handlers import (_create_user, _get_users, _get_user_by_id, _create_user_role, _get_all_roles, _get_role_by_id,
                       _update_role_by_id, _delete_role_by_id, _update_user, _create_super_user, _delete_user,
                       _update_user_role, _get_user_client, _add_user_clients)




router = APIRouter(
  prefix='/users',
  tags=['Users']
)




@router.post('/roles', response_model=UserRoleShow, status_code=status.HTTP_201_CREATED)
async def create_new_user_role(
  role_name: str, session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    created_role = await _create_user_role(session, role_name)
    if created_role is not None:
      return created_role
  else:    
    return access_denied_error



@router.get('/roles', response_model=List[UserRoleShow])
async def get_all_roles(
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    user_roles = await _get_all_roles(session)
    return user_roles
  else:
    return access_denied_error



@router.get('/roles/{role_id}', response_model=UserRoleShow)
async def get_role_by_id(
  role_id: int,
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    role = await _get_role_by_id(session, role_id)
    return role
  else:
    return access_denied_error
  


@router.patch('/roles/{role_id}', response_model=UpdateRoleShow)
async def update_role_by_id(
  role_id: int, new_name: str,
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    updated_role = await _update_role_by_id(
      session=session, role_id=role_id, new_name=new_name
    )
    return updated_role
  else:
    return access_denied_error
    



@router.delete('/roles/{role_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_role_by_id(
  role_id: int, session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    deleted_role = await _delete_role_by_id(session, role_id)
    return deleted_role
  else:
    return access_denied_error


# =============== Users routers ================

@router.post('/', response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(
  token: str,
  body: CreateUser | CreateSuperUser,
  session: AsyncSession = Depends(get_db)
):
  if body.email in super_user_email:
    created_user = await _create_super_user(session=session, body=body)
  else:
    current_user = await get_current_user_from_token(
      token=token,
      session=session
    )
    permission = Permissions(current_user=current_user)
    permission_role = await permission.superuser_permission()
    if permission_role:
      created_user = await _create_user(session=session, body=body)
    else:
      return access_denied_error
  return created_user



@router.get('/', response_model=List[ShowUser])
async def get_users(
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    return await _get_users(session)
  else:
    return access_denied_error



@router.get('/{user_id}', response_model=ShowUser)
async def get_user_by_id(
  user_id: int,
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    user = await _get_user_by_id(
      session=session,
      user_id=user_id
    )
    return user
  else:
    return access_denied_error



@router.patch('/{user_id}', response_model=ShowUser)
async def update_user(
  body: UserUpdate,
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    updated_user = await _update_user(session=session, body=body)
    return updated_user
  else:
    return access_denied_error



@router.patch('/user_role/{user_id}', response_model=ShowUser)
async def update_user_role(
  user_id: int,
  user_role_id: int,
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    updated_user_role = await _update_user_role(
      session=session,
      user_id=user_id,
      role_id=user_role_id
    )
    return updated_user_role
  else:
    return access_denied_error



@router.delete('/{user_id}', response_model=DeleteUserResponse)
async def delete_user(
  user_id: int,
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    deleted_user = await _delete_user(
      session=session,
      user_id=user_id
    )
    return deleted_user
  else:
    return access_denied_error



@router.get('/user_clients/{user_id}')
async def get_user_clients(
  user_id: int,
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    user_client = await _get_user_client(session=session, user_id=user_id)
    return user_client
  else:
    return access_denied_error



@router.post('/user_clients/{user_id}')
async def add_user_client(
  user_id: int,
  body: CreateClient,
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    add_clients = await _add_user_clients(
      session=session, user_id=user_id, body=body
    )
    return add_clients
  else:
    return access_denied_error