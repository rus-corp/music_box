from typing import TYPE_CHECKING
from pydantic import BaseModel, constr, EmailStr
from typing import Optional, List


from backend.clients.schemas import ShowUserClients



# =============== User Role Schemas ==================

class UserRoleCreate(BaseModel):
  role_name: str
  

class UserRoleShow(BaseModel):
  id: int
  role_name: str
  
  class Config:
    from_attributes = True
    

class UpdateRoleShow(UserRoleShow):
  pass


# =============== User Schemas ==================

class UserBase(BaseModel):
  class Config:
    from_attributes = True


class ShowUser(UserBase):
  id: int
  name: str
  login: str
  email: EmailStr
  is_active: bool
  comment: Optional[str] = None
  is_superuser: bool
  
  role: UserRoleShow
  client: Optional[List[ShowUserClients] | ShowUserClients] = None
  
  
class CreateSuperUser(BaseModel):
  name: str
  login: str
  email: EmailStr
  password: str
  
  
class CreateUser(BaseModel):
  name: str
  login: str
  email: EmailStr
  password: str
  comment: Optional[str] = None
  
  role_id: int
  
  
class UserUpdate(BaseModel):
  id: int
  name: Optional[constr(min_length=2)] = None # type: ignore
  login: Optional[constr(min_length=2)] = None # type: ignore
  password: Optional[constr(min_length=6)] = None # type: ignore
  role_id: Optional[int] = None


class DeleteUserResponse(BaseModel):
  id: int


class UserShowForClient(UserBase):
  id: int
  name: str
  comment: str
  login: str
  email: str
  is_active: bool
  is_superuser: bool
  