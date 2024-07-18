from typing import List, Optional, Union
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


class UpdateCollectiongroupRequest(BaseModel):
  id: int
  name: str


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


class AppendTrackCollectionToClient(BaseModel):
  track_collection_id: int
  client_id: int

# =========== Tracks Schemas ============
class TrackShow(BaseModel):
  id: int
  title: str
  artist: str
  label: str
  open_name: str
  file_path: str
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
  

class TrackError(BaseModel):
  message: str
  
  
class TrackCreateResponse(BaseModel):
  error_tracks: Optional[List[Union[str, TrackError]]] = []
  created_tracks: Optional[List[Union[str, TrackError]]] = []
  
  
class DeletedTrackFromCollection(BaseModel):
  track_collection_id: int
 
# ================ COMMON MODELS =================== 
class GroupCollectionWithTrackCollectionCreate(GroupCollectionShow):
  track_collection: 'TrackCollectionShow'
  
  
class GroupCollectionWithTrackCollectionShow(GroupCollectionShow):
  track_collections: List[TrackCollectionShow]
  
  
class TrackCollectionWithTracks(TrackCollectionShow):
  tracks: List[TrackShow]

