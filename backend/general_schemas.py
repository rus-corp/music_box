from typing import Optional, List

from .clients.schemas import ClientClusterShow, ClientGroupShow, ShowClientWithTrackColections
from .users.schemas import UserShowForClient, ShowUser






class ClientGroupShow_With_Clients(ClientGroupShow):
  clients: Optional[ShowClientWithTrackColections] = None


class ClientGroupAppendUserResponse(ClientGroupShow):
  user: Optional[UserShowForClient]
  
  class Config:
    from_attributes = True


class UserWithClient(ShowUser):
  client_groups: Optional[List[ClientGroupShow]]