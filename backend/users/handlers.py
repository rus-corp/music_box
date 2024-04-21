from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from .dals import UserDAL, UserRoleDAL
from .schemas import CreateUser, ShowUser, UpdateRoleShow, UserUpdate, UserRoleShow, CreateSuperUser
from backend.auth.service import Hasher
from backend.auth.errors import not_Found_error
from backend.clients.handlers.clients_hand import _create_client_for_user
from backend.clients.schemas import CreateClient, ShowUserClients



async def _create_user_role(session: AsyncSession, name: str):
  async with session.begin():
    role_dal = UserRoleDAL(session)
    created_role = await role_dal.create_user_role(name)
    await session.commit()
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
      return not_Found_error
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
async def _get_user_by_email(session: AsyncSession, email: str):
  async with session.begin():
    user_dal = UserDAL(session)
    return await user_dal.get_user_by_email(email)



async def _create_super_user(session: AsyncSession, body: CreateUser | CreateSuperUser):
  async with session.begin():
    user_dal = UserDAL(session)
    body_data = body.model_dump(exclude_none=True)
    role_dal = UserRoleDAL(session)
    role = await role_dal.get_role_by_name('superuser')
    if role is None:
      role = await role_dal.create_user_role('superuser')
    body_data.update({'is_superuser': True})
    super_user, error = await user_dal.create_user(
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



async def _create_user(session: AsyncSession, body: CreateUser):
  async with session.begin():
    user_dal = UserDAL(session)
    body_data = body.model_dump(exclude_none=True)
    role_dal = UserRoleDAL(session)
    role = await role_dal.get_user_role_by_id(id=body_data['role_id'])
    new_user, error = await user_dal.create_user(
      name=body_data.get('name'),
      login=body_data.get('login'),
      email=body_data.get('email'),
      password=Hasher.get_hasher_password(body_data['password']),
      comment=body_data.get('comment', None),
      role=role
    )
    if error:
      message_start_index = error.find('DETAIL: ')
      message_end_index = error.find('[SQL:')
      if message_start_index != -1:
        message = error[message_start_index:message_end_index].rstrip()
      return JSONResponse(status_code=400, content=message)
    return new_user


async def _get_users(session: AsyncSession):
  async with session.begin():
    user_dal = UserDAL(session)
    users = await user_dal.get_users()
    return list(users)


async def _get_user_by_id(session: AsyncSession, user_id: int):
  async with session.begin():
    user_dal = UserDAL(session)
    user = await user_dal.get_user_by_id_with_role(user_id)
    if user is None:
      return not_Found_error
    return user


async def _update_user(session: AsyncSession, body: UserUpdate):
  async with session.begin():
    user_dal = UserDAL(session)
    role_dal = UserRoleDAL(session)
    user_data = body.model_dump(exclude_none=True)
    user = await user_dal.get_user_by_id(user_data.get('id'))
    if user is None:
      return not_Found_error
    update_user = await user_dal.update_user_by_id(
      user_id=user_data.pop('id'),
      kwargs=user_data
    )
    user_role = UserRoleShow(
      id=update_user.role.id,
      role_name=update_user.role.role_name
    )
    updated_user_data = ShowUser(
      id=update_user.id,
      name=update_user.name,
      login=update_user.login,
      email=update_user.email,
      is_active=update_user.is_active,
      comment=update_user.comment,
      is_superuser=update_user.is_superuser,
      role=user_role
    )
    return updated_user_data



async def _update_user_role(session: AsyncSession, user_id: int, role_id: int):
  async with session.begin():
    user_dal = UserDAL(session)
    user_data = await user_dal.get_user_by_id(user_id=user_id)
    if user_data is None:
      return not_Found_error
    updated_user_role = await user_dal.update_user_role(
      user_id=user_id, role_id=role_id
    )
    return updated_user_role
    


async def _delete_user(session: AsyncSession, user_id: int):
  async with session.begin():
    user_dal = UserDAL(session)
    user_data = await user_dal.get
    user = await user_dal.delete_user_by_id(user_id=user_id)
    if user is None:
      return not_Found_error
    deleted_user = await user_dal.delete_user_by_id(user_id=user_id)
    return deleted_user


async def _get_user_client(session: AsyncSession, user_id: int):
  async with session.begin():
    user_dal = UserDAL(session)
    user_clients= await user_dal.get_user_clients(user_id=user_id)
    return user_clients


async def _add_user_clients(session: AsyncSession, user_id: int, body: CreateClient):
  async with session.begin():
    user_dal = UserDAL(session)
    user = await user_dal.get_user_by_id(user_id)
    new_client = await _create_client_for_user(
      session=session, body=body
    )
    user.client.append(new_client)
    await session.commit()
    client = ShowUserClients(
      client_id=new_client.id,
      name=new_client.name,
      full_name=new_client.full_name,
      certificate=new_client.certificate,
      contract_number=new_client.contract_number,
      contract_date=new_client.contract_date,
      city=new_client.city,
      address=new_client.address,
      email=new_client.email,
      phone=new_client.phone,
      price=new_client.price,
      currency=new_client.currency
    )
    return ShowUser(
      id=user.id,
      name=user.name,
      login=user.login,
      email=user.email,
      is_active=user.is_active,
      comment=user.comment,
      is_superuser=user.is_superuser,
      role=user.role,
      client=client
    )