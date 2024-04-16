from typing import List, TYPE_CHECKING
import sqlalchemy
from datetime import datetime
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, Column, ForeignKey, UniqueConstraint, Integer, Table

from backend.database import Base




if TYPE_CHECKING:
  from backend.music.models import TrackCollection
  from backend.users.models import User



user_client_group_association = Table(
  'user_client_group_association',
  Base.metadata,
  Column('id', Integer, primary_key=True, autoincrement=True),
  Column('user_id', ForeignKey('user.id')),
  Column('client_group_id', ForeignKey('client_group.id'))
)



trackCollections_client_association = Table(
  'trackCollections_client_association',
  Base.metadata,
  Column('id', Integer, primary_key=True, autoincrement=True),
  Column('client_id', ForeignKey('client.id')),
  Column('track_collection_id', ForeignKey('track_collection.id'))
)



class Currency(Base):
  __tablename__ = 'currency'
  id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
  cur_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
  
  client: Mapped[List['Client']] = relationship(back_populates='currency')



class ClientCluster(Base):
  __tablename__ = 'client_cluster'
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(unique=True, nullable=False)



class ClientGroup(Base):
  __tablename__ = 'client_group'
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str]
  comment: Mapped[str]
  
  users: Mapped[List['User']] = relationship(secondary='user_client_group_association', back_populates='client_groups')  

  clients: Mapped['Client'] = relationship('Client', back_populates='client_group')



class Client(Base):
  __tablename__ = 'client'
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(nullable=False)
  full_name: Mapped[str] = mapped_column(nullable=False, info={'desc': 'Наименование Юр.лица'})
  certificate: Mapped[str] = mapped_column(nullable=False)
  contract_number: Mapped[str]
  contract_date: Mapped[datetime]
  city: Mapped[str] = mapped_column(nullable=False)
  address:Mapped[str] = mapped_column(nullable=False)
  email:Mapped[str] = mapped_column(nullable=False)
  phone:Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
  price:Mapped[int] 
  
  currency_id = mapped_column(sqlalchemy.ForeignKey('currency.id'))
  currency: Mapped[Currency] = relationship(back_populates='client')
  
  client_group_id = mapped_column(sqlalchemy.ForeignKey('client_group.id'))
  client_group: Mapped['ClientGroup'] = relationship('ClientGroup', back_populates='clients')
  
  another_contract: Mapped[List['AnotherContracts']] = relationship(back_populates='client')
  track_collections: Mapped[List['TrackCollection']] = relationship(secondary='trackCollections_client_association', back_populates='clients')
  
  
  
  
class AnotherContracts(Base):
  __tablename__ = 'another_contracts'
  
  id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
  contract_number = sqlalchemy.Column(sqlalchemy.Date)
  payment_date = sqlalchemy.Column(sqlalchemy.Date)
  
  client_id = mapped_column(sqlalchemy.ForeignKey('client.id'))
  client: Mapped['Client'] = relationship(back_populates='another_contract')
  
  