from httpx import AsyncClient
import json
import pytest



from .test_a_users import (test_bad_token, create_test_super_user_access_token,
                           create_test_user_token, create_test_redactor_token)

from .test_data import main_group_data, track_group_data




async def test_create_collection(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token, create_test_redactor_token):
  for item in main_group_data[:3]:
    super_user_req = await ac.post('/music/main_collection/group_collections',
                                   headers={"Authorization": f"Bearer {create_test_super_user_access_token['access_token']}"},
                                   json=item)
    assert super_user_req.status_code == 201
    collections_data = super_user_req.json()
    collection_id = collections_data['id']
    assert collections_data['group_name'] == main_group_data[collection_id - 1]['group_name']
  for item2 in main_group_data[3: -1]:
    redactor_req = await ac.post('/music/main_collection/group_collections', headers={"Authorization": f"Bearer {create_test_redactor_token['access_token']}"}, json=item2)
    assert redactor_req.status_code == 201
    redactor_collection_data = redactor_req.json()
    redactor_collection_id = redactor_collection_data['id']
    assert redactor_collection_data['group_name'] == main_group_data[redactor_collection_id - 1]['group_name']
  redactor_bad_req = await ac.post('/music/main_collection/group_collections', headers={"Authorization": f"Bearer {create_test_redactor_token['access_token']}"}, json=main_group_data[-1])
  assert redactor_bad_req.status_code == 400
  client_req = await ac.post('/music/main_collection/group_collections', headers={"Authorization": f"Bearer {create_test_user_token['access_token']}"}, json=main_group_data[-2])
  assert client_req.status_code == 403
  
  collection_db_data = await ac.get('/music/main_collection/group_without_track_collections', headers={"Authorization": f"Bearer {create_test_redactor_token['access_token']}"})
  collection_db_data.status_code == 200
  db_data_json = collection_db_data.json()
  data_len = len(db_data_json)
  assert data_len + 1 == len(main_group_data)



async def test_get_all_colelctions_without_track_group(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token, create_test_redactor_token):
  redactor_req = await ac.get('/music/main_collection/group_without_track_collections', headers={"Authorization": f"Bearer {create_test_super_user_access_token['access_token']}"})
  assert redactor_req.status_code == 200
  redactor_data = redactor_req.json()
  assert len(redactor_data) == len(main_group_data) - 1
  super_user_req = await ac.get('/music/main_collection/group_without_track_collections', headers={"Authorization": f"Bearer {create_test_redactor_token['access_token']}"})
  assert super_user_req.status_code == 200
  super_user_data = super_user_req.json()
  assert len(main_group_data) - 1 == len(super_user_data)
  user_req = await ac.get('/music/main_collection/group_without_track_collections', headers={"Authorization": f"Bearer {create_test_user_token['access_token']}"})
  assert user_req.status_code == 403


async def test_get_one_colelction_without_track_group(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token, create_test_redactor_token):
  redactor_req = await ac.get('/music/main_collection/group_collection/2', headers={"Authorization": f"Bearer {create_test_redactor_token['access_token']}"})
  assert redactor_req.status_code == 200
  redactor_data = redactor_req.json()
  assert redactor_data['id'] == 2
  assert redactor_data['group_name'] == main_group_data[1]['group_name']
  super_user_req = await ac.get('/music/main_collection/group_collection/1', headers={"Authorization": f"Bearer {create_test_super_user_access_token['access_token']}"})
  assert super_user_req.status_code == 200
  super_user_data = super_user_req.json()
  assert super_user_data['id'] == 1
  assert super_user_data['group_name'] == main_group_data[0]['group_name']
  user_req = await ac.get('/music/main_collection/group_collection/1', headers={"Authorization": f"Bearer {create_test_user_token['access_token']}"})
  assert user_req.status_code == 403



async def test_update_collection(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token, create_test_redactor_token):
  data1 = {'id': 1, 'name': 'NEW NAME'}
  super_req = await ac.patch('/music/main_collection/group_collections', headers={"Authorization": f"Bearer {create_test_super_user_access_token['access_token']}"}, json=data1)
  assert super_req.status_code == 200
  super_req_db = super_req.json()
  assert super_req_db['group_name'] == data1['name']
  
  super_user_req = await ac.get('/music/main_collection/group_collection/1', headers={"Authorization": f"Bearer {create_test_super_user_access_token['access_token']}"})
  assert super_user_req.status_code == 200
  super_user_req_data = super_user_req.json()
  assert super_user_req_data['group_name'] == data1['name']
  
  data2 = {'id': 2, 'name': 'NEW SECOND NAME'}
  redactor_update_req = await ac.patch('/music/main_collection/group_collections', headers={"Authorization": f"Bearer {create_test_redactor_token['access_token']}"}, json=data2)
  assert redactor_update_req.status_code == 200
  redactor_update_req_db = redactor_update_req.json()
  assert redactor_update_req_db['group_name'] == data2['name']
  
  redactor_update_req = await ac.get('/music/main_collection/group_collection/2', headers={"Authorization": f"Bearer {create_test_redactor_token['access_token']}"})
  assert redactor_update_req.status_code == 200
  redactor_update_req_db = redactor_update_req.json()
  assert redactor_update_req_db['group_name'] == data2['name']
  
  data3 = {'id': 1, 'name': 'NEW THERD NAME'}
  user_req = await ac.patch('/music/main_collection/group_collections', headers={"Authorization": f"Bearer {create_test_user_token['access_token']}"}, json=data3)
  assert user_req.status_code == 403




async def test_create_track_collections(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token, create_test_redactor_token):
  for item in track_group_data[:5]:
    super_user_req = await ac.post('/music/track_collection/',
                                   headers={"Authorization": f"Bearer {create_test_super_user_access_token['access_token']}"},
                                   json=item)
    assert super_user_req.status_code == 201
    super_user_data = super_user_req.json()
    super_user_data_id = super_user_data['track_collection']['id']
    assert track_group_data[super_user_data_id - 1]['track_collection_name'] == super_user_data['track_collection']['name']
    assert track_group_data[super_user_data_id - 1]['group_coollection_id'] == super_user_data['id']
  for item2 in track_group_data[5 : -2]:
    redactor_req = await ac.post('/music/track_collection/',
                                 headers={"Authorization": f"Bearer {create_test_redactor_token['access_token']}"},
                                 json=item2)
    assert redactor_req.status_code == 201
    redactor_req_data = redactor_req.json()
    redactor_req_data_id = redactor_req_data['track_collection']['id']
    assert track_group_data[redactor_req_data_id - 1]['track_collection_name'] == redactor_req_data['track_collection']['name']
    assert track_group_data[redactor_req_data_id - 1]['group_coollection_id'] == redactor_req_data['id']
  
  user_bad_req = await ac.post('/music/track_collection/',
                               headers={"Authorization": f"Bearer {create_test_user_token['access_token']}"},
                               json=track_group_data[4])
  assert user_bad_req.status_code == 403
  
  
  redactor_bad_req1 = await ac.post('/music/track_collection/',
                                headers={"Authorization": f"Bearer {create_test_redactor_token['access_token']}"},
                                json=track_group_data[-1])
  assert redactor_bad_req1.status_code == 422
  
  redactor_bad_req2 = await ac.post('/music/track_collection/',
                                headers={"Authorization": f"Bearer {create_test_redactor_token['access_token']}"},
                                json=track_group_data[-2])
  assert redactor_bad_req2.status_code == 404




async def test_get_track_collections(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token, create_test_redactor_token):
  redactor_req = await ac.get('/music/track_collection/',
                              headers={"Authorization": f"Bearer {create_test_redactor_token['access_token']}"})
  assert redactor_req.status_code == 200
  redactor_data = redactor_req.json()
  assert len(redactor_data) == len(track_group_data) - 2



async def test_update_track_collection(ac: AsyncClient, create_test_super_user_access_token, create_test_user_token, create_test_redactor_token):
  new_data = {'name': 'new_name'}
  redactor_req = await ac.patch('/music/track_collection/1',
                              headers={"Authorization": f"Bearer {create_test_redactor_token['access_token']}"}, json=new_data)
  assert redactor_req.status_code == 200
  
  redactor_req_db = await ac.get('/music/track_collection/1',
                                 headers={"Authorization": f"Bearer {create_test_redactor_token['access_token']}"})
  assert redactor_req_db.status_code == 200
  redactor_req_db_data = redactor_req_db.json()
  assert redactor_req_db_data['name'] == new_data['name']


























# async def test_get_group_and_track_collection(ac: AsyncClient):
#   response = await ac.get('music/main_group/group_track_collections')
#   assert response.status_code == 200
#   response_data = response.json()
#   for num, item in enumerate(response_data):
#     if num < 3:
#       assert len(item['track_collections']) >= 1
#       assert item['group_name'] == main_group_data[num]['group_name']
#     else:
#       assert len(item['track_collections']) == 0
    


# async def test_get_group_colection_by_id_with_track_colections(ac: AsyncClient):
#   collection_id = 2
#   response = await ac.get(f'/music/main_group/group_collection_with_track/{collection_id}')
#   assert response.status_code == 200
#   response_data = response.json()
#   assert response_data['group_name'] == 'second group'
#   assert len(response_data['track_collections']) == 2
#   assert response_data['track_collections'][0]['name'] == 'therd'
#   assert response_data['track_collections'][1]['name'] == 'fourth'


# async def test_get_group_collection_by_id_without_track_collections(ac: AsyncClient):
#   collection_id = 4
#   response = await ac.get(f'/music/main_group/group_collection/{collection_id}')
#   assert response.status_code == 200
#   response_data = response.json()
#   assert response_data['group_name'] == 'fourth group'
#   assert 'track_collections' not in response_data  
  
  
# async def test_update_group_collection(ac: AsyncClient):
#   collection_id = 1
#   new_name = 'new group name'
#   response = await ac.patch(f'/music/main_group/group_collection/{collection_id}', params={'name': new_name})
#   assert response.status_code == 200
#   db_rec = response.json()
#   assert len(db_rec) == 2
#   assert db_rec['group_name'] == new_name
  
  
  
  
# async def test_delete_group_collection(ac: AsyncClient):
#   collection_id = 2
#   initial_response = await ac.get(f'/music/main_group/group_collection/{collection_id}')
#   db_len_before = len(initial_response.json())
#   collection_id = 2
#   response = await ac.delete(f'/music/group_collection/{collection_id}')
#   assert response.status_code == 200
#   after_initial = await ac.get('/music/group_collection')
#   db_len_after = len(after_initial.json())
#   assert db_len_after == db_len_before - 1
  
  
