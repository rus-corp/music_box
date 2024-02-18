from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse


from ..dals.tracks_dal import TrackDAL


async def _create_track(session: AsyncSession, body):
  async with session.begin():
    track_dal = TrackDAL(session)
    create_track = await track_dal.create_track(**body)
    return create_track


async def _get_tracks(offset: int, limit: int, session: AsyncSession):
  async with session.begin():
    track_dal = TrackDAL(session)
    tracks = await track_dal.get_tracks(limit=limit, offset=offset)
    return list(tracks)
  

async def _get_track_by_id(session: AsyncSession, track_id: int):
  async with session.begin():
    track_dal = TrackDAL(session)
    track = await track_dal.get_track_by_id(track_id)
    return track
  
  
async def _update_track(session: AsyncSession, track_id: int, body):
  async with session.begin():
    track_dal = TrackDAL(session)
    track = await track_dal.get_track_by_id(track_id)
    if track is None:
      return JSONResponse(content=f'Track with id {track_id} not found', status_code=404)
    updated_track = await track_dal.update_track(track_id, body)
    return updated_track
  

async def _delete_track_by_id(session: AsyncSession, track_id: int):
  async with session.begin():
    track_dal = TrackDAL(session)
    track = await track_dal.get_track_by_id(track_id)
    if track is None:
      return JSONResponse(content=f'Track with id {track_id} not found', status_code=404)
    deleted_track = await track_dal.delete_track_by_id(track_id)
    return deleted_track
  
  
 