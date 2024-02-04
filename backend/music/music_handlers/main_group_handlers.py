from sqlalchemy.ext.asyncio import AsyncSession



from backend.music.dals.main_group_dal import CollectionGroupDAL



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