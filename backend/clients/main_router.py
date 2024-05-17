from fastapi import APIRouter


from .routers import client_cluster_rout, client_group_rout, currency_rout
from .routers.clients_rout import router


# router = APIRouter(
#   prefix='/clients',
#   tags=['Clients']
# )

router.include_router(currency_rout.router)
router.include_router(client_group_rout.router)
