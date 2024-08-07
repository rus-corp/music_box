from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse


from ..models import TrackCollection

from ..dals.tracks_dal import TrackDAL
from backend.users.models import User
from backend.auth.permissions import Permissions
from backend.auth import errors
from ..service import FileProcessing
from ..schemas import TrackCollectionWithTracks
from ..dals.track_group_dal import TrackCollectionDAL


class TrackHandler:
  def __init__(self, session: AsyncSession, current_user: User, files=None) -> None:
    self.session = session
    self.track_dal = TrackDAL(self.session)
    self.permission = Permissions(current_user)
    self.files = files
  
  
  async def _create_track(self):
    tracks = {'error_tracks': [], 'created_tracks': []}
    if self.permission.redactor_permission():
      async with self.session.begin():
        for track in self.files:
          track_service = FileProcessing(track)
          track_db = await track_service.file_proc()
          if 'exceptions_errors' in track_db:
            tracks['error_tracks'].append(
              track_db['exceptions_errors']
            )
          else:
            create_track = await self.track_dal.create_track(**track_db)
            tracks['created_tracks'].append(
              create_track.open_name
            )
        await self.session.commit()
        return tracks
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


  async def _append_track_to_collection(self, track_collection_id: int, track_id: int):
    if self.permission.redactor_permission():
      async with self.session.begin():
        track = await self.track_dal.get_track_for_append_to_group(track_id)
        if track is None:
          await self.session.rollback()
          return errors.found_error_in_db('Track', track_id)
        track_group_dal = TrackCollectionDAL(self.session)
        track_group: TrackCollection = await track_group_dal.get_track_group_by_id_with_tracks(track_collection_id)
        if track_group is None:
          await self.session.rollback()
          return errors.found_error_in_db('Track Group', track_collection_id)
        track_group.tracks.append(track)
        await self.session.commit()
        return TrackCollectionWithTracks(
          id=track_group.id,
          name=track_group.name,
          player_option=track_group.player_option,
          tracks=[track]
        )
    else:
      return errors.access_denied_error
  
  async def _delete_track_from_collection(self, track_id: int, track_collection_id: int):
    if self.permission.redactor_permission():
      async with self.session.begin():
        track = await self.track_dal.get_track_for_append_to_group(track_id)
        if track is None:
          await self.session.rollback()
          return errors.found_error_in_db('Track', track_id)
        track_group_dal = TrackCollectionDAL(self.session)
        track_group: TrackCollection = await track_group_dal.get_track_group_by_id_with_tracks(track_collection_id)
        if track_group is None:
          await self.session.rollback()
          return errors.found_error_in_db('Track Group', track_collection_id)
        try:
          track_group.tracks.remove(track)
          await self.session.commit()
        except ValueError:
          await self.session.rollback()
          return JSONResponse(content=f'Track with id {track_id} not in Track Collection with id {track_collection_id}',
                              status_code=404)
        return JSONResponse(content=f'Track with id {track_id} deleted from Collection with id {track_collection_id}',
                            status_code=200)
    else:
      return errors.access_denied_error