
from httpx import AsyncClient
from .test_a_users import (test_bad_token, create_test_super_user_access_token,
                           create_test_user_token, create_test_redactor_token)
from .test_data import client_clusters_data



async def test_update_role(ac: AsyncClient, create_test_super_user_access_token):
  updated_role_bad = await ac.patch('users/roles/4', params={'new_name': 'new role name'})
  assert updated_role_bad.status_code == 401
  updated_role_ok = await ac.patch('users/roles/4', params={'new_name': 'new role'}, headers={"Authorization": f"Bearer {create_test_super_user_access_token['access_token']}"})
  updated_role_ok.status_code == 200
  updated_role_db = updated_role_ok.json()
  assert updated_role_db['role_name'] == 'new role'


async def test_delete_user(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
  users_list = await ac.get('/users/', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert users_list.status_code == 200
  users_db = users_list.json()
  
  deleted_user = await ac.delete('users/5', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert deleted_user.status_code == 200
  deleted_user_data = deleted_user.json()
  assert deleted_user_data['id'] == 5
  users_after_del = await ac.get('/users/', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  users_after_db = users_after_del.json()
  assert len(users_db) == len(users_after_db)
  assert users_after_db[4]['is_active'] == False
  acces_unauthorized = await ac.delete('users/6', headers={'Authorization': f'Bearer {test_bad_token}'})
  assert acces_unauthorized.status_code == 401
  
  acces_denied_delete = await ac.delete('users/3', headers={'Authorization': f'Bearer {create_test_user_token["access_token"]}'})
  print(acces_denied_delete)
  acces_denied_delete_data = acces_denied_delete.json()
  print(acces_denied_delete_data)
  assert acces_denied_delete.status_code == 403


async def test_delete_client_from_group(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
  user_clients_group = await ac.get('/users/user_clients/2', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert user_clients_group.status_code == 200
  user_clients_group_db = user_clients_group.json()
  user_clients = user_clients_group_db['client_groups']
  assert len(user_clients) == 3
  body = {'client_group_id': 1, 'user_id': 2}
  delete_user_from_group = await ac.request(method='DELETE', url='/clients/client_groups/delete_user_from_client_group/', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'}, json=body)
  assert delete_user_from_group.status_code == 200
  user_clients_group_after = await ac.get('/users/user_clients/2', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert user_clients_group_after.status_code == 200
  user_clients_after_del = user_clients_group_after.json()
  user_clients_group_after_del = user_clients_after_del['client_groups']
  clients_len_after = len(user_clients_group_after_del)
  assert clients_len_after + 1 == len(user_clients)


async def test_delete_cluster(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
  cluster_before_delete = await ac.get('clients/client_cluster/without_client_groups', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert cluster_before_delete.status_code == 200
  cluster_before_db = cluster_before_delete.json()
  assert len(cluster_before_db) == len(client_clusters_data)
  delete_cluster = await ac.delete('clients/client_cluster/5', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert delete_cluster.status_code == 200
  cluster_after_delete = await ac.get('clients/client_cluster/without_client_groups', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert cluster_after_delete.status_code == 200
  cluster_after_db = cluster_after_delete.json()
  assert len(cluster_after_db) == len(cluster_before_db) - 1
  deleted_bad_req = await ac.delete('clients/client_cluster/1', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert deleted_bad_req.status_code == 400


# async def test_delete_colection(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token, create_test_redactor_token):pass