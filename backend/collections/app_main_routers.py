from typing import List
from fastapi import APIRouter, Depends



from .music_routers.main_group_router import router as main_group_router
from .music_routers.track_group_router import router as track_group_router
from .music_routers.track_routers import router as tracks_routers


router = APIRouter(
  prefix='/music',
  # tags=['Music']
)




router.include_router(main_group_router, tags=['Main groups'])
router.include_router(track_group_router, tags=['Track Group'])
router.include_router(tracks_routers)