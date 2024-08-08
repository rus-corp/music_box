from httpx import AsyncClient
import json
from fastapi.exceptions import HTTPException
import pytest


from .test_data import users_data, user_roles_data, client_clusters_data
from backend.auth.security import create_access_token

test_bad_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJydXNAZ21haWasdaffcWDasdaIiwicm9sZSI6InN1cGVydXNlciIsImV4cCI6MTcxOTEyOTcwMH0.dRML3C5z2LEr1d1Tlte6McgJ63bTkrG54IIYsHvzRWk'

@pytest.fixture(scope='session')
def create_test_super_user_access_token():
  super_user = users_data[0]
  token = create_access_token(
    data={'sub': super_user['email'], 'role': 'superuser'}
  )
  return {'access_token': token, 'token_type': 'bearer'}


@pytest.fixture(scope='session')
def create_test_user_token():
  user = users_data[1]
  token = create_access_token(
    data={'sub': user['email'], 'role': 'client'}
  )
  return {'access_token': token, 'token_type': 'bearer'}


@pytest.fixture(scope='session')
def create_test_redactor_token():
  user = users_data[-1]
  token = create_access_token(
    data={'sub': user['email'], 'role': 'redactor'}
  )
  return {'access_token': token, 'token_type': 'bearer'}


@pytest.fixture(scope='session')
def create_test_empty_user_token():
  user = users_data[-2]
  token = create_access_token(
    data={'sub': user['email'], 'role': 'manager'}
  )
  return {'access_token': token, 'token_type': 'bearer'}










async def test_create_super_user(ac: AsyncClient):
  super_create = await ac.post('/users/', json=users_data[0])
  assert super_create.status_code == 201


# ================ USER ROLES TESTS ==========================
async def test_create_role(ac: AsyncClient, create_test_super_user_access_token):
  token = create_test_super_user_access_token['access_token']
  for role in user_roles_data:
    create_role = await ac.post('/users/roles', params={'role_name': role['role_name']}, headers={"Authorization": f"Bearer {token}"})
    assert create_role.status_code == 201
  after_create = await ac.get('users/roles', headers={"Authorization": f"Bearer {token}"})
  db_rec = after_create.json()
  assert len(db_rec) == 4
  assert db_rec[1]['role_name'] == user_roles_data[0]['role_name']


async def test_get_role_by_id(ac: AsyncClient, create_test_super_user_access_token):
  token = create_test_super_user_access_token['access_token']
  role_data = await ac.get('/users/roles/2', headers={"Authorization": f"Bearer {token}"})
  role_db = role_data.json()
  assert role_data.status_code == 200
  assert role_db['role_name'] == 'client'
  role_bad_request = await ac.get('/users/roles/2')
  assert role_bad_request.status_code == 401
  not_found_role = await ac.get('/users/roles/6', headers={"Authorization": f"Bearer {token}"})
  assert not_found_role.status_code == 404
  







# ================ USER TESTS ==========================

async def test_create_users(ac: AsyncClient, create_test_super_user_access_token):
  token = create_test_super_user_access_token['access_token']
  for user in users_data[1:]:
    user_create = await ac.post('/users/', json=user, params={'token': token})
    assert user_create.status_code == 201
  user_list = await ac.get('/users/', headers={'Authorization': f'Bearer {token}'})
  assert user_list.status_code == 200
  db_users = user_list.json()
  assert len(db_users) == len(users_data)
  acces_denied_response = await ac.get('/users/')
  assert acces_denied_response.status_code == 401
  


async def test_get_user_by_id(ac: AsyncClient, create_test_super_user_access_token):
  token = create_test_super_user_access_token['access_token']
  user = await ac.get('/users/2', headers={'Authorization': f'Bearer {token}'})
  user_db = user.json()
  assert user.status_code == 200
  assert user_db['name'] == 'ven'
  user_bad_request = await ac.get('/users/3')
  assert user_bad_request.status_code == 401
  user_not_found_request = await ac.get('/users/33', headers={'Authorization': f'Bearer {token}'})
  assert user_not_found_request.status_code == 404


async def test_update_user(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
  super_token = create_test_super_user_access_token['access_token']
  body = {'name': 'new NAME', 'comment': 'new user comment'}
  updated_user_bad = await ac.patch('users/2')
  assert updated_user_bad.status_code == 401
  update_user_ok = await ac.patch('users/3', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'}, json=body)
  assert update_user_ok.status_code == 200
  updated_user_db = await ac.get('users/3', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert updated_user_db.status_code == 200
  updated_user_data = updated_user_db.json()
  assert updated_user_data['name'] == body['name']
  assert updated_user_data['comment'] == body['comment']
  
  access_denied_request = await ac.patch('users/4', headers={'Authorization': f'Bearer {create_test_user_token["access_token"]}'}, json=body)
  assert access_denied_request.status_code == 403

  

  










# async def test_add_user_to_client_group(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token): pass


# async def test_get_user_clients(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
#   user_clients_list = await ac.get('user_clients/', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})


# async def test_remove_user_from_client_group(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token): pass
# async def test_change_user_client_group(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token): pass