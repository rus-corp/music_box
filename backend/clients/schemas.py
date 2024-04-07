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



# =================== CLIENT ====================
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
  user_id: int


class ShowClient(BaseClient):
  client_id: int
  user: int
  track_collections: List[TrackCollectionShow] = None
  currency: CurrencyShow = None


class UpdateClientRequest(BaseModel):
  id: Optional[int] = None
  name: Optional[str] = None
  full_name: Optional[str] = None
  certificate: Optional[str] = None
  contract_number: Optional[str] = None
  contract_date: Optional[date] = None
  city: Optional[str] = None
  address: Optional[str] = None
  email: Optional[EmailStr] = None
  phone: Optional[str] = None
  price: Optional[float] = None
  currency: Optional[int] = None
  user_id: Optional[int] = None
  
  class Config:
    from_attributes = True



class UpdateClientResponse(BaseClient):
  id: int
  currency_id: int
  user_id: int
