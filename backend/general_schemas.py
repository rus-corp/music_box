from typing import Optional, List

from .clients.schemas import ClientClusterShow, ClientGroupShow, ShowClient
from .users.schemas import UserShowForClient


class ClientClusterShow_With_ClientGroups(ClientClusterShow):
  client_groups: ClientGroupShow


class ClientGroupShow_With_Clients(ClientGroupShow):
  clients: Optional[ShowClient] = None


class ClientGroup_WithUsers(ClientGroupShow):
  users: Optional[List[UserShowForClient]] = None
  
  class Config:
    from_attributes = True