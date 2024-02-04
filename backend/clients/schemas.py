from pydantic import BaseModel, constr, EmailStr
from typing import Optional, List
from datetime import date


class CurrencyShow(BaseModel):
  cur_id: int
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
  
  price_currency: CurrencyShow
  
  class Config:
    from_attributes = True
  
  
class CreateClient(BaseClient):
  pass

class ShowClient(BaseClient):
  client_id: int
  user: int