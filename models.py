from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime,func
from database import Base
from database import Base

class WearableData(Base):
    __tablename__ = "wearable_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    heart_rate = Column(Integer)
    steps = Column(Integer)
    sleep_hours = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
