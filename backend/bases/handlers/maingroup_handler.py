from sqlalchemy.ext.asyncio import AsyncSession



from ..dals.mainbase_dal import MainBaseDAL
from backend.auth.permissions import Permissions


class MainGroupHandler:
  def __init__(self, session: AsyncSession, current_user=None) -> None:
    self.session = session
    self.main_base_dal = MainBaseDAL(self.session)
    self.permission = Permissions(current_user)