from pydantic import BaseModel, constr, EmailStr
from typing import Optional, List
from datetime import date

from backend.music.schemas import TrackCollectionShow


class CurrencyShow(BaseModel):
  id: int
  cur_name: str

  
class CurrencyDeleteResponse(BaseModel):
  currency_delete_id: int

class UpdateCurrencyRequest(BaseModel):
  cur_name: str
  
  
class UpdateCurrencyResponse(BaseModel):
  cur_name: Optional[constr(min_length=2)] # type: ignore


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
  

class ShowClient(BaseClient):
  client_id: int
  user: int
  track_collections: List[TrackCollectionShow] = None
  currency: CurrencyShow = None