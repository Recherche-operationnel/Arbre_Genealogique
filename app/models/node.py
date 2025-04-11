from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    birthday = Column(String, nullable=True)
    sex = Column(Boolean, nullable=True)

    # Relationships
    parent_vertices = relationship("Vertex", foreign_keys="Vertex.parent_id", back_populates="parent")
    child_vertices = relationship("Vertex", foreign_keys="Vertex.child_id", back_populates="child")
    
    # Spouse relationships
    spouse_relationships1 = relationship("Spouse", foreign_keys="Spouse.node1_id", back_populates="node1")
    spouse_relationships2 = relationship("Spouse", foreign_keys="Spouse.node2_id", back_populates="node2")

    @property
    def parents(self):
        return [vertex.parent for vertex in self.child_vertices]

    @property
    def children(self):
        return [vertex.child for vertex in self.parent_vertices]

    @property
    def spouses(self):
        # Combine spouses from both relationships
        spouses = []
        for rel in self.spouse_relationships1:
            spouses.append(rel.node2)
        for rel in self.spouse_relationships2:
            spouses.append(rel.node1)
        return spouses