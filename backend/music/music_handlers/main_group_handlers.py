from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse


from backend.music.dals.main_group_dal import CollectionGroupDAL
from backend.music.dals.track_group_dal import TrackCollectionDAL
from backend.music import schemas


async def _create_collection_group(session: AsyncSession, name):
  async with session.begin():
    colection_dal = CollectionGroupDAL(session)
    collection = await colection_dal.create_collection_group(name.group_name)
    return collection
  
  
async def _get_collcetions_group_all_with_track_collections(session: AsyncSession):
  async with session.begin():
    collections_dal = CollectionGroupDAL(session)
    collections = await collections_dal.get_all_collection_group_with_track_collections()
    return list(collections)
  

async def _get_group_collections_without_track_collections(session: AsyncSession):
  async with session.begin():
    collections_dal = CollectionGroupDAL(session)
    collections = await collections_dal.get_group_collections_without_track_collections()
    return collections

  
async def _get_collection_by_id(session: AsyncSession, collection_id: int):
  async with session.begin():
    collections_dal = CollectionGroupDAL(session)
    collection = await collections_dal.get_collection_group_by_id(collection_id)
    return collection
  
  
async def _get_group_coll_by_id_with_track_collections(session: AsyncSession, collection_id):
  async with session.begin():
    collections_dal = CollectionGroupDAL(session)
    collection = await collections_dal.get_group_collection_with_track_collections(collection_id=collection_id)
    return collection
  
  
async def _update_collection_group(session: AsyncSession, collection_group_id: int, name: str):
  async with session.begin():
    collections_dal = CollectionGroupDAL(session)
    collection_group = await collections_dal.get_collection_group_by_id(collection_group_id)
    if collection_group is None:
      return None
    update_collection = await collections_dal.update_collection_group(collection_group_id, name)
    return update_collection
    

async def _delete_collection_group(session: AsyncSession, collection_id: int):
  async with session.begin():
    collections_dal = CollectionGroupDAL(session)
    collection_group = await collections_dal.get_collection_group_by_id(collection_id)
    if collection_group is None:
      return None
    delete_collection = await collections_dal.delete_collection_group(collection_id)
    return delete_collection
  
  
async def _change_main_group_in_track_group(session: AsyncSession,
                                            new_main_group: int,
                                            old_main_group: int,
                                            track_collection_group: int):
  async with session.begin():
    collection_dal = CollectionGroupDAL(session)
    new_group = await collection_dal.get_collection_group_for_track_collection(new_main_group)
    if new_group is None:
      return JSONResponse(
        content=f'New main group with id = {new_main_group} not found, you need to create her',
        status_code=404
      )
    delete_relationship = await collection_dal.delete_track_group_in_main_group(
      old_main_grop_id=old_main_group,
      track_collection_group_id=track_collection_group
    )
    if delete_relationship != old_main_group:
      return JSONResponse(
        content=f'Связь между {old_main_group} и {track_collection_group} отсутсвует',
        status_code=403
      )
    
    track_collection_dal = TrackCollectionDAL(session)
    track_collection = await track_collection_dal.get_track_collection_by_id(
      track_collection_id=track_collection_group
    )
    
    if track_collection is None:
      return JSONResponse(
        content=f'New track_collection group with id = {track_collection_group} not found',
        status_code=404
      )
    
    new_group.track_collections.append(track_collection)
    await session.commit()
    
    track_collection_show = schemas.TrackCollectionShow(
      id=track_collection.id,
      name=track_collection.name,
      player_option=track_collection.player_option
    )
    
    return schemas.GroupCollectionWithTrackCollectionCreate(
      id=new_group.id,
      group_name=new_group.group_name,
      track_collections=track_collection_show
    )
    
    