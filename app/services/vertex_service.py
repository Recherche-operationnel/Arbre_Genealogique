from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.vertex import Vertex
from app.models.node import Node
from app.schemas.vertex import VertexCreate, VertexUpdate
from typing import List, Optional

class VertexService:
    @staticmethod
    def create_vertex(db: Session, vertex_data: VertexCreate) -> Optional[Vertex]:
        # Check if parent and child nodes exist
        parent = db.query(Node).filter(Node.id == vertex_data.parent_id).first()
        child = db.query(Node).filter(Node.id == vertex_data.child_id).first()
        
        if not parent or not child:
            return None
        
        # Verify the max parents constraint: max 2^rank parents per node at rank k
        rank = vertex_data.rank
        child_id = vertex_data.child_id
        
        current_parents_count = db.query(func.count(Vertex.id)).filter(
            Vertex.child_id == child_id,
            Vertex.rank == rank
        ).scalar()
        
        if current_parents_count >= 2**rank:
            return None  # Max parents constraint violated
        
        # Generate vertex ID
        vertex_id = f"v_{vertex_data.parent_id}_{vertex_data.child_id}_{vertex_data.rank}"
        
        # Create and save the vertex
        db_vertex = Vertex(
            id=vertex_id,
            rank=vertex_data.rank,
            parent_id=vertex_data.parent_id,
            child_id=vertex_data.child_id
        )
        
        db.add(db_vertex)
        db.commit()
        db.refresh(db_vertex)
        
        return db_vertex

    @staticmethod
    def get_vertex(db: Session, vertex_id: str) -> Optional[Vertex]:
        return db.query(Vertex).filter(Vertex.id == vertex_id).first()

    @staticmethod
    def get_all_vertices(db: Session) -> List[Vertex]:
        return db.query(Vertex).all()

    @staticmethod
    def update_vertex(db: Session, vertex_id: str, vertex_data: VertexUpdate) -> Optional[Vertex]:
        db_vertex = db.query(Vertex).filter(Vertex.id == vertex_id).first()
        if not db_vertex:
            return None
            
        update_data = vertex_data.dict(exclude_unset=True)
        
        # Check rank constraint if needed
        if "rank" in update_data:
            new_rank = update_data["rank"]
            child_id = update_data.get("child_id", db_vertex.child_id)
            
            if new_rank != db_vertex.rank:
                current_parents_count = db.query(func.count(Vertex.id)).filter(
                    Vertex.child_id == child_id,
                    Vertex.rank == new_rank,
                    Vertex.id != vertex_id
                ).scalar()
                
                if current_parents_count >= 2**new_rank:
                    return None  # Max parents constraint violated
        
        # Update vertex attributes
        for key, value in update_data.items():
            setattr(db_vertex, key, value)
            
        db.commit()
        db.refresh(db_vertex)
        return db_vertex

    @staticmethod
    def delete_vertex(db: Session, vertex_id: str) -> bool:
        db_vertex = db.query(Vertex).filter(Vertex.id == vertex_id).first()
        if not db_vertex:
            return False
            
        db.delete(db_vertex)
        db.commit()
        return True