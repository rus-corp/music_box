from typing import List, Optional
from pydantic import BaseModel, constr
from datetime import datetime

# =========== GroupCollection Schemas ============
class GroupCollectionCreate(BaseModel):
  group_name: str
  
  class Config:
    from_attributes = True
  

  
class GroupCollectionShow(BaseModel):
  id: int
  group_name: str
  
  class Config:
    from_attributes = True
  

class DeletedGroupResponse(BaseModel):
  delete_group_id: int
  
    
  

# =========== TrackCollection Schemas ============
class TrackCollectionCreate(BaseModel):
  track_collection_name: str
  player_option: bool = True
  group_coollection_id: int
  

class TrackCollectionShow(BaseModel):
  id: int
  name: str
  player_option: bool
  
  class Config:
    from_attributes = True


class TrackCollectionUpdateResponse(BaseModel):
  name: Optional[str] = None
  player_option: Optional[bool] = None


class TrackCollectionDeleteResponse(BaseModel):
  track_collection_id: int
  
  
  
# =========== Tracks Schemas ============
class TrackShow(BaseModel):
  id: int
  title: str
  artist: str
  label: str
  open_name: str
  created_at: datetime
  
  class Config:
    from_attributes = True
    

class TrackCreate(BaseModel):
  title: str
  artist: str
  label: str
  open_name: str
  

class TrackUpdate(BaseModel):
  title: Optional[constr(min_length=2)] # type: ignore
  artist: Optional[constr(min_length=2)] # type: ignore
  label: Optional[constr(min_length=2)] # type: ignore
  open_name: Optional[constr(min_length=2)] # type: ignore
  
 
 
# ================ Service Models =================== 
class GroupCollectionWithTrackCollectionCreate(GroupCollectionShow):
  track_collections: 'TrackCollectionShow'
  
  
class GroupCollectionWithTrackCollectionShow(GroupCollectionShow):
  track_collections: List[TrackCollectionShow]