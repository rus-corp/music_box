from sqlalchemy import Column, ForeignKey, Integer, Table



from backend.database import Base





group_track_collection_association = Table(
  'group_track_collection_association',
  Base.metadata,
  Column('id', Integer, primary_key=True),
  Column('group_collection_id', ForeignKey('group_collection.id')),
  Column('track_collection_id', ForeignKey('track_collection.id'))
)


track_collection_tracks_association = Table(
  'track_collection_tracks_association',
  Base.metadata,
  Column('id', Integer, primary_key=True),
  Column('track_id', ForeignKey('track.id')),
  Column('track_collection_id', ForeignKey('track_collection.id'))
)


trackCollection_baseCollection_association = Table(
  'trackCollection_baseCollection_association',
  Base.metadata,
  Column('id', Integer, primary_key=True, autoincrement=True),
  Column('trac_collection_id', Integer, ForeignKey('track_collection.id')),
  Column('base_collection_id', Integer, ForeignKey('base_collection.id'))
)

trackBaseCollectionAssociation = Table(
  'trackBaseCollectionAssociation',
  Base.metadata,
  Column('id', Integer, primary_key=True),
  Column('track_id', Integer, ForeignKey('track.id')),
  Column('base_collection_id', Integer, ForeignKey('base_collection.id'))
)