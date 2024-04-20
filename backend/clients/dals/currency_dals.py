from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete


from ..models import Currency

class CurrencyDAL:
  def __init__(self, db_session: AsyncSession) -> None:
    self.db_session = db_session
  
  
  async def create_currency(self, name):
    new_currency = Currency(cur_name=name)
    self.db_session.add(new_currency)
    await self.db_session.flush()
    return new_currency


  async def get_all_currency(self):
    query = select(Currency).order_by(Currency.id)
    result = await self.db_session.execute(query)
    return result.scalars().all()


  async def get_currency_by_id(self, currency_id: int):
    query = select(Currency).where(Currency.id == currency_id)
    currency = await self.db_session.scalar(query)
    return currency


  async def update_currency(self, currency_id: int, new_name: str):
    stmt = update(Currency).where(Currency.id == currency_id).values(
      new_name).returning(Currency)
    result = await self.db_session.execute(stmt)
    currency = result.fetchone()
    if currency is not None:
      return currency[0]


  async def delete_currency_by_id(self, currency_id):
    stmt = delete(Currency).where(Currency.id == currency_id).returning(Currency.id)
    deleted_currency = await self.db_session.execute(stmt)
    await self.db_session.commit()
    if deleted_currency is not None:
      return True