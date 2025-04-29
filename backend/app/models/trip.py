import uuid
from sqlalchemy import Column, String, Date, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Trip(Base):
    __tablename__ = "trips"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    trip_name = Column(String, nullable=True)
    trip_data = Column(JSON, nullable=False)

    def __repr__(self):
        return f"<Trip id={self.id} session_id={self.session_id}>"
