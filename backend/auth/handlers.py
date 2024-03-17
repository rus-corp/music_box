from sqlalchemy.ext.asyncio import AsyncSession



from backend.users.handlers import _get_user_by_email
from .service import Hasher  


async def _authenticate_user(session: AsyncSession, email: str, password: str):
  user = await _get_user_by_email(
    session=session, email=email
  )
  if user is None:
    return False
  if not Hasher.verify_password(password, user.hashed_password):
    return False
  return user