from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.node import NodeCreate, NodeUpdate, Node, NodeDetail
from app.services.node_service import NodeService

router = APIRouter(prefix="/nodes", tags=["nodes"])

@router.post("/", response_model=Node)
def create_node(node: NodeCreate, db: Session = Depends(get_db)):
    return NodeService.create_node(db, node)

@router.get("/", response_model=List[Node])
def get_all_nodes(db: Session = Depends(get_db)):
    return NodeService.get_all_nodes(db)

@router.get("/{node_id}", response_model=NodeDetail)
def get_node(node_id: int, db: Session = Depends(get_db)):
    node = NodeService.get_node_with_relationships(db, node_id)
    if node is None:
        raise HTTPException(status_code=404, detail=f"Node with ID {node_id} not found")
    return node

@router.put("/{node_id}", response_model=Node)
def update_node(node_id: int, node: NodeUpdate, db: Session = Depends(get_db)):
    updated_node = NodeService.update_node(db, node_id, node)
    if not updated_node:
        raise HTTPException(status_code=404, detail=f"Node with ID {node_id} not found")
    return updated_node

@router.delete("/{node_id}")
def delete_node(node_id: int, db: Session = Depends(get_db)):
    deleted = NodeService.delete_node(db, node_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Node with ID {node_id} not found")
    return {"message": f"Node with ID {node_id} deleted successfully"}