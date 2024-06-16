from httpx import AsyncClient
import json
from fastapi.exceptions import HTTPException
import pytest


"""/music/main_group/:
1. group_collections   - post
2. group_track_collections   - get
3. group_no_track_collections   -get
4. group_collection/{collection_id}   -get
5. group_collection_with_track/{collection_id}   - get
6. group_collection/{collection_id}   - patch
7. group_collection/{collection_id}   - del


/music/track_group/:
1. track_group_collection   - post
2. track_collections   - get
3. track_collections/{track_collection_id}   - get
4. track_collections/{track_collection_id}   - patch
5. track_collections/{track_collection_id}   -del
"""





main_group_data = [
  {'group_name': 'first group'},
  {'group_name': 'second group'},
  {'group_name': 'therd group'},
  {'group_name': 'fourth group'},
  {'group_name': 'fith group'},
  {'group_name': ''}
]

track_group_data = [
  {'track_collection_name': 'first', 'player_option': True, 'group_coollection_id': 1},
  {'track_collection_name': 'second', 'player_option': False, 'group_coollection_id': 1},
  {'track_collection_name': 'therd', 'player_option': True, 'group_coollection_id': 2},
  {'track_collection_name': 'fourth', 'player_option': False, 'group_coollection_id': 2},
  {'track_collection_name': 'sixten', 'group_coollection_id': 3},
  {'track_collection_name': 'fifth', 'player_option': False, 'group_coollection_id': 23},
  {'player_option': True, 'group_coollection_id': 1},
]


# async def test_create_collection(ac: AsyncClient):
#   initial_response = await ac.get('/music/main_group/group_no_track_collections')
#   db_len_before = len(initial_response.json())
#   assert db_len_before == 0
#   for data in main_group_data[:-1]:
#     response = await ac.post('/music/main_group/group_collections', json=data)
#     assert response.status_code == 200
#   bad_response = await ac.post('/music/main_group/group_collections', json=main_group_data[-1])
#   assert bad_response.status_code == 400
#   after_response = await ac.get('/music/main_group/group_no_track_collections')
#   db_record = after_response.json()
#   assert len(db_record) == len(main_group_data) - 1
#   assert db_record[0]['group_name'] == main_group_data[0]['group_name']
  


# async def test_create_track_collcetions(ac: AsyncClient):
#   for item in track_group_data[:-2]:
#     response1 = await ac.post('/music/track_group/track_group_collections', json=item)
#     assert response1.status_code == 200
  
#   response2 = await ac.post('/music/track_group/track_group_collections', json=track_group_data[-2])
#   assert response2.status_code == 404
  
#   response3 = await ac.post('/music/track_group/track_group_collections', json=track_group_data[-1])
#   assert response3.status_code == 422
  
#   response4 = await ac.get('/music/track_group/track_group_collections')
#   total_data = response4.json()
#   assert len(total_data) == len(track_group_data) - 2
#   for i, record in enumerate(total_data):
#     rec_id = record['id']
#     assert record['name'] == track_group_data[rec_id - 1]['track_collection_name']
    
  
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
  
  
