from sqlalchemy import Column, Integer, String, DateTime, JSON
from app.database import Base
from datetime import datetime

class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    offer_id = Column(String, index=True)
    bank_name = Column(String, index=True)
    offer_text = Column(String)
    description = Column(String)
    payment_instruments = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
