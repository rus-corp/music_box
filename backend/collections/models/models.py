from typing import List, TYPE_CHECKING
from sqlalchemy import Table, Column, Integer, DateTime, String, ForeignKey, Boolean, func
from sqlalchemy.orm import Mapped, relationship




from backend.database import Base
from backend.clients.models import Client
from .association_models import track_collection_tracks_association, group_track_collection_association





class Track(Base):
  __tablename__ = 'track'
  
  id = Column(Integer, primary_key=True)
  title = Column(String, unique=True, nullable=False)
  artist = Column(String, nullable=False)
  label = Column(String, nullable=False)
  open_name = Column(String, info={'desc': 'Красивое имя для отображения на фронте'})
  file_path = Column(String, nullable=False)
  album = Column(String, nullable=False)
  genre = Column(String, nullable=False)
  created_at = Column(DateTime, default=func.now())
  
  track_collections: Mapped[List['TrackCollection']] = relationship(secondary=track_collection_tracks_association, back_populates='tracks')
  
  
  
class TrackCollection(Base):
  __tablename__ = 'track_collection'
  
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  player_option = Column(Boolean, default=True, info={'desc': 'true - играет по порядку'})
  
  tracks: Mapped[List['Track']] = relationship(secondary=track_collection_tracks_association, back_populates='track_collections')
  group_collections: Mapped[List['CollectionGroup']] = relationship(secondary=group_track_collection_association, back_populates='track_collections')
  
  clients: Mapped[List['Client']] = relationship(secondary='trackCollections_client_association', back_populates='track_collections')
   
   
   
class CollectionGroup(Base):
  __tablename__ = 'group_collection'
  id = Column(Integer, primary_key=True, autoincrement=True)
  group_name = Column(String, nullable=False)
  
  track_collections: Mapped[List['TrackCollection']] = relationship(secondary=group_track_collection_association, back_populates='group_collections')
