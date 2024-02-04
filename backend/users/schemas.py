from pydantic import BaseModel, constr
from typing import Optional



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
  

class DeleteUserRole(BaseModel):
  id: int



# =============== User Schemas ==================

class UserBase(BaseModel):
  class Config:
    from_attributes = True
    
    
class ShowUser(UserBase):
  id: int
  name: str
  login: str
  password: str
  is_active: bool
  is_superuser: bool
  comment: Optional[str] = None
  
  role: UserRoleShow
  
  
class CreateUser(BaseModel):
  name: str
  login: str
  password: str
  comment: Optional[str] = None
  
  role_id: int
  
  
class UserUpdate(BaseModel):
  name: Optional[constr(min_length=2)] # type: ignore
  login: Optional[constr(min_length=2)] # type: ignore
  password: Optional[constr(min_length=6)] # type: ignore