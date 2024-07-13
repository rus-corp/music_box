from httpx import AsyncClient


from .test_data import (client_clusters_data, client_groups_data, currency_data,
                        client_data, client_profile, append_user_to_client_group_list)
from .test_a_users import test_bad_token, create_test_super_user_access_token, create_test_user_token



async def test_create_client_cluster(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
  for item in client_clusters_data:
    client_cluster = await ac.post('/clients/client_cluster/', params={'name': item['name']}, headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
    assert client_cluster.status_code == 201
  client_cluster_req = await ac.get('clients/client_cluster/without_client_groups', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert client_cluster_req.status_code == 200
  cluster_data = client_cluster_req.json()
  print(cluster_data)
  assert len(cluster_data) == len(client_clusters_data)
  
  cluster_create_bad = await ac.post('/clients/client_cluster/', headers={'Authorization': f'Bearer {test_bad_token}'})
  assert cluster_create_bad.status_code == 401
  
  cluster_create_access_denied = await ac.post('/clients/client_cluster/', params={'name': 'test name'}, headers={'Authorization': f'Bearer {create_test_user_token["access_token"]}'})
  assert cluster_create_access_denied.status_code == 405




async def test_create_currency(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
  for item in currency_data:
    curency = await ac.post('/clients/currency/', params={'currency_name': item['currency_name']}, headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
    assert curency.status_code == 201
  curencies = await ac.get('/clients/currency/', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert curencies.status_code == 200
  curency_db = curencies.json()
  assert len(curency_db) == len(currency_data)
  assert curency_db[0]['cur_name'] == currency_data[0]['currency_name']
  curency_bad_req = await ac.post('/clients/currency/', params={'currency_name': item['currency_name']}, headers={'Authorization': f'Bearer {create_test_user_token["access_token"]}'})
  assert curency_bad_req.status_code == 405
  
  
  

async def test_create_client_group(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
  for item in client_groups_data:
    body = {'name': item['name'], 'comment': item['comment'], 'client_cluster_id': item['client_cluster_id']}
    client_group = await ac.post('/clients/client_groups/', json=body, headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
    assert client_group.status_code == 201
  client_group_db = await ac.get('/clients/client_groups/', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert client_group_db.status_code == 200
  client_group_list = client_group_db.json()
  assert len(client_group_list) == len(client_groups_data)
  client_group_bad_req = await ac.get('/clients/client_groups/', headers={'Authorization': f'Bearer {test_bad_token}'})
  assert client_group_bad_req.status_code == 401
  client_group_acces_denied = await ac.post('/clients/client_groups/', headers={'Authorization': f'Bearer {create_test_user_token["access_token"]}'}, json=body)
  assert client_group_acces_denied.status_code == 405
  


async def test_create_cleints_with_profile(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
  for ind, item in enumerate(client_data):
    params = {"name": item['name'], "city": item['city'], "email": item['email'], "phone": item['phone'], "price": item['price'], "client_group_id": item['client_group_id'], "currency_id": item['currency_id'],
              'profile': client_profile[ind]}
    client_create = await ac.post('/clients/', json=params, headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
    assert client_create.status_code == 201
  clients_db = await ac.get('/clients/', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert clients_db.status_code == 200
  clients_list = clients_db.json()
  assert len(clients_list) == len(client_data)


async def test_one_item(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
  cluster_db = await ac.get('clients/client_cluster/cluster_without_client_group/1', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert cluster_db.status_code == 200
  client_group_db = await ac.get('/clients/client_groups/1', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert client_group_db.status_code == 200
  client_db = await ac.get('/clients/1', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
  assert client_db.status_code == 200
  
  cluster_item = cluster_db.json()
  group_item = client_group_db.json()
  client_item = client_db.json()
  
  assert cluster_item['name'] == client_clusters_data[0]['name']
  assert group_item['name'] == client_groups_data[0]['name']
  assert client_item['name'] == client_data[0]['name']




from collections import Counter

async def test_append_client_to_client_group(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
  for item in append_user_to_client_group_list:
    append_client = await ac.post('/clients/client_groups/append_user_to_client_group', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'}, json=item)
    assert append_client.status_code == 201
  for item in append_user_to_client_group_list:
    user_clients = await ac.get(f'/users/user_clients/{item["user_id"]}', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
    assert user_clients.status_code == 200
    user_clients_data = user_clients.json()
    user_clients = user_clients_data.get('client_groups')
    filterd_clients = [entry['client_group_id'] for entry in append_user_to_client_group_list if entry['user_id'] == user_clients_data['id']]
    counter = Counter(filterd_clients)
    assert len(user_clients) == len(counter)




# async def test_get_client_group_with_clients(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
#   client_groups = await ac.get('clients/client_groups/with_clients/', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
#   assert client_groups.status_code == 200
#   client_groups_list = client_groups.json()
#   for item in client_groups_list:
#     assert item['clients']
  


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



# async def test_delete_cluster(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
#   cluster_before_delete = await ac.get('clients/client_cluster/without_client_groups', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
#   assert cluster_before_delete.status_code == 200
#   cluster_before_db = cluster_before_delete.json()
#   assert len(cluster_before_db) == len(client_clusters_data)
#   delete_cluster = await ac.delete('clients/client_cluster/1', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
#   assert delete_cluster.status_code == 200
#   cluster_after_delete = await ac.get('clients/client_cluster/without_client_groups', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
#   assert cluster_after_delete.status_code == 200
#   cluster_after_db = cluster_after_delete.json()
#   assert len(cluster_after_db) == len(cluster_before_db) - 1









# async def test_get_client_cluster_by_id(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token):
#   client_cluster = await ac.get('clients/client_cluster/cluster_without_client_group/1', headers={'Authorization': f'Bearer {create_test_super_user_access_token["access_token"]}'})
#   assert client_cluster.status_code == 200
#   cluster_db = client_cluster.json()
#   assert cluster_db['name'] == client_clusters_data[0]['name']




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
