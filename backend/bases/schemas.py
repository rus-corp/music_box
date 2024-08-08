from typing import Optional, List, Union
from pydantic import BaseModel, ConfigDict




class MainBaseModel(BaseModel):
  model_config = ConfigDict(from_attributes=True)


class CreateBase(MainBaseModel):
  name: str


class ShowBase(MainBaseModel):
  id: int
  name: str


class UpdateBaseRequest(ShowBase):
  pass


class DeletedBase(MainBaseModel):
  id: Union[str, int]
  
  class Config:
    from_attributes=True



class BaseCollectionModel(BaseModel):
  model_config = ConfigDict(from_attributes=True)


class ShowBaseCollection(BaseCollectionModel):
  id: int
  name: str
  main_base_id: int

class BaseCollectionCreateRequest(BaseCollectionModel):
  name: str
  base_id: int


class BaseCollectionUpdateRequest(BaseCollectionModel):
  name: Optional[str] = None
  main_base_id: Optional[int] = None


class ShowBaseWithCollection(ShowBase):
  collections: Optional[List[ShowBaseCollection]] = []