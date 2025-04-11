from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Spouse(Base):
    __tablename__ = "spouses"

    id = Column(Integer, primary_key=True, index=True)
    node1_id = Column(Integer, ForeignKey("nodes.id", ondelete="CASCADE"))
    node2_id = Column(Integer, ForeignKey("nodes.id", ondelete="CASCADE"))

    # Define a unique constraint to prevent duplicate spouse relationships
    __table_args__ = (UniqueConstraint('node1_id', 'node2_id', name='unique_spouse_relationship'),)

    # Relationships
    node1 = relationship("Node", foreign_keys=[node1_id], back_populates="spouse_relationships1")
    node2 = relationship("Node", foreign_keys=[node2_id], back_populates="spouse_relationships2")