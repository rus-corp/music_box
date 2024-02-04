from sqlalchemy import Column, String, Integer, ForeignKey
from typing import List
from sqlalchemy.orm import relationship, Mapped, mapped_column



from backend.database import Base



class UserRole(Base):
  __tablename__ = 'user_role'
  id: Mapped[int] = mapped_column(primary_key=True)
  role_name: Mapped[str] = mapped_column(nullable=False, unique=True)
  
  user: Mapped[List['User']] = relationship(back_populates='role')
  


class User(Base):
  __tablename__ = 'user'
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(nullable=False)
  comment: Mapped[str] = mapped_column(nullable=True)
  login: Mapped[str] = mapped_column(nullable=False)
  password: Mapped[str] = mapped_column(nullable=False)
  is_active: Mapped[bool] = mapped_column(default=True)
  is_superuser: Mapped[bool] = mapped_column(default=False)
  
  role_id: Mapped[int] = mapped_column(ForeignKey('user_role.id'))
  role: Mapped[UserRole] = relationship(back_populates='user')
  client = relationship('Client', back_populates='user')
  