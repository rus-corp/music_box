from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession



from backend.database import get_db
from backend.auth.security import super_user_permission, get_current_user_from_token
from backend.auth.errors import access_denied_error
from backend.auth.permissions import Permissions
from config import super_user_email



from .handlers import UserRoleHandler, UserHandler
from .schemas import (ShowUser, CreateUser, UserRoleShow, UpdateRoleShow, UserUpdateRequest,
                      CreateSuperUser, DeleteUserResponse, UserUpdateResponse)
from backend.general_schemas import UserWithClient




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
    role_handler = UserRoleHandler(session)
    created_role = await role_handler._create_user_role(role_name)
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
    role_handler = UserRoleHandler(session)
    user_roles = await role_handler._get_all_roles()
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
    role_handler = UserRoleHandler(session)
    role = await role_handler._get_role_by_id(role_id)
    return role
  else:
    return access_denied_error
  


@router.patch('/roles/{role_id}', response_model=UpdateRoleShow, status_code=status.HTTP_200_OK)
async def update_role_by_id(
  role_id: int, new_name: str,
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    role_handler = UserRoleHandler(session)
    updated_role = await role_handler._update_role_by_id(
      role_id=role_id, new_name=new_name
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
    role_handler = UserRoleHandler(session)
    deleted_role = await role_handler._delete_role_by_id(role_id)
    return deleted_role
  else:
    return access_denied_error


# =============== Users routers ================

@router.post('/', response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(
  body: CreateUser | CreateSuperUser,
  session: AsyncSession = Depends(get_db),
  token: str = None,
):
  user_handler = UserHandler(session)
  if body.email in super_user_email:
    
    created_user = await user_handler._create_super_user(body=body)
  else:
    current_user = await get_current_user_from_token(
      token=token,
      session=session
    )
    permission = Permissions(current_user=current_user)
    permission_role = await permission.superuser_permission()
    if permission_role:
      created_user = await user_handler._create_user(body=body)
    else:
      return access_denied_error
  return created_user



@router.get('/', response_model=List[ShowUser])
async def get_users(
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    user_handler = UserHandler(session)
    return await user_handler._get_users()
  else:
    return access_denied_error



@router.get('/{user_id}', response_model=ShowUser)
async def get_user_by_id(
  user_id: int,
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    user_handler = UserHandler(session)
    user = await user_handler._get_user_by_id(
      user_id=user_id
    )
    return user
  else:
    return access_denied_error



@router.patch('/{user_id}', response_model=UserUpdateResponse, status_code=status.HTTP_200_OK)
async def update_user(
  user_id: int,
  body: UserUpdateRequest,
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    user_handler = UserHandler(session)
    updated_user = await user_handler._update_user(user_id=user_id, body=body)
    return updated_user
  else:
    return access_denied_error


@router.delete('/{user_id}', response_model=DeleteUserResponse, status_code=status.HTTP_200_OK)
async def delete_user(
  user_id: int,
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    user_handler = UserHandler(session)
    deleted_user = await user_handler._delete_user(
      user_id=user_id
    )
    return deleted_user
  else:
    return access_denied_error



@router.get('/user_clients/{user_id}', status_code=status.HTTP_200_OK, response_model=UserWithClient)
async def get_user_clients(
  user_id: int,
  session: AsyncSession = Depends(get_db),
  permissions: bool = Depends(super_user_permission)
):
  if permissions:
    user_handler = UserHandler(session)
    user_client = await user_handler._get_user_client(user_id=user_id)
    return user_client
  else:
    return access_denied_error
