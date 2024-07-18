from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from .dals import UserDAL, UserRoleDAL
from .schemas import (CreateUser, ShowUser, UpdateRoleShow, UserUpdateRequest,
                      UserRoleShow, CreateSuperUser, UserUpdateResponse,
                      DeleteUserResponse)
from backend.auth.service import Hasher
from backend.auth.errors import not_Found_error




class UserRoleHandler:
  def __init__(self, session: AsyncSession) -> None:
    self.session = session
    self.role_dal = UserRoleDAL(self.session)
  
  
  async def _create_user_role(self, name: str):
    async with self.session.begin():
      created_role = await self.role_dal.create_user_role(name)
      await self.session.commit()
      if created_role is not None:
        return created_role
  
  
  async def _get_all_roles(self):
    async with self.session.begin():
      user_roles = await self.role_dal.get_user_roles()
      return list(user_roles)
  
  
  async def _get_role_by_id(self, role_id: int):
    async with self.session.begin():
      role = await self.role_dal.get_user_role_by_id(role_id)
      if role is None:
        return not_Found_error
      return role

  
  async def _update_role_by_id(self, role_id: int, new_name: str):
    async with self.session.begin():
      role = await self.role_dal.get_user_role_by_id(role_id)
      if role is None:
        raise HTTPException(status_code=404, detail=f'Role with {role_id} not found')
      updated_role = await self.role_dal.update_user_role(role_id, new_name)
      if updated_role is not None:
        return UpdateRoleShow(
          id=updated_role.id,
          role_name=updated_role.role_name
        )

  
  # async def _delete_role_by_id(self, role_id: int):
  #   async with self.session.begin():
  #     role = await self.role_dal.get_user_role_by_id(role_id)
  #     if role is None:
  #       raise HTTPException(status_code=404, detail=f'Role with {role_id} not found')
  #     deleted_role = await self.role_dal.delete_user_role(role_id)
  #     if deleted_role is not None:
  #       return deleted_role




# ==================== User Handlers ===================
class UserHandler:
  def __init__(self, session: AsyncSession) -> None:
    self.session = session
    self.user_dal = UserDAL(self.session)
  
  
  async def _get_user_by_email(self, email: str):
    async with self.session.begin():
      return await self.user_dal.get_user_by_email(email)
  
  
  async def _create_super_user(self, body: CreateUser | CreateSuperUser):
    async with self.session.begin():
      body_data = body.model_dump(exclude_none=True)
      role_dal = UserRoleDAL(self.session)
      role = await role_dal.get_role_by_name('superuser')
      if role is None:
        role = await role_dal.create_user_role('superuser')
      body_data.update({'is_superuser': True})
      super_user, error = await self.user_dal.create_user(
        name=body_data.get('name'),
        login=body_data.get('login'),
        email=body_data.get('email'),
        password=Hasher.get_hasher_password(body_data['password']),
        is_superuser=body_data.get('is_superuser'),
        comment=body_data.get('comment', None),
        role=role
      )
      if error:
        message_start_index = error.find('DETAIL: ')
        message_end_index = error.find('[SQL:')
        if message_start_index != -1:
          message = error[message_start_index:message_end_index].rstrip()
        return JSONResponse(status_code=400, content=message)
      return super_user
  
  
  async def _create_user(self, body: CreateUser):
    async with self.session.begin():
      body_data = body.model_dump(exclude_none=True)
      role_dal = UserRoleDAL(self.session)
      role = await role_dal.get_user_role_by_id(id=body_data['role_id'])
      new_user, error = await self.user_dal.create_user(
      name=body_data.get('name'),
      login=body_data.get('login'),
      email=body_data.get('email'),
      password=Hasher.get_hasher_password(body_data['password']),
      comment=body_data.get('comment', None),
      role=role)
      if error:
        message_start_index = error.find('DETAIL: ')
        message_end_index = error.find('[SQL:')
        if message_start_index != -1:
          message = error[message_start_index:message_end_index].rstrip()
        return JSONResponse(status_code=400, content=message)
      return new_user
  
  
  async def _get_users(self):
    async with self.session.begin():
      users = await self.user_dal.get_users()
      return list(users)
  
  
  async def _get_user_by_id(self, user_id: int):
    async with self.session.begin():
      user = await self.user_dal.get_user_by_id_with_role(user_id)
      if user is None:
        return not_Found_error
      return user
  
  
  async def _update_user(self, user_id: int, body: UserUpdateRequest):
    async with self.session.begin():
      user_data = body.model_dump(exclude_none=True)
      user = await self.user_dal.get_user_by_id_with_role(user_id)
      if user is None:
        return not_Found_error
      update_user = await self.user_dal.update_user_by_id(
        user_id=user_id,
        kwargs=user_data
      )
      return update_user
  
  
  async def _delete_user(self, user_id: int):
    async with self.session.begin():
      user = await self.user_dal.get_user_by_id_with_role(user_id=user_id)
      if user is None:
        return not_Found_error
      deleted_user = await self.user_dal.delete_user_by_id(user_id=user_id)
      return DeleteUserResponse(id=deleted_user)
  
  
  async def _get_user_client(self, user_id: int):
    async with self.session.begin():
      user = await self.user_dal.get_user_by_id_with_role(user_id=user_id)
      if user is None:
        return not_Found_error
      user_clients= await self.user_dal.get_user_clients(user_id=user_id)
      return user_clients



