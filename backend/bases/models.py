from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey




from backend.database import Base




class MainBase(Base):
  __tablename__ = 'bases'
  
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str]
  collection: Mapped['BaseCollection'] = relationship(back_populates='bases')


class BaseCollection(Base):
  __tablename__ = 'base_collection'
  
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str]
  
  main_base_id: Mapped[int] = mapped_column(ForeignKey('bases.id'))
  bases: Mapped['MainBase'] = relationship(back_populates='collection')


