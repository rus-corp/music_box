from typing import TYPE_CHECKING
from pydantic import BaseModel, constr, EmailStr
from typing import Optional, List
from datetime import date

from backend.music.schemas import TrackCollectionShow


# from backend.users.schemas import UserShowForClient



# =================== CURRENCY ====================
class CurrencyBase(BaseModel):
  class Config:
    from_attributes = True


class CurrencyShow(CurrencyBase):
  id: int
  cur_name: str



class UpdateCurrencyRequest(CurrencyBase):
  cur_name: str


class UpdateCurrencyResponse(CurrencyBase):
  cur_name: Optional[constr(min_length=2)] # type: ignore



# =================== CLIENT CLUSTER ====================
class ClientClusterBase(BaseModel):
  class Config:
    from_attributes = True


class ClientClusterShow(ClientClusterBase):
  id: int
  name: str


class ClientClusterCreate(ClientClusterBase):
  name: str




# =================== CLIENT GROUP ====================
class ClientGroupBase(BaseModel):
  class Config:
    from_attributes = True


class ClientGroupShow(ClientGroupBase):
  id: int
  name: str
  comment: Optional[str] = None


class ClientGroupCreate(ClientGroupBase):
  name: str
  comment: Optional[str] = None
  client_cluster_id: int


class ClientGroupUpdate(ClientGroupBase):
  id: int
  name: Optional[str] = None
  comment: Optional[str] = None


# =================== CLIENT ====================
class BaseClient(BaseModel):
  name: str
  full_name: str
  certificate: str
  contract_number: str
  contract_date: date
  city: str
  address: str
  email: EmailStr
  phone: str
  price: float
  
  class Config:
    from_attributes = True


class CreateClient(BaseClient):
  currency_id: int
  user_id: int


class ShowClient(BaseClient):
  client_id: int
  user: int
  track_collections: List[TrackCollectionShow] = None
  currency: CurrencyShow = None


class ShowUserClients(BaseClient):
  client_id: int
  currency: CurrencyShow = None


class UpdateClientRequest(BaseModel):
  name: Optional[str] = None
  full_name: Optional[str] = None
  certificate: Optional[str] = None
  contract_number: Optional[str] = None
  contract_date: Optional[date] = None
  city: Optional[str] = None
  address: Optional[str] = None
  email: Optional[EmailStr] = None
  phone: Optional[str] = None
  price: Optional[float] = None
  currency: Optional[int] = None
  user_id: Optional[int] = None
  
  class Config:
    from_attributes = True



class UpdateClientResponse(BaseClient):
  id: int
  currency_id: int
  user_id: int


# ================ COMMON MODELS =================== 
class ClientClusterShow_With_ClientGroups(ClientClusterShow):
  client_groups: ClientGroupShow

class ClientGroupShow_With_Clients(ClientGroupShow):
  clients: Optional[ShowClient] = None


# class ClientGroup_WithUsers(ClientGroupShow):
#   users: Optional[List[UserShowForClient]] = None