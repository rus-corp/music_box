from httpx import AsyncClient


from .test_data import client_clusters_data, client_groups_data
from .test_a_users import test_bad_token, create_test_super_user_access_token, create_test_user_token



async def test_create_client_cluster(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
  for item in client_clusters_data:
    client_cluster = await ac.post('/clients/client_cluster/', params={'name': item['name']}, headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
    assert client_cluster.status_code == 201
  client_cluster_req = await ac.get('clients/client_cluster/without_client_groups', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert client_cluster_req.status_code == 200
  cluster_data = client_cluster_req.json()
  assert len(cluster_data) == len(client_clusters_data)
  
  cluster_create_bad = await ac.post('/clients/client_cluster/', headers={'Authorization': f'Bearer {test_bad_token}'})
  assert cluster_create_bad.status_code == 401
  
  cluster_create_access_denied = await ac.post('/clients/client_cluster/', params={'name': 'test name'}, headers={'Authorization': f'Bearer {create_test_user_token["access_token"]}'})
  assert cluster_create_access_denied.status_code == 405



async def test_get_client_cluster_by_id(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
  client_cluster = await ac.get('clients/client_cluster/cluster_without_client_group/1', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert client_cluster.status_code == 200
  cluster_db = client_cluster.json()
  assert cluster_db['name'] == client_clusters_data[0]['name']


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
  delete_cluster = await ac.delete('clients/client_cluster/1', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert delete_cluster.status_code == 200
  cluster_after_delete = await ac.get('clients/client_cluster/without_client_groups', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert cluster_after_delete.status_code == 200
  cluster_after_db = cluster_after_delete.json()
  assert len(cluster_after_db) == len(cluster_before_db) - 1





# (ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
# (ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
