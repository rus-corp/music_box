from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse


from backend.collections.dals.main_group_dal import CollectionGroupDAL
from backend.collections.dals.track_group_dal import TrackCollectionDAL
from backend.collections import schemas
from backend.auth import errors
from backend.auth.permissions import Permissions

from backend.users.models import User


class MainGroupHandler:
  def __init__(self, session: AsyncSession, current_user: User = None) -> None:
    self.session = session
    self.current_user = current_user
    self.colection_dal = CollectionGroupDAL(self.session)
    self.role = 'redactor'
    self.permission = Permissions(self.current_user)
  
  
  async def _check_group_collection_in_db(self, group_id: int):
    collection_group = await self.colection_dal.get_group_collection_by_id_without_track_collections(group_id)
    if collection_group is None:
      return False
    return True
  
  
  async def _create_collection_group(self, name):
    if self.permission.redactor_permission():
      collection = await self.colection_dal.create_collection_group(name)
      return collection
    else:
      return errors.access_denied_error
  
  
  async def _get_all_collection_groups(self, flag: bool = False):
    async with self.session.begin():
      if self.permission.redactor_permission():
        if flag:
          collection_group = await self.colection_dal.get_all_group_collections_with_track_collections()
        else:
          collection_group = await self.colection_dal.get_all_group_collections_without_track_collections()
        return list(collection_group)
      else:
        return errors.access_denied_error
        
  
  
  async def _get_group_collelctions_by_id(self, group_id: int, flag:bool=False):
    async with self.session.begin():
      if self.permission.redactor_permission():
        if flag:
          colection_group = await self.colection_dal.get_group_collection_by_id_with_track_collections(group_id)
        else:
          colection_group = await self.colection_dal.get_group_collection_by_id_without_track_collections(group_id)
        if colection_group is None:
          return errors.not_Found_error
        return colection_group
      else:
        return errors.access_denied_error
      
  
  
  async def _update_group_collection(self, body: schemas.UpdateCollectiongroupRequest):
    if self.permission.redactor_permission():
      body_data = body.model_dump()
      has_group = await self._check_group_collection_in_db(body_data['id'])
      if has_group:
        updated_collection = await self.colection_dal.update_collection_group(
          collection_group_id=body_data['id'], name=body_data['name']
        )
        return updated_collection
      else:
        return errors.not_Found_error
    else:
      return errors.access_denied_error
  
  
  async def _delete_group_collection_by_id(self, group_id: int):
    if self.permission.redactor_permission():
        deleted_group = await self.colection_dal.delete_collection_group(group_id)
        if isinstance(deleted_group, str):
          return JSONResponse(
            content=deleted_group, status_code=400
          )
        if deleted_group is None:
          return errors.found_error_in_db(
            data='Collection Group', id=group_id
          )
        return deleted_group
    else:
      return errors.access_denied_error
  
  
  
  # async def _change_main_group_in_track_group(self,
  #                                             new_main_group: int,
  #                                             old_main_group: int,
  #                                             track_collection_group: int):
  #   async with self.session.begin():
  #     new_group = await self.colection_dal.get_collection_group_for_track_collection(new_main_group)
  #     if new_group is None:
  #       return JSONResponse(
  #         content=f'New main group with id = {new_main_group} not found, you need to create her',
  #         status_code=404
  #       )
  #     delete_relationship = await self.colection_dal.delete_track_group_in_main_group(
  #       old_main_grop_id=old_main_group,
  #       track_collection_group_id=track_collection_group
  #     )
  #     if delete_relationship != old_main_group:
  #       return JSONResponse(
  #         content=f'Связь между {old_main_group} и {track_collection_group} отсутсвует',
  #         status_code=403
  #       )
      
  #     track_collection_dal = TrackCollectionDAL(self.session)
  #     track_collection = await track_collection_dal.get_track_collection_by_id(
  #       track_collection_id=track_collection_group
  #     )
      
  #     if track_collection is None:
  #       return JSONResponse(
  #         content=f'New track_collection group with id = {track_collection_group} not found',
  #         status_code=404
  #       )
      
  #     new_group.track_collections.append(track_collection)
  #     await self.session.commit()
      
  #     track_collection_show = schemas.TrackCollectionShow(
  #       id=track_collection.id,
  #       name=track_collection.name,
  #       player_option=track_collection.player_option
  #     )
      
  #     return schemas.GroupCollectionWithTrackCollectionCreate(
  #       id=new_group.id,
  #       group_name=new_group.group_name,
  #       track_collections=track_collection_show
  #     )