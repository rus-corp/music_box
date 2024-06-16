from httpx import AsyncClient
import json
from fastapi.exceptions import HTTPException
import pytest


from .test_data import users_data, user_roles_data
from backend.auth.security import create_access_token


#access_token = create_access_token(
  #   data={'sub': user.email, 'role': user.role.role_name},
  #   expires_delta=access_token_expires
  # )


# @pytest.mark.asyncio
# async def test_authenticate_user(session):
#   session.add(users_data[0])
#   await session.commit()
  
#   user = await _authenticate_user(session, user_roles_data[0])
#   assert user is not None

# @pytest.fixture(scope='session')
# def auth_token(ac: AsyncClient, user):
#   token = ac.post('/auth/token', json=user)
#   return token


@pytest.fixture(scope='session')
def create_test_access_token():
  super_user = users_data[0]
  token = create_access_token(
    data={'sub': super_user['email'], 'role': 'superuser'}
  )
  return {'access_token': token, 'token_type': 'bearer'}



async def test_create_super_user(ac: AsyncClient):
  super_create = await ac.post('/users/', json=users_data[0])
  assert super_create.status_code == 201


async def test_create_role(ac: AsyncClient, create_test_access_token):
  for role in user_roles_data:
    create_role = await ac.post('/users/roles', params={'role_name': role['role_name']}, headers={"Authorization": f"Bearer {create_test_access_token['access_token']}"})
    assert create_role.status_code == 201
  after_create = await ac.get('users/roles', headers={"Authorization": f"Bearer {create_test_access_token['access_token']}"})
  db_rec = after_create.json()
  assert len(db_rec) == 4
  assert db_rec[1]['role_name'] == user_roles_data[0]['role_name']


# async def test_update_role(ac: AsyncClient, create_test_access_token):
#   updated_role_bad = await ac.patch('users/roles', params={'role_name': 'new role name'})
#   assert updated_role_bad.status_code == 422
#   updated_role_ok = await ac.patch('users/roles', params={'role_name': 'new role name'}, headers={"Authorization": f"Bearer {create_test_access_token['access_token']}"})



async def test_create_users(ac: AsyncClient, create_test_access_token):
  for user in users_data[1:]:
    user_create = await ac.post('/users/', json=user, params={'token': create_test_access_token['access_token']})
    assert user_create.status_code == 201
  

# async def test_get_users(ac: AsyncClient): pass

# async def test_get_user_by_id(ac: AsyncClient): pass

# async def test_update_user(ac: AsyncClient): pass

# async def test_delete_user(ac: AsyncClient): pass

# async def test_get_user_clients(ac: AsyncClient): pass

# async def test_create_user_role(ac: AsyncClient):
#   super_resp = ac.post('/users', json=users_data[0])
#   assert super_resp.status_code == 200
  
  





# async def test_get_roles(ac: AsyncClient): pass

# async def test_get_user_role(ac: AsyncClient): pass

# async def test_update_user_role(ac: AsyncClient): pass

# async def test_delete_user_role(ac: AsyncClient): pass