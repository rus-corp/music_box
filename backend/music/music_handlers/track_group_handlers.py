from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from backend.music.dals.track_group_dal import TrackCollectionDAL
from backend.music.dals.main_group_dal import CollectionGroupDAL


from backend.music.schemas import TrackCollectionCreate, TrackCollectionShow, GroupCollectionWithTrackCollectionCreate, TrackCollectionUpdateResponse



async def _create_track_collection(session: AsyncSession, track_collection_dal: TrackCollectionDAL, body):
  track_collection_created = await track_collection_dal.create_track_collection(name=body['track_collection_name'], player_option=body['player_option'])
  return track_collection_created


async def _create_track_and_group_collections(session: AsyncSession, body: TrackCollectionCreate):
  async with session.begin():
    track_collection_dal = TrackCollectionDAL(session)
    group_collection_dal = CollectionGroupDAL(session)
    model_data = body.model_dump(exclude_none=True)
    group_coollection_id = model_data.pop('group_coollection_id')
    has_group_collection = await group_collection_dal.get_collection_group_by_id(group_coollection_id)
    if has_group_collection is None:
      return JSONResponse(content=f'Collection with id = {group_coollection_id} not found', status_code=404)
    group_collection = await group_collection_dal.get_collection_group_for_track_collection(group_coollection_id)
    
    track_collection = await _create_track_collection(session=session, track_collection_dal=track_collection_dal, body=model_data)
    
    group_collection.track_collections.append(track_collection)
    await session.commit()
    
  track_collection_show = TrackCollectionShow(
    id=track_collection.id,
    name=track_collection.name,
    player_option=track_collection.player_option
  )
  return GroupCollectionWithTrackCollectionCreate(
    id=group_collection.id,
    group_name=group_collection.group_name,
    track_collections=track_collection_show
  )

  
async def _get_track_collections(session: AsyncSession):
  track_collection_dal = TrackCollectionDAL(session)
  track_collections = await track_collection_dal.get_all_track_collections()
  return list(track_collections)
  
  
async def _get_track_collection_by_id(session: AsyncSession, track_collection_id: int):
  async with session.begin():
    track_collection_dal = TrackCollectionDAL(session)
    track_collection_by_id = await track_collection_dal.get_track_collection_by_id(track_collection_id=track_collection_id)
    return track_collection_by_id
  

async def _update_track_collection(session: AsyncSession, track_collection_id, body: TrackCollectionUpdateResponse):
  async with session.begin():
    track_collection_dal = TrackCollectionDAL(session)
    track_collection_group = track_collection_dal.get_track_collection_by_id(track_collection_id)
    if track_collection_group is None:
      return None
    body_data = body.model_dump(exclude_none=True)
    updated_track_collection = await track_collection_dal.update_track_collection(track_collection_id, **body_data)
    return updated_track_collection

  
async def _delete_track_collection(session: AsyncSession, track_collection_id: int):
  async with session.begin():
    track_collection_dal = TrackCollectionDAL(session)
    track_collection_group = await track_collection_dal.get_track_collection_by_id(track_collection_id)
    if track_collection_group is None:
      return None
    has_client = await track_collection_dal.collection_has_client(track_collection_id=track_collection_id)
    if has_client:
      return JSONResponse(content=f'Track collection {track_collection_id} has a client', status_code=403)
    deleted_track_collection = await track_collection_dal.delete_track_collection(track_collection_id)
    return deleted_track_collection
  

async def _delete_client_in_trackcollection(session: AsyncSession, track_collection_id: int, client_id: int):
  async with session.begin():
    track_collection_dal = TrackCollectionDAL(session)
    deleted_client_in_track_collection = await track_collection_dal.delete_client_in_group_collection(
      track_collection_id=track_collection_id, client_id=client_id
    )
    return JSONResponse(content=f'Deleted {deleted_client_in_track_collection} rows', status_code=204)
