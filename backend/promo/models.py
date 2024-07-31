from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, DateTime, ForeignKey
from datetime import datetime



from backend.clients.models import Client
from backend.database import Base




class PromotionAudo(Base):
  _tablename__ = 'promo_audio'
  
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name:Mapped[str] = mapped_column(nullable=False)
  file_path: Mapped[str] = mapped_column(nullable=False)
  created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True), server_default=func.now()
  )
  
  client_id: Mapped[int] = mapped_column(
    ForeignKey('client.id', ondelete='CASCADE')
  )
  client: Mapped['Client'] = relationship(back_populates='promotions')