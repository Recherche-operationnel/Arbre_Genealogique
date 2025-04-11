from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Vertex(Base):
    __tablename__ = "vertices"

    id = Column(String, primary_key=True)
    rank = Column(Integer, nullable=False)
    parent_id = Column(Integer, ForeignKey("nodes.id", ondelete="CASCADE"))
    child_id = Column(Integer, ForeignKey("nodes.id", ondelete="CASCADE"))

    # Relationships
    parent = relationship("Node", foreign_keys=[parent_id], back_populates="parent_vertices")
    child = relationship("Node", foreign_keys=[child_id], back_populates="child_vertices")