from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from .models import User, UserRole
from .schemas import CreateUser, ShowUser, UserRoleShow



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
    
    
  async def create_user(self, name: str, login: str, email: str,
                        password: str, comment: str = None, role: UserRole = None) -> ShowUser:
    new_user = User(
      name=name,
      login=login,
      email=email,
      hashed_password=password,
      comment=comment,
      role=role
    )
    self.db_session.add(new_user)
    try:
      await self.db_session.flush()
      user_role = UserRoleShow(
        id=new_user.role.id,
        role_name=new_user.role.role_name
      )
      show_user = ShowUser(
        id=new_user.id,
        name=new_user.name,
        login=new_user.login,
        email=new_user.email,
        is_active=new_user.is_active,
        comment=new_user.comment,
        role=user_role
      )
      return show_user, None
    
    except IntegrityError as e:
      return None, str(e)
      
    
    
    
  async def get_users(self) -> list[ShowUser]:
    query = select(User, UserRole).join(User.role).order_by(User.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()
  
  
  async def get_user_by_id_with_role(self, user_id: int) -> ShowUser:
    query = select(User).where(User.id == user_id).options(selectinload(User.role))
    result = await self.db_session.execute(query)
    user_row = result.scalar()
    return user_row
  
  
  async def get_user_by_email(self, user_email):
    query = select(User).where(User.email == user_email).options(selectinload(User.role))
    result = await self.db_session.execute(query)
    user_row = result.fetchone()
    if user_row is not None:
      return user_row[0]
  
  
  async def update_user_by_id(self, user_id: int, **kwargs):
    query = update(User).where(User.id == user_id).values(kwargs).returning(User)
    result = await self.db_session.execute(query)
    updated_user = result.fetchone()
    if updated_user is not None:
      return updated_user[0]
    
    
  async def update_user_role(self): pass
  
  
  async def delete_user_by_id(self):
    pass
  
  
  
