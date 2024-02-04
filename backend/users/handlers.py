from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from .services import UserDAL, UserRoleDAL
from .schemas import CreateUser, ShowUser, UpdateRoleShow


async def _create_user_role(session: AsyncSession, name: str):
  async with session.begin():
    role_dal = UserRoleDAL(session)
    created_role = await role_dal.create_user_role(name)
    if created_role is not None:
      return created_role
  
  
async def _get_all_roles(session: AsyncSession):
  async with session.begin():
    role_dal = UserRoleDAL(session)
    user_roles = await role_dal.get_user_roles()
    return list(user_roles)
  
async def _get_role_by_id(session: AsyncSession, role_id):
  async with session.begin():
    role_dal = UserRoleDAL(session)
    role = await role_dal.get_user_role_by_id(role_id)
    if role is None:
      return JSONResponse(content=f'Role with {role_id} not found', status_code=404)
    return role
  
  
async def _update_role_by_id(session: AsyncSession, role_id: int, new_name: str):
  async with session.begin():
    role_dal = UserRoleDAL(session)
    role = await role_dal.get_user_role_by_id(role_id)
    if role is None:
      raise HTTPException(status_code=404, detail=f'Role with {role_id} not found')
    updated_role = await role_dal.update_user_role(role_id, new_name)
    if updated_role is not None:
      return UpdateRoleShow(
        id=updated_role.id,
        role_name=updated_role.role_name
      )
    

async def _delete_role_by_id(session: AsyncSession, role_id: int):
  async with session.begin():
    role_dal = UserRoleDAL(session)
    role = await role_dal.get_user_role_by_id(role_id)
    if role is None:
      raise HTTPException(status_code=404, detail=f'Role with {role_id} not found')
    deleted_role = await role_dal.delete_user_role(role_id)
    if deleted_role is not None:
      return deleted_role




# ==================== User Handlers ===================
async def _create_user(session: AsyncSession, body: CreateUser):
  async with session.begin():
    user_dal = UserDAL(session)
    body_data = body.model_dump(exclude_none=True)
    role_dal = UserRoleDAL(session)
    role = await role_dal.get_user_role_by_id(id=body_data['role_id'])
    new_user = await user_dal.create_user(
      name=body_data.get('name'),
      login=body_data.get('login'),
      password=body_data.get('password'),
      comment=body_data.get('comment'),
      role=role
    )
    return new_user


async def _get_users(session):
  async with session.begin():
    user_dal = UserDAL(session)
    users = await user_dal.get_users()
    return list(users)
  
  
async def _get_user_by_id(session: AsyncSession, user_id: int):
  async with session.begin():
    user_dal = UserDAL(session)
    user = await user_dal.get_user_by_id(user_id)
    return user
    # return ShowUser(
    #   id=id,
    #   role=
    # )