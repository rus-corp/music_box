from sqlalchemy.ext.asyncio import AsyncSession



from backend.users.handlers import UserHandler
from .service import Hasher  


async def _authenticate_user(session: AsyncSession, email: str, password: str):
  user_habdler = UserHandler(session)
  user = await user_habdler._get_user_by_email(email=email)
  if user is None:
    return False
  if not Hasher.verify_password(password, user.hashed_password):
    return False
  return user





