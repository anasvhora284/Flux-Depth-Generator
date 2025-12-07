from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime
from app.core.database import Base
import enum

class JobStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True) # Nullable for guest jobs if we allow them later
    
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    
    total_files = Column(Integer, default=0)
    processed_files = Column(Integer, default=0)
    
    # Store path to the final zip or temp directory
    file_path = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    error_message = Column(String, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="jobs")
