from httpx import AsyncClient


from .test_data import (client_clusters_data, client_groups_data, currency_data,
                        client_data, client_profile, append_user_to_client_group_list)
from .test_a_users import test_bad_token, create_test_super_user_access_token, create_test_user_token


async def test_update_client_cluster(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
  body = {'cluster_id': 1, 'name': 'new name'}
  cluster_update = await ac.patch('clients/client_cluster/1', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'}, params=body)
  assert cluster_update.status_code == 200
  cluster_db = cluster_update.json()
  assert cluster_db['id'] == 1
  assert cluster_db['name'] == body['name']
  cluster_bad_req = await ac.patch('clients/client_cluster/1', params=body, headers={'Authorization': f'Bearer {test_bad_token}'})
  assert cluster_bad_req.status_code == 401
  cluster_access_denied = await ac.patch('clients/client_cluster/1', params=body, headers={'Authorization': f'Bearer {create_test_user_token["access_token"]}'})
  assert cluster_access_denied.status_code == 405



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


async def test_update_client_group(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
  new_data = {'name': 'new group name', 'comment': 'new comment', 'client_cluster_id':4 }
  client_group_before_change = await ac.get('/clients/client_groups/with_clients/1', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert client_group_before_change.status_code == 200
  client_group_before_change_db = client_group_before_change.json()
  group_id = client_group_before_change_db['id']
  assert client_group_before_change_db['name'] == client_groups_data[group_id - 1]['name']
  assert client_group_before_change_db['client_cluster']['id'] == client_groups_data[group_id - 1]['client_cluster_id']
  
  updated_client_group = await ac.patch('/clients/client_groups/1', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'}, json=new_data)
  updated_client_group.status_code == 200
  updated_client_group_data = updated_client_group.json()
  assert updated_client_group_data['name'] == new_data['name']
  assert updated_client_group_data['comment'] == new_data['comment']
  assert updated_client_group_data['client_cluster'] == new_data['client_cluster_id']
  
  updated_client_group_after_from_db = await ac.get('/clients/client_groups/with_clients/1', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert updated_client_group_after_from_db.status_code == 200
  updated_group_db = updated_client_group_after_from_db.json()
  assert updated_group_db['id'] == group_id
  assert updated_group_db['name'] == new_data['name']
  assert updated_group_db['client_cluster']['id'] == new_data['client_cluster_id']
  

# async def test_update_client(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):pass


# async def test_delete_client_group(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):pass

# async def test_delete_cleient(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):pass