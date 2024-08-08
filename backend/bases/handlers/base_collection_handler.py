from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse



from backend.users.models import User
from backend.auth.permissions import Permissions
from backend.auth import errors

from ..schemas import BaseCollectionUpdateRequest, BaseCollectionCreateRequest
from ..dals.base_collection_dal import BaseCollectionDAL
from ..dals.mainbase_dal import MainBaseDAL



class BaseCollectionHandler:
  def __init__(self, session: AsyncSession, current_user: User) -> None:
    self.session = session
    self.collection_dal = BaseCollectionDAL(self.session)
    self.permission = Permissions(current_user)
  
  
  async def _create_base_collection(self, body: BaseCollectionCreateRequest):
    if self.permission.redactor_permission():
      async with self.session.begin():
        body_data = body.model_dump(exclude_none=True)
        base_dal = MainBaseDAL(self.session)
        base = await base_dal.get_main_base_by_id_without_collection(
          base_id=body_data['base_id']
        )
        if base is None:
          return errors.found_error_in_db(
            data='Main Base',
            id=body_data['base_id']
          )
        base_collection = await self.collection_dal.create_base_collection(
          name=body_data['name'], base_id=body_data['base_id']
        )
        return base_collection
    else:
      return errors.access_denied_error
  
  
  async def _get_all_base_collections(self):
    if self.permission.redactor_permission():
      async with self.session.begin():
        collection_lst = await self.collection_dal.get_all_base_collections()
        return list(collection_lst)
    else:
      return errors.access_denied_error
  
  
  async def _get_base_collection_by_id(self, collection_id: int):
    if self.permission.redactor_permission():
      async with self.session.begin():
        base_collection = await self.collection_dal.get_collection_by_id(
          collection_id
        )
        return base_collection
    else:
      return errors.access_denied_error
  
  
  async def _get_base_collection_by_id_with_tracks(self, collection_id: int):
    if self.permission.redactor_permission():
      async with self.session.begin():
        base_collection = await self.collection_dal.get_collection_by_id_with_tracks(
          collection_id=collection_id
        )
        return base_collection
    else:
      return errors.access_denied_error
  
  
  async def _update_base_collection(self, collection_id: int, body: BaseCollectionUpdateRequest):
    if self.permission.redactor_permission():
      async with self.session.begin():
        body_data = body.model_dump(exclude_none=True)
        updated_collection = await self.collection_dal.update_collection_by_id(collection_id, **body_data)
        return updated_collection
    else:
      return errors.access_denied_error
  
  
  async def _delete_base_collection(self, collection_id: int):
    if self.permission.redactor_permission():
      async with self.session.begin():
        deleted_collection = await self.collection_dal.delete_collection_by_id(
          collection_id
        )
        return deleted_collection
    else:
      return errors.access_denied_error