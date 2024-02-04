from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession


from .models import User, UserRole
from .schemas import CreateUser, ShowUser



class UserRoleDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session
    
  async def create_user_role(self, name: str):
    new_role = UserRole(
      role_name=name
    )
    self.db_session.add(new_role)
    await self.db_session.commit()
    return new_role
  
  async def get_user_roles(self):
    query = select(UserRole).order_by(UserRole.id)
    roles = await self.db_session.execute(query)
    return roles.scalars().all()
  
  async def get_user_role_by_id(self, id: int):
    query = select(UserRole).where(UserRole.id == id)
    role = await self.db_session.execute(query)
    role_row = role.fetchone()
    if role_row is not None:
      return role_row[0]
  
  async def update_user_role(self, id: int, new_name: str):
    stmt = update(UserRole).where(UserRole.id == id).values(role_name=new_name).returning(UserRole)
    updated_role = await self.db_session.execute(stmt)
    await self.db_session.commit()
    updated_role_row = updated_role.fetchone()
    if updated_role_row is not None:
      return updated_role_row[0]
  
  async def delete_user_role(self, role_id: int):
    stmt = delete(UserRole).where(UserRole.id == role_id)
    result = await self.db_session.execute(stmt)
    await self.db_session.commit()
    deleted_role_row = result.fetchone()
    if deleted_role_row is not None:
      return deleted_role_row[0]
    



class UserDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session
    
    
  async def create_user(self, name: str, login: str,
                        password: str, comment: str = None, role: UserRole = None) -> ShowUser:
    new_user = User(
      name=name,
      login=login,
      password=password,
      comment=comment,
      role=role
    )
    self.db_session.add(new_user)
    await self.db_session.flush()
    return new_user
    
    
  async def get_users(self) -> list[ShowUser]:
    query = select(User, UserRole).join(User.role).order_by(User.user_id)
    result = await self.db_session.execute(query)
    return result.scalars().all()
  
  
  async def get_user_by_id(self, user_id: int) -> ShowUser:
    query = select(User).where(User.id == user_id).options(selectinload(User.role))
    result = await self.db_session.execute(query)
    user_row = result.scalar()
    return user_row
  
  
  async def update_user_by_id(self):
    pass
  
  
  async def delete_user_by_id(self):
    pass
  
  
  
