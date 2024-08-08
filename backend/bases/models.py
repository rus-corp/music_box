from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey




from backend.database import Base
if TYPE_CHECKING:
  from backend.collections.models.models import TrackCollection, Track



class MainBase(Base):
  __tablename__ = 'bases'
  
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str]
  base_collections: Mapped[List['BaseCollection']] = relationship(back_populates='base')


class BaseCollection(Base):
  __tablename__ = 'base_collection'
  
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str]
  
  main_base_id: Mapped[int] = mapped_column(ForeignKey('bases.id'))
  base: Mapped['MainBase'] = relationship(back_populates='base_collections')
  
  tracks: Mapped[List['Track']] = relationship(
    secondary='trackBaseCollectionAssociation',
    back_populates='base_collections'
  )
  
  track_collections: Mapped[List['TrackCollection']] = relationship(
    secondary='trackCollection_baseCollection_association',
    back_populates='base_collections'
  )