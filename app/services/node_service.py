from sqlalchemy.orm import Session
from app.models.node import Node
from app.schemas.node import NodeCreate, NodeUpdate, NodeDetail
from typing import List, Optional, Dict, Any

class NodeService:
    @staticmethod
    def create_node(db: Session, node_data: NodeCreate) -> Node:
        db_node = Node(**node_data.dict())
        db.add(db_node)
        db.commit()
        db.refresh(db_node)
        return db_node

    @staticmethod
    def get_node(db: Session, node_id: int) -> Optional[Node]:
        return db.query(Node).filter(Node.id == node_id).first()

    @staticmethod
    def get_all_nodes(db: Session) -> List[Node]:
        return db.query(Node).all()

    @staticmethod
    def update_node(db: Session, node_id: int, node_data: NodeUpdate) -> Optional[Node]:
        db_node = db.query(Node).filter(Node.id == node_id).first()
        if not db_node:
            return None
            
        # Update the node attributes
        for key, value in node_data.dict(exclude_unset=True).items():
            setattr(db_node, key, value)
            
        db.commit()
        db.refresh(db_node)
        return db_node

    @staticmethod
    def delete_node(db: Session, node_id: int) -> bool:
        db_node = db.query(Node).filter(Node.id == node_id).first()
        if not db_node:
            return False
            
        db.delete(db_node)
        db.commit()
        return True

    @staticmethod
    def get_node_with_relationships(db: Session, node_id: int) -> Optional[Node]:
        node = db.query(Node).filter(Node.id == node_id).first()
        return node