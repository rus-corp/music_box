from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse


from ..dals.mainbase_dal import MainBaseDAL
from backend.auth.permissions import Permissions
from backend.auth import errors

class MainBaseHandler:
  def __init__(self, session: AsyncSession, current_user=None) -> None:
    self.session = session
    self.main_base_dal = MainBaseDAL(self.session)
    self.permission = Permissions(current_user)
  
  
  async def _create_main_base(self, name: str):
    if self.permission.redactor_permission():
      async with self.session.begin():
        new_base = await self.main_base_dal.create_main_base(
          name=name
        )
        return new_base
    else:
      return errors.access_denied_error
  
  
  async def _get_all_bases(self, flag: bool):
    if self.permission.redactor_permission():
      async with self.session.begin():
        if flag:
          bases = await self.main_base_dal.get_all_main_base_with_collection()
        else:
          bases = await self.main_base_dal.get_all_main_base()
      return list(bases)
    else:
      return errors.access_denied_error
  
  
  # async def _get_all_bases_with_base_collections(self):
  #   if self.permission.redactor_permission():
  #     async with self.session.begin():
  #       bases = await self.main_base_dal.get_all_main_base_with_collection()
  #       return list(bases)
  #   else:
  #     return errors.access_denied_error
  
  
  async def _get_base_by_id(self, base_id: int, flag: bool):
    if self.permission.redactor_permission():
      async with self.session.begin():
        if flag:
          base = await self.main_base_dal.get_main_base_by_id_with_collection(base_id)
        else:
          base = await self.main_base_dal.get_main_base_by_id_without_collection(
          base_id=base_id
        )
      return base
    else:
      return errors.access_denied_error
  
  
  # async def _get_base_by_id_with_collection(self, base_id: int):
  #   if self.permission.redactor_permission():
  #     async with self.session.begin():
  #       base = await self.main_base_dal.get_main_base_by_id_with_collection(base_id)
  #       return base
  #   else:
  #     return errors.access_denied_error
  
  
  async def _update_base_by_id(self, base_id: int, new_name: str):
    if self.permission.redactor_permission():
      async with self.session.begin():
        updated_base = await self.main_base_dal.update_main_base(
          base_id=base_id, new_name=new_name
        )
        return updated_base
    else:
      return errors.access_denied_error
  
  
  async def _delete_base_dy_id(self, base_id: int):
    if self.permission.redactor_permission():
      async with self.session.begin():
        deleted_base = await self.main_base_dal.delete_main_base(base_id)
        if isinstance(deleted_base, str):
          return JSONResponse(
            content=deleted_base, status_code=400
          )
        if deleted_base is None:
          return errors.found_error_in_db(
            data='Bases', id=base_id
          )
        return deleted_base
    else:
      return errors.access_denied_error