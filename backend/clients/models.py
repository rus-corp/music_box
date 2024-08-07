from typing import List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, Column, ForeignKey, UniqueConstraint, Integer, Table, Date

from backend.database import Base




if TYPE_CHECKING:
  from backend.collections.models import TrackCollection
  from backend.users.models import User



user_client_group_association = Table(
  'user_client_group_association',
  Base.metadata,
  Column('id', Integer, primary_key=True, autoincrement=True),
  Column('user_id', ForeignKey('user.id')),
  Column('client_group_id', ForeignKey('client_group.id')),
  
  UniqueConstraint('user_id', 'client_group_id')
)



trackCollections_client_association = Table(
  'trackCollections_client_association',
  Base.metadata,
  Column('id', Integer, primary_key=True, autoincrement=True),
  Column('client_id', ForeignKey('client.id')),
  Column('track_collection_id', ForeignKey('track_collection.id')),
  
  UniqueConstraint('client_id', 'track_collection_id')
)



class Currency(Base):
  __tablename__ = 'currency'
  id = Column(Integer, primary_key=True)
  cur_name = Column(String, nullable=False)
  
  clients: Mapped[List['Client']] = relationship(back_populates='currency')



class ClientCluster(Base):
  __tablename__ = 'client_cluster'
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(unique=True, nullable=False)
  
  client_groups: Mapped['ClientGroup'] = relationship(back_populates='client_cluster')



class ClientGroup(Base):
  __tablename__ = 'client_group'
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str]
  comment: Mapped[str] = mapped_column(nullable=True)
  
  client_cluster_id: Mapped[int] = mapped_column(ForeignKey('client_cluster.id'))
  client_cluster: Mapped['ClientCluster'] = relationship(back_populates='client_groups', lazy='joined')
  
  users: Mapped[List['User']] = relationship(secondary='user_client_group_association', back_populates='client_groups')  

  clients: Mapped[List['Client']] = relationship('Client', back_populates='client_group')



class Client(Base):
  __tablename__ = 'client'
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(nullable=False)
  city: Mapped[str] = mapped_column(nullable=False)
  email:Mapped[str] = mapped_column(nullable=False)
  phone:Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
  price:Mapped[int] = mapped_column(nullable=True)
  
  profile: Mapped['ClientProfile'] = relationship(
    back_populates='client', lazy='joined', cascade='all, delete'
  )
  
  currency_id = mapped_column(ForeignKey('currency.id'))
  currency: Mapped[Currency] = relationship(
    back_populates='clients', lazy='joined'
  )
  
  client_group_id = mapped_column(
    ForeignKey('client_group.id')
  )
  client_group: Mapped['ClientGroup'] = relationship('ClientGroup', back_populates='clients')
  
  another_contract: Mapped[List['AnotherContracts']] = relationship(back_populates='client')
  track_collections: Mapped[List['TrackCollection']] = relationship(
    secondary='trackCollections_client_association', back_populates='clients'
  )




class ClientProfile(Base):
  __tablename__ = 'client_profile'
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  address:Mapped[str] = mapped_column(nullable=False)
  full_name: Mapped[str] = mapped_column(nullable=False, info={'desc': 'Наименование Юр.лица'})
  certificate: Mapped[str] = mapped_column(nullable=False)
  contract_number: Mapped[str] = mapped_column(nullable=True)
  contract_date: Mapped[datetime] = mapped_column(nullable=True)
  
  client_id:Mapped[int] = mapped_column(ForeignKey('client.id', ondelete='CASCADE'))
  client: Mapped[Client] = relationship(back_populates='profile')






class AnotherContracts(Base):
  __tablename__ = 'another_contracts'
  
  id = Column(Integer, primary_key=True)
  contract_number = Column(Date)
  payment_date = Column(Date)
  
  client_id = mapped_column(ForeignKey('client.id'))
  client: Mapped['Client'] = relationship(back_populates='another_contract')
  
  