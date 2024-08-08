from fastapi import APIRouter


from .routers.main_base_router import router as main_base_router




router = APIRouter(
  prefix='/bases',
  tags=['Bases']
)

router.include_router(main_base_router)