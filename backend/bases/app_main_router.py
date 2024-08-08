from fastapi import APIRouter


from .routers.main_base_router import router as main_base_router
from .routers.base_collection_touter import router as main_collection_router




router = APIRouter(
  prefix='/bases',
  tags=['Bases']
)

router.include_router(main_base_router)
router.include_router(main_collection_router)