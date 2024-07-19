from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse


from ..dals.tracks_dal import TrackDAL
from backend.users.models import User
from backend.auth.permissions import Permissions
from backend.auth import errors


class TrackHandler:
  def __init__(self, session: AsyncSession, current_user: User) -> None:
    self.session = session
    self.track_dal = TrackDAL(self.session)
    self.permission = Permissions(current_user)
  
  
  async def _create_track(self, body):
    if self.permission.redactor_permission():
      async with self.session.begin():
        create_track = await self.track_dal.create_track(**body)
        return create_track
    else:
      return errors.access_denied_error
  
  
  async def _get_tracks(self, offset: int, limit: int):
    async with self.session.begin():
      tracks = await self.track_dal.get_tracks(limit=limit, offset=offset)
      return list(tracks)
  
  
  async def _get_track_by_id(self, track_id: int):
    async with self.session.begin():
      track = await self.track_dal.get_track_by_id(track_id)
      return track
  
  
  async def _update_track(self, track_id: int, body):
    if self.permission.redactor_permission():
      async with self.session.begin():
        track = await self.track_dal.get_track_by_id(track_id)
        if track is None:
          return JSONResponse(content=f'Track with id {track_id} not found', status_code=404)
        updated_track = await self.track_dal.update_track(track_id, body)
        return updated_track
    else:
      return errors.access_denied_error
  
  
  async def _delete_track_by_id(self, track_id: int):
    if self.permission.redactor_permission():
      async with self.session.begin():
        track = await self.track_dal.get_track_by_id(track_id)
        if track is None:
          return JSONResponse(content=f'Track with id {track_id} not found', status_code=404)
        deleted_track = await self.track_dal.delete_track_by_id(track_id)
        return deleted_track
    else:
      return errors.access_denied_error


  # async def _append_track_to_collection(self, track_collection_id: int, track_id: int):
  #   async with self.session.begin():
  #     track_collection = await self.track_collection_dal.get_track_collection_for_append_track_to_group(track_group_id=track_collection_id)
  #     if track_collection is None:
  #       return JSONResponse(content='track_collection not found', status_code=404)
  #     track_dal = TrackDAL(self.session)
  #     track = await track_dal.get_track_by_id(track_id=track_id)
      
  #     track_collection.tracks.append(track)
  #     await self.session.commit()
      
  #     track = TrackShow(
  #       id = track.id,
  #       title = track.title,
  #       artist = track.artist,
  #       label= track.label,
  #       open_name = track.open_name,
  #       file_path = track.file_path,
  #       created_at = track.created_at
  #     )
      
  #     return TrackCollectionWithTracks(
  #       id = track_collection.id,
  #       name = track_collection.name,
  #       player_option = track_collection.player_option,
  #       tracks=track
  #     )
    
    
  # async def _delete_track_from_track_collection(self, track_id: int, track_collection_id: int):
  #   async with self.session.begin():
  #     track_collection = await self.track_collection_dal.get_track_collection_for_append_track_to_group(track_group_id=track_collection_id)
  #     track_dal = TrackDAL(self.session)
  #     track = await track_dal.get_track_by_id(track_id=track_id)
  #     if track_collection is None or track is None:
  #       return JSONResponse(content='track collection or track not found')
      
  #     deleted_track_from_collection = await track_dal.delete_track_from_collection(
  #       track_id=track_id, track_collection_id=track_collection_id
  #     )
  #     return deleted_track_from_collection