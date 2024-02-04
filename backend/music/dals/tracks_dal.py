from sqlalchemy.ext.asyncio import AsyncSession


from ..models import Track
from ..schemas import TrackCreate, TrackShow

class TrackDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session
    
  async def create_track(self, title: str,
                         artist: str, label: str,
                         open_name: str, file_path: str):
    new_track = Track(
      title=title,
      artist=artist,
      label=label,
      open_name=open_name,
      file_path=file_path
    )
    
    self.db_session.add(new_track)
    await self.db_session.commit()
    return new_track
  
  
  async def get_tracks(self, limit: int): pass
  
  async def get_track_by_id(self, track_id: int): pass
  
  async def update_track(self, **kwargs): pass
  
  async def delete_track_by_id(self, track_id): pass
  