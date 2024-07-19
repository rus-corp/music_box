from typing import TYPE_CHECKING
from pydantic import BaseModel, constr, EmailStr
from typing import Optional, List
from datetime import date


from backend.music.schemas import TrackCollectionShow



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

class ClientClusterDeleteResponse(ClientClusterBase):
  id: int


# =================== CLIENT GROUP ====================
class ClientGroupBase(BaseModel):
  class Config:
    from_attributes = True


class ClientGroupShow(ClientGroupBase):
  id: int
  name: str
  comment: Optional[str] = None


class ClientGroupShowDefault(ClientGroupShow):
  client_cluster: ClientClusterShow


class ClientGroupCreateRequest(ClientGroupBase):
  name: str
  comment: Optional[str] = None
  client_cluster_id: int


class ClientGroupCreateResponse(ClientGroupShow):
  client_cluster: ClientClusterShow


class ClientGroupUpdateRequset(ClientGroupBase):
  name: Optional[str] = None
  comment: Optional[str] = None
  client_cluster_id: Optional[int] = None


class ClientGroupUpdateResponse(BaseModel):
  id: int
  name: str
  comment: str
  client_cluster: int
  old_client_cluster: ClientClusterShow


class ClientGroupDeleteResponse(BaseModel):
  id: int


class AppendUserToGroupRequest(BaseModel):
  client_group_id: int
  user_id: int


# =================== CLIENT PROFILE ====================
class ClientProfileBase(BaseModel):
  address: str
  full_name: str
  certificate: str
  contract_number: str
  contract_date: date
  
  class Config:
    from_attributes = True


class ClientProfileDefaultResponse(ClientProfileBase):
  id: int


class ClientProfileUpdateRequest(BaseModel):
  address: Optional[str] = None
  full_name: Optional[str] = None
  certificate: Optional[str] = None
  contract_number: Optional[str] = None
  contract_date: Optional[date] = None



# =================== CLIENT ====================
class BaseClient(BaseModel):
  name: str
  city: str
  email: EmailStr
  phone: str
  price: int
  client_group_id: int
  
  class Config:
    from_attributes = True


class CreateClient(BaseClient):
  currency_id: int
  profile: ClientProfileBase


class ClientProfileCreateResponse(BaseClient):
  id: int
  profile: ClientProfileDefaultResponse


class ShowClientWithTrackColections(BaseClient):
  id: int
  profile: ClientProfileDefaultResponse
  track_collections: List[TrackCollectionShow] = None
  currency: CurrencyShow = None


class ShowClientWithClientGroup(BaseClient):
  id: int
  profile: ClientProfileDefaultResponse
  client_group: ClientGroupShowDefault
  currency: CurrencyShow = None


class ClientShowForGroup(BaseModel):
  id: int
  name: str
  

class UpdateClientRequest(BaseModel):
  name: Optional[str] = None
  city: Optional[str] = None
  email: Optional[EmailStr] = None
  phone: Optional[str] = None
  price: Optional[float] = None
  currency_id: Optional[int] = None
  profile: Optional[ClientProfileUpdateRequest] = None
  
  class Config:
    from_attributes = True



class UpdateClientResponse(BaseClient):
  id: int
  currency_id: int
  user_id: int


class ClientClusterShow_With_ClientGroups(ClientClusterShow):
  client_groups: Optional[ClientGroupShow] = None


class ClientClusterShow_With_Listr_ClientGroups(ClientClusterShow):
  client_groups: Optional[List[ClientGroupShow]] = None


class ClientGroupWithClientShow(ClientGroupShowDefault):
  clients: Optional[List[ClientShowForGroup]] = None