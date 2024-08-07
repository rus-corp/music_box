from typing import Optional, List
from pydantic import BaseModel, EmailStr
from .clients.schemas import ClientClusterShow, ClientGroupShow, ShowClientWithTrackColections
from .users.schemas import UserShowForClient, ShowUser
from .collections.schemas import TrackCollectionShow


class ErrorMessageResponse(BaseModel):
  message: str



class ClientGroupShow_With_Clients(ClientGroupShow):
  clients: Optional[ShowClientWithTrackColections] = None


class ClientGroupAppendUserResponse(ClientGroupShow):
  user: Optional[UserShowForClient]
  
  class Config:
    from_attributes = True


class UserWithClient(ShowUser):
  client_groups: Optional[List[ClientGroupShow]]


class ClientWithTrackCollection(BaseModel):
  id: int
  name: str
  city: str
  email: EmailStr
  phone: str
  price: int
  
  track_collection: TrackCollectionShow
  