from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse


from ..dals.tracks_dal import TrackDAL


async def _create_track(session: AsyncSession, body):
  track_dal = TrackDAL(session)
  create_track = await track_dal.create_track(**body)