from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession



from backend.clients.dals.clients_dals import ClientDAL


class MusicMixin:
  
  def check_body(self, body: dict) -> bool:
    return len(body) < 2