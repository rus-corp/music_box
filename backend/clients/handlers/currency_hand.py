from sqlalchemy.ext.asyncio import AsyncSession


from backend.auth import errors
from ..dals.currency_dals import CurrencyDAL





async def _create_currency(session: AsyncSession, currency_name: str):
  async with session.begin():
    currency_dal = CurrencyDAL(session)
    new_currency = await currency_dal.create_currency(name=currency_name)
    return new_currency
    

async def _get_all_currencies(session: AsyncSession):
  async with session.begin():
    currency_dal = CurrencyDAL(session)
    currencies = await currency_dal.get_all_currency()
    return list(currencies)
  

async def _get_currency_by_id(session : AsyncSession, currency_id):
  async with session.begin():
    currency_dal = CurrencyDAL(session)
    currency = await currency_dal.get_currency_by_id(currency_id)
    if currency is None:
      return errors.not_Found_error
    return currency
  

async def _update_currency(session: AsyncSession, currency_id: int, new_name: str):
  async with session.begin():
    currency_dal = CurrencyDAL(session)
    has_currency = await currency_dal.get_currency_by_id(currency_id)
    if has_currency is None:
      return errors.not_Found_error
    updated_currency = currency_dal.update_currency(
      currency_id=currency_id, new_name=new_name
    )
    return updated_currency
  
  
async def _delete_currency(session: AsyncSession, currency_id: int):
  async with session.begin():
    currency_dal = CurrencyDAL(session)
    has_currency = await currency_dal.get_currency_by_id(currency_id)
    if has_currency is None:
      return errors.not_Found_error
    deleted_currency = currency_dal.delete_currency_by_id(currency_id)
    return deleted_currency



async def _add_currency_to_client(session: AsyncSession, client_id: int): pass